import random
import pickle
from math import log
from pathlib import Path

import numpy as np

from . import stemmer

# Categories index
categories=['business','entertainment','news','politics','sports']

class doc_classifier():
    """ Class to perform the classification of nepali news """
    def __init__(self):
        self.datapath='data'

        self.documents=[]

        # Size of training matrix
        self.docs_size=1000
        self.max_stems=4000
        self.stems_size=0

        # Stems to use as feature
        self.stems=None

        # Assign a SVM classifier
        from sklearn import svm
        self.clf=svm.SVC()

    # Obtain necessary data
    def loadDocuments(self):
        for category in Path(self.datapath).iterdir():

            # Convert path to posix notation
            category_name=category.as_posix().split('/')[1]

            for filepath in category.iterdir():
                self.documents.append({
                    'path':filepath.as_posix(),
                    'category_id':categories.index(category_name)
                    })

        # Obtain relevant stems
        stems_dict={}
        for doc in random.sample(self.documents,self.docs_size):

            file=open(doc['path'],'r')
            content=file.read()
            file.close()

            # Obtain known stems
            known_stems=stemmer.get_known_stems(content)

            # Add the count of stems
            for stem in known_stems:
                stems_dict[stem]=stems_dict.get(stem,0)+1

        from operator import itemgetter
        stem_tuple=sorted(stems_dict.items(), key=itemgetter(1), reverse=True)[10:self.max_stems+10]

        self.stems=[item[0] for item in stem_tuple]

        self.stems_size=len(self.stems)

    # Compute tf-idf and train classifier
    def train(self):
         # tf matrix
        tf_matrix=np.ndarray((self.docs_size,self.stems_size),dtype='float16')

        # Training matrix
        train_matrix=np.ndarray((self.docs_size,self.stems_size),dtype='float16')
        output_matrix=np.ndarray((self.docs_size,1),dtype='float16')

        occur_dict={}
        init_doc_vector={}

        for stem in self.stems:
            occur_dict[stem]=0
            init_doc_vector[stem]=0

        # Use a sample of documents
        for i,document in enumerate(random.sample(self.documents,self.docs_size)):

            file=open(document['path'],'r')
            content=file.read()
            file.close()

            # Assign the initial vector
            doc_vector=init_doc_vector

            # Find stems in document
            doc_stems=stemmer.get_known_stems(content)

            # Obtain known stems set
            known_stems=set(doc_stems)

            # Add their occurances
            max_count=1
            for stem in known_stems:
                occur_dict[stem]=occur_dict.get(stem,0)+1
                count=doc_stems.count(stem)            
                doc_vector[stem]=count
                if(count>max_count):
                    max_count=count

            # Compute the tf and append it
            tf_matrix[i,:]=0.5+0.5/max_count*np.array([doc_vector[stem] for stem in self.stems])

            output_matrix[i,0]=document['category_id']

        self.occur_vector=occur_dict
        idf_matrix=np.array([log(self.docs_size/(1+x)) for x in [occur_dict[stem] for stem in self.stems]])

        # Element wise multiplication
        for i in range(self.docs_size):
            train_matrix[i,:]=tf_matrix[i,:] * idf_matrix

        # Train the SVM
        self.clf.fit(train_matrix,output_matrix.ravel())

        # Dumping extracted data
        data={
        'clf':self.clf,
        'stems':self.stems,
        'occur_vector':self.occur_vector,
        }

        pickle.dump(data,open('data.p','wb'))

    # Loads data from file
    def loadData(self):
        if(not(self.stems)):
            data=pickle.load(open('data.p','rb'))

            self.clf=data['clf']
            self.stems=data['stems']
            self.occur_vector=data['occur_vector']

    # Compute tf-idf for a text
    def tfidfvector(self,text):
        # Makes sure the data is present
        self.loadData()

        # Find stems in document
        doc_stems=stemmer.get_known_stems(text)

        # Obtain known stems set
        known_stems=set(doc_stems)

        doc_vector={}
        for stem in self.stems:
            doc_vector[stem]=0

        for stem in known_stems:
            doc_vector[stem]=doc_stems.count(stem)

        doc_vector_list=[doc_vector[stem] for stem in self.stems]

        max_count=max(doc_vector_list)

        tf_vector=[0.5+0.5/max_count*x for x in doc_vector_list]

        tf_idf_vector=[]
        for i,stem in enumerate(self.stems):
            tf_idf_vector.append(tf_vector[i]*self.occur_vector[stem])

        return(tf_idf_vector)

    # Predict the class
    def predict(self,text):
        # Makes sure the data is present
        self.loadData()

        tf_idf_vector=self.tfidfvector(text)

        id=int(round(self.clf.predict(tf_idf_vector)[0]))
        return (categories[id])

if __name__ == '__main__':
    var1=doc_classifier()
    print('Obtaining documents')
    var1.loadDocuments()

    print('Training SVM')
    var1.train()

    print('Predicting class')
    cls=var1.predict(""" इलाम, असार ८ - दूध बिक्री गरेर गुजारा चलाउँदै आएका यहाँका सर्वसाधारण/कृषक आफैं दुग्ध प्रशोधन कारखाना खोलेर मालिक बन्न थालेका छन् । व्यावसायिक गाईपालनमा कृषकको आकर्षण थपिएसँगै अधिक आम्दानी गर्ने उद्देश्यले दूधजन्य उद्योग खुल्ने क्रम बढेको हो । कृषकले दूधबाट घिउ, छुर्पी, चिज, ललिलपलगायत सामग्री आफैं उत्पादन गरेर बिक्री गर्ने क्रम बढेको हो । दूध बिक्रीबाट लगानीअनुसार आम्दानी हुन छाडेपछि कृषक आफैंले उद्योग सञ्चालनका लागि पहल थालेका हुन् ।
    जिल्लामा १ सय १२ वटा डेरी उद्योग छन् । दर्ता हुन बाँकी डेरी उद्योग पनि उल्लेख्य छन् । हरेकले दैनिक ५० देखि ५ सय लिटरसम्म दूध प्रशोधन गर्छन् । संस्थानअन्तर्गतका तीनबाहेक २४ वटा चिज कारखाना सञ्चालनमा आएका छन् । हरेक कारखानाले दैनिक १ हजारदेखि २ हजार लिटर दूध जम्मा गर्छन् । दैनिक २ सयदेखि ७ सय लिटरसम्म दूध संकलन गरेर प्रशोधन गर्ने नौवटा ललिपप उद्योग खोलिएका छन् ।
    आफैं प्रशोधन उद्योग खोलेर सञ्चालन गर्दा स्थानीय बासिन्दालाई रोजगारी दिन सकिने र आम्दानी पनि राम्रो हुने व्यवसायीको भनाइ छ । धेरैले सानातिना डेरी उद्योग सञ्चालनका लागि लगानी बढाएका छन् । ‘अमेरिकामा छुर्पी निर्यात हुने र घिउको मूल्य राम्रो पाइने भएकाले मिहिनेतअनुसार कमाइ गर्न सकिएको छ,’ माई मझुवाका दिलीप राईले भने । गाउँगाउँ पुगेर नै व्यपारीहरूले घिउ र छुर्पी ४ सय रुपैयाँ प्रतिकिलोभन्दा धेरैले खरिद गर्ने गरेका छन् ।
    जिल्ला पशुसेवा कार्यालयले दैनिक ३ लाख ३६ हजार लिटर दूध उत्पादन हुने जानकारी दियो । त्यसमध्यै घरायसी प्रयोजनमा खर्च हुने दैनिक डेढ लाख लिटर दूधबाहेक सबै बिक्री हुन्छ । बिक्री हुने २ लाख लिटर दूधमध्ये ठूलो हिस्सा स्थानीयस्तरमा खुलेका उद्योगमा खपत हुने गरेको छ ।
    यसअघि दैनिक ४० देखि ५० हजार लिटरसम्म दूध विराटनगरस्थित दुग्ध वितरण आयोजनामा जाने गरे पनि यो क्रम घटेको छ । कृत्रिम गर्भाधानबाट उन्नत गाईको संख्या बढेसँगै दूधको उत्पादन पनि बढ्दै गएको हो । आफ्नै उद्योग सञ्चालन गर्ने कृषकका लागि उपकरण खरिद, डेरी प्रवद्र्धन, नश्ल सुधारलगायत विषयमा पशु सेवा कार्यालयले सहयोग पुर्‍याउने गरेको छ । निजी उद्योगको वृद्धिसँगै चिस्यान केन्द्र पनि समुदायिकस्तबाट खुल्ने क्रम बढ्दो छ । समुदायस्तरबाट जिल्लामा आठवटा चिस्यान केन्द्र सञ्चालनमा छन् । संस्थानअन्तर्गत पनि आठवटा चिस्यान केन्द्र छन् ।
    चिज कारखानामा आकर्षण बढ्दो नेपालकै सहरहरूमा राम्रो बजार विस्तार भएपछि चिज कारखानाप्रति कृषकको आकर्षण धेरै छ । बाक्लै खुलेका चिज कारखानाले यो वर्ष १८ करोड रुपैयाँबराबरको चिज उत्पादन गरी बिक्री गरेका छन् । संस्थानअन्तर्गत रक्से, नयाँबजार, देउराली र पशुपतिनगरमा चिज कारखाना सञ्चालित छन् । बाँकी २० वटा कारखाना निजीस्तरबाट सञ्चालित छन् । त्यस्तै निजी क्षेत्रबाट सूर्योदय नगरपालिका, लक्ष्मीपुर, नयाँबजार, सुलुबुङलगायतमा कारखाना सञ्चालित छन् ।
    संस्थान र निजी सबै कारखानाले ५ लाख १ हजार किलो चिज उत्पादन गरेका हुन् । वार्षिक रूपमा ४५ लाख लिटरभन्दा धेरै दूध चिज निर्माणमा खपत हुन्छ । ‘चिजलाई मनपराउने स्वदेशी र विदेशीको संख्या बढेकै कारण माग धेरै छ,’ चिज उत्पादक व्यवासायी संघका अध्यक्ष आङरता शेर्पाले भने, ‘राजधानीलागयत प्रमुख सहरमै अधिकांश चिज खपत हुने गरेको छ ।’ औसत ४० रुपैयाँ प्रतिलिटर दूधको मूल्य दिने कारखानाले प्रतिकलो ६ सय रुपैयाँको हाराहारीमा चिज बिक्री गर्छन् । गुणस्तरीय चिज उत्पादनका लागि सम्बन्धित पक्षबाट प्राविधिक ज्ञान र आवश्यक सहयोग पर्याप्त नभएको व्यवसायीको गुनसो छ । जिल्लाका चिजलगायत दुग्धजन्य उद्योगमा वार्षिक ४८ करोडभन्दा बढीको कारोबार हुने गरेको पशु सेवा कार्यालयको तथ्यांक छ । """)    
    print(cls)