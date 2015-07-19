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

        # Number of documents for each class
        self.doc_num = 1000

        # Maximum stems to use
        self.max_stems = 2000

        # Stems to use as feature
        self.stems = None

        self.idf_vector = None

        # Classifier
        self.documents = []
        self.categories = []
        self.clf = None

    def process_corpus(self):
        # Vectors for stems
        stems_dict = {}
        idf_vector = {}        

        for root,dirs,files in os.walk(self.data_path):
            for file_pth in files:
                file_path = os.path.join(root, file_pth)
                abs_file_path = os.path.join(self.base_path, file_path)

                file = open(abs_file_path, 'r')
                content = file.read()
                file.close()

                # Obtain known stems
                doc_stems = stemmer.get_known_stems(content)
                doc_stems_set = set(doc_stems)

                # Add the count of stems
                for stem in doc_stems:
                    stems_dict[stem] = stems_dict.get(stem,0)+1

                for stem in doc_stems_set:
                    idf_vector[stem] = idf_vector.get(stem, 0)+1

        # Obtain frequently occuring stems
        stem_tuple=sorted(
            stems_dict.items(),
            key = itemgetter(1),
            reverse = True
        )[10 : self.max_stems+10]
    
        # Construct a ordered list of frequent stems
        stems = [item[0] for item in stem_tuple]
        idf_vector = {k:v for k,v in idf_vector.items() if k in stems}
        
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

            self.documents.extend(random.sample(files, self.doc_num))

            category_id += 1
   
    # Compute tf-idf and train classifier
    def train(self):
        if(not(self.stems)):
            raise Exception('Corpus info not available.')

        if(not(self.documents)):
            raise Exception('Training data not selected')

        stems_size = len(self.stems)
        docs_size = len(self.documents)

         # tf matrix
        tf_matrix = np.ndarray(
            (docs_size, stems_size),
            dtype = 'float16'
        )

        # Training matrix
        train_matrix = np.ndarray(
            (docs_size, stems_size),
            dtype='float16'
        )

        output_matrix = np.ndarray((docs_size,1), dtype = 'float16')

        # Use a sample of documents
        for i,doc in enumerate(self.documents):

            file = open(doc['path'], 'r')
            content = file.read()
            file.close()

            # Find stems in document
            doc_stems = stemmer.get_known_stems(content)

            # Obtain known stems set
            doc_stems_set = set(doc_stems)

            doc_vector = {}

            # Add their occurances
            max_count = 1
            for stem in doc_stems_set:
                count = doc_stems.count(stem)            
                doc_vector[stem] = count
                if(count > max_count):
                    max_count = count 

            # Compute the tf and append it
            tf_matrix[i, :] = 0.5+0.5/max_count*np.array(
                [doc_vector.get(stem,0) for stem in self.stems]
            )

            output_matrix[i,0] = doc['category_id']

        idf_matrix = np.array([
            log(docs_size/(1+x)) 
            for x
            in [self.idf_vector[stem] for stem in self.stems]
        ])

        # Element wise multiplication
        for i in range(docs_size):
            train_matrix[i,:] = tf_matrix[i,:] * idf_matrix

        # Assign and train a SVM
        clf = svm.SVC()
        clf.fit(train_matrix,output_matrix.ravel())

        data = {
            'categories' : self.categories,
            'clf' : clf,
        }

        # Dumping extracted data
        clf_file = os.path.join(self.base_path,'clf.p')
        pickle.dump(data,open(clf_file,'wb'))

    def load_clf(self):
        if(not(self.stems)):
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

        # Obtain known stems set
        doc_stems_set = set(doc_stems)

        # Document vector
        doc_vector = {stem:doc_stems.count(stem) for stem in doc_stems_set} 

        doc_vector_list = [doc_vector.get(stem,0) for stem in self.stems]

        max_count = max(doc_vector_list)
        if(max_count == 0):
            max_count = 1

        tf_vector = [0.5+0.5/max_count*x for x in doc_vector_list]

        tf_idf_vector = []
        for i,stem in enumerate(self.stems):
            tf_idf_vector.append(tf_vector[i]*self.idf_vector[stem])

        return(tf_idf_vector)

    # Predict the class
    def predict(self,text):
        if(not(self.clf)):
            raise Exception('Classifier not loaded')

        tf_idf_vector = self.tf_idf_vector(text)
        
        class_id = int(round(self.clf.predict(tf_idf_vector)[0]))
        return (self.categories[class_id])

if __name__ == '__main__':
    var1 = NepClassifier()

    print('Processing Corpus')
    # var1.process_corpus()
    
    print('Loading Corpus Info')
    # var1.load_data()

    print('Loading Training Data')
    # var1.load_training_data()

    print('Training SVM')
    # var1.train()

    print('Loading Classifier')
    var1.load_clf()

    print('Predicting class')
    cls = var1.predict(""" ३ साउन, कठमाडौं । समाजसेवी फुर्पा लामाले भूकम्प अतिप्रभावित जिल्लामा १५ लाख रुपैयाँ बराबरको सोलार बत्ति तथा अन्य राहत सामग्री वितरण गरेका छन् । लामाको व्यत्तिगत पहलमा विदेशमा रहेका साथी तथा संघसंस्थामार्फ उपलब्ध भएका विभिन्न राहत सामग्री वितरण गरेका हुन ।
                            उनले सिन्धुपाल्चोकको विभिन्न गाविसमा सोलार बत्ति, घर बनाउने जस्तापाता, त्रिपाललगायतका सामग्री वितरण गरेका हुन । लामाले अमेरिकन सोलर बत्ति भूकम्प अति प्रभावित जिल्लामा वितरण गर्दै आएका छन् । अहिलेसम्म उनले ७० थान सोलार, ८५ बन्डल जस्तापाता र ३० बन्डल त्रिपाल वितरण गरिसकेका हुन । उनले पहिलो चरणमा राहत स्वरुप त्रिपाल वितरण गरे । त्यसपछि बस्ने बास बनाउनका लागि जस्तापाता र अहिले विजुली बाल्नका लागि सोलार बाडेका हुन ।
                        जलबायु परिवर्तन सम्वन्धी काम गर्दै आएका लामाले गत बैशाख १२ पछिदेखि हालसम्म राहतका सामग्री निरन्तर बाड्दै आएका हुन । उनका अनुसार केही दिनमा दोलखा र नुवाकोटका केही विद्यालय तथा सार्वजनिक स्थलमा पनि सोलार राखिदिने छ । उक्त सोलार अमेरिकी एक संस्थासँग अर्डर गरिसकेको बताए । उक्त सोलारको प्रतिथान मूल्य ५० हजारदेखि ७० हजारसम्म पर्ने बताए । त्यसबाट १ सय ५० वाट विजुली निकाल्न सकिने क्षमताको छ । उनले हालसम्म रामेछाप, सिन्धुपाल्चोक, दोलखा, नुवाकोटलगायतका जिल्लामा विभिन्न सामग्री वितरण गरिसकेका छन् । यसैगरी भूकम्पबाट प्रभावित जिल्लामा मानिसलाई राहत स्वरुप रकम समेत उपलब्ध गराइसकेको छ । """)    
    print(cls)
