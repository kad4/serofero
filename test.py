import os
from tokenizer import tokenize

path='onlinekhabar/news'
files=os.listdir(path)

total_set=set()

for file in files:
    filepath=path+'/'+file
    file_ptr= open(filepath,'r')
    print('Processing file: ',file)
    file_text= file_ptr.read()
    tokens= tokenize(file_text)
    total_set=total_set.union(tokens)
    file_ptr.close()

print('Unique words: ',len(total_set))
file=open('unique_words.txt','w')
str='\n'.join(total_set)
file.write(str)
file.close()
