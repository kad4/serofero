import os
import random
import pickle
from math import log
from pathlib import Path
from operator import itemgetter

import numpy as np
from sklearn import svm

from stemmer import NepStemmer

stemmer = NepStemmer()
stemmer.read_stems()

class NepClassifier():
    """ Class to perform the classification of nepali news """
    def __init__(self):
        # Base path to use
        self.base_path = os.path.dirname(__file__)

        # Folder containg data
        self.data_path = os.path.join(self.base_path, 'data')

        # Training data for each class
        self.doc_num = 1200
        
        # Total testing data
        self.test_num = 1000

        # Maximum stems to use
        self.max_stems = 2000

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
        )[10 : self.max_stems+10]
    
        # Construct a ordered list of frequent stems
        stems = [item[0] for item in stem_tuple]

        # IDF vector for the stems
        idf_vector = [log(total_docs / (1 + idf_vector_total[k]) for k in stems)]
        
        # Dump the data obtained
        data = {
            'stems' : stems,
            'idf_vector' : idf_vector
        }
        data_file = os.path.join(self.base_path, 'data.p')
        pickle.dump(data, open(data_file, 'wb'))

    def load_data(self):
        # Load dump data
        data_file = os.path.join(self.base_path, 'data.p')
        data = pickle.load(open(data_file, 'rb'))
        
        self.stems = data['stems']
        self.idf_vector = data['idf_vector']

    def load_training_data(self):
        data_path = os.path.join(self.base_path, 'data')
        category_id = 0
        for category in Path(data_path).iterdir():

            # Convert path to posix notation
            category_name = category.as_posix().split('/')[-1]
            self.categories.append(category_name)

            files = []

            for filepath in category.iterdir():
                files.append({
                        'path' : filepath.as_posix(),
                        'category_id' : category_id
                    })

            self.train_data.extend(random.sample(files, self.doc_num))

            category_id += 1

    def train_test_split(self):
        # Shuffle the training data
        random.shuffle(self.train_data)

        # Seperate train and test data
        # self.test_data = self.train_data[-1000:]
        # self.train_data = self.train_data[:-1000]
    
    # Compute tf-idf and train classifier
    def train(self):
        if (not(self.stems)):
            raise Exception('Corpus info not available.')

        if (not(self.train_data)):
            raise Exception('Training data not selected')

        stems_size = len(self.stems)
        docs_size = len(self.train_data)

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
        for i,doc in enumerate(self.train_data):

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

        # Assign and train a SVM
        clf = svm.SVC()
        clf.fit(input_matrix,output_matrix.ravel())

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
        for i,stem in enumerate(self.stems):
            tf_idf_vector.append(tf_vector[i] * self.idf_vector[stem])

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

def main():
    var1 = NepClassifier()

    # print('Processing Corpus')
    # var1.process_corpus()
    
    # print('Loading Corpus Info')
    # var1.load_data()

    # print('Loading Training Data')
    # var1.load_training_data()

    # print('Splitting data in train and test')
    # var1.train_test_split()

    # print('Training SVM')
    # var1.train()

    print('Loading Classifier')
    var1.load_clf()
    
    test_file = open('test_ent.txt', 'r')
    content = test_file.read()

    print('Predicting class')
    cls = var1.predict(content)    
    print(cls)

if __name__ == '__main__':
    main()
