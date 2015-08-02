import os
import random
import pickle
import logging
from math import log
from pathlib import Path
from operator import itemgetter

import numpy as np
from sklearn import svm

from stemmer import NepStemmer

stemmer = NepStemmer()
stemmer.read_stems()

# Creating a logger
logger = logging.getLogger('Classifier')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

class NepClassifier():
    """ Class to perform the classification of nepali news """
    def __init__(self):
        # Base path to use
        self.base_path = os.path.dirname(__file__)

        # Folder containg data
        self.data_path = os.path.join(self.base_path, 'data')

        # Training data size
        self.train_num = 10000
        
        # Test data size
        self.test_num = 1000

        # Maximum stems to use
        self.max_stems = 1000

        # Stems to use as feature
        self.stems = None

        # Vector to hold the IDF of stems
        self.idf_vector = None

        # Training data to use
        self.train_data = []
        self.test_data = []

        # Document categories
        self.categories = []

        # Classifier
        self.clf = None

    def process_corpus(self):
        ''' 
            Class method to process corpus located at path provided 
            at self.data_path

            The data must be organized as utf-8 encoded raw text file
            having following structure

            root/
                class1/
                    text11.txt
                    text12.txt
                class2/
                    text21.txt
                    text22.txt
                ...
        '''

        logger.info('Processing corpus at : ' + self.data_path)

        # Vectors for stems
        count_vector = {}
        idf_vector_total = {}

        total_docs = 0

        for root,dirs,files in os.walk(self.data_path):
            for file_path in files:
                abs_path = os.path.join(self.base_path, root, file_path)

                file = open(abs_path, 'r')
                content = file.read()
                file.close()

                # Obtain known stems
                doc_stems = stemmer.get_known_stems(content)
                doc_stems_set = set(doc_stems)

                # Add the count of stems
                for stem in doc_stems:
                    count_vector[stem] = count_vector.get(stem,0) + 1

                for stem in doc_stems_set:
                    idf_vector_total[stem] = idf_vector_total.get(stem, 0) + 1

                total_docs += 1

        # Obtain frequently occuring stems
        stem_tuple=sorted(
            count_vector.items(),
            key = itemgetter(1),
            reverse = True
        )[:self.max_stems]

        print(stem_tuple[-10:])
    
        # Construct a ordered list of frequent stems
        stems = [item[0] for item in stem_tuple]

        # IDF vector for the stems
        idf_vector = [
            log(total_docs / (1 + idf_vector_total[k])) 
            for k in stems
        ]
        
        # Dump the data obtained
        data = {
            'stems' : stems,
            'idf_vector' : idf_vector
        }
        data_file = os.path.join(self.base_path, 'data.p')
        pickle.dump(data, open(data_file, 'wb'))

    def load_corpus_info(self):
        '''
            Load the corpus information from the file
            data.p located along with this script 
        '''

        # Load dump data
        data_file = os.path.join(self.base_path, 'data.p')
        data = pickle.load(open(data_file, 'rb'))
        
        self.stems = data['stems']
        self.idf_vector = data['idf_vector']

        logger.info('Corpus info loaded')

    def load_training_data(self):
        '''
            Load training data from the path specified by
            self.data_path

            The files are loaded as a dictionary similar to one
            given below
            doc = {
                'path' : '../data/text1.txt',
                'category_id' : 1
            }
        '''

        data_path = os.path.join(self.base_path, 'data')
        category_id = 0

        docs = []

        categories = ['economy', 'entertainment', 'politics', 'sports', 'world']

        for category in Path(data_path).iterdir():

            # Convert path to posix notation
            category_name = category.as_posix().split('/')[-1]

            if (not(category in categories)):
            	continue

            self.categories.append(category_name)

            for filepath in category.iterdir():
                docs.append({
                        'path' : filepath.as_posix(),
                        'category_id' : category_id
                    })

            category_id += 1

        sample_docs = random.sample(
            docs,
            self.train_num + self.test_num
        )
        
        self.test_data = sample_docs[-1000:]
        self.train_data = sample_docs[:-1000]
            
        logger.info('Train and test data loaded')

    def compute_matrix(self, data):
        stems_size = len(self.stems)
        docs_size = len(data)

        # Tf matrix
        tf_matrix = np.ndarray(
            (docs_size, stems_size),
            dtype = 'float16'
        )

        idf_matrix = np.array(self.idf_vector)

        # Training matrix
        input_matrix = np.ndarray(
            (docs_size, stems_size),
            dtype='float16'
        )

        output_matrix = np.ndarray((docs_size, 1), dtype = 'float16')

        # Use a sample of documents
        for i,doc in enumerate(data):

            file = open(doc['path'], 'r')
            content = file.read()
            file.close()

            # Find stems in document
            doc_stems = stemmer.get_known_stems(content)

            doc_vector = {}
            for stem in doc_stems:
                doc_vector[stem] = doc_vector.get(stem, 0) + 1

            doc_vector_list = doc_vector.values()
            if(not(doc_vector_list)):
                max_count = 1
            else:
                max_count = max(doc_vector_list)
                if (max_count == 0):
                    max_count = 1

            # Compute the tf and append it
            tf_matrix[i, :] = 0.5 + (0.5 / max_count) * np.array(
                [doc_vector.get(stem, 0) for stem in self.stems]
            )

            output_matrix[i, 0] = doc['category_id']

        # Element wise multiplication
        for i in range(docs_size):
            input_matrix[i, :] = tf_matrix[i, :] * idf_matrix

        output_matrix = output_matrix.ravel()

        return (input_matrix, output_matrix)
    
    # Compute tf-idf and train classifier
    def train(self):
        if (not(self.stems)):
            raise Exception('Corpus info not available.')

        if (not(self.train_data)):
            raise Exception('Training data not selected')

        logger.info('Computing feature matrix')

        input_matrix, output_matrix = self.compute_matrix(self.train_data)

        logger.info('Training classifier')

        # Assign and train a SVM
        clf = svm.SVC()
        clf.fit(input_matrix,output_matrix)

        data = {
            'categories' : self.categories,
            'clf' : clf,
        }

        # Dumping extracted data
        clf_file = os.path.join(self.base_path,'clf.p')
        pickle.dump(data,open(clf_file,'wb'))
    
    def load_clf(self):
        if (not(self.stems)):
            self.load_data()

        clf_file = os.path.join(self.base_path, 'clf.p')
        data = pickle.load(open(clf_file, 'rb'))

        self.categories = data['categories']
        self.clf = data['clf']

        logger.info('Classifier loaded')

    # Compute tf-idf for a text
    def tf_idf_vector(self, text):
        if (not(self.stems)):
            raise Exception('Corpus info not available')

        # Find stems in document
        doc_stems = stemmer.get_known_stems(text)

        doc_vector = {}
        for stem in doc_stems:
            doc_vector[stem] = doc_vector.get(stem, 0) + 1

        doc_vector_list = [doc_vector.get(stem, 0) for stem in self.stems]

        max_count = max(doc_vector_list)
        if (max_count == 0):
            max_count = 1

        tf_vector = [0.5 + (0.5 / max_count) * x for x in doc_vector_list]

        tf_idf_vector = []
        for i in range(len(self.stems)):
            tf_idf_vector.append(tf_vector[i] * self.idf_vector[i])

        return(tf_idf_vector)

    # Predict the class
    def predict(self,text):
        if (not(self.clf)):
            raise Exception('Classifier not loaded')
        
        if (text == ''):
            raise Exception('Empty text provided')
        
        tf_idf_vector = self.tf_idf_vector(text)
        output_val = self.clf.predict(tf_idf_vector)[0]
        
        class_id = int(output_val)
        return (self.categories[class_id])

    def validate_model(self):
        if (not(self.clf)):
            raise Exception('Classifier not loaded')

        input_matrix, output_matrix = self.compute_matrix(self.train_data)

        return(self.clf.score(input_matrix, output_matrix))

def main():
    var1 = NepClassifier()
    # var1.process_corpus()

    var1.load_corpus_info()
    var1.load_training_data()
    
    var1.train()
    var1.load_clf()
    score = var1.validate_model()
    print('Accuracy : ', score*100, '%')

if __name__ == '__main__':
    main()
