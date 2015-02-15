import re
def tokenize(text):
   # Removing unnecessary items
   remove_exp= re.compile("[\d]+")
   removed_text= remove_exp.sub("",text)

   # Extracting words from text
   # Splits complex combinations in single step
   extract_exp= re.compile("[\s।|!?.,:;%+\-–*/'‘’“\"()]+")
   words= extract_exp.split(removed_text)

   # Removing empty words
   empty=words.count('')
   for i in range(0,empty):
       words.remove('')
   return(words)

if __name__=='__main__':
    file_r= open('ekantipur/business/397477.txt','r')
    text= file_r.read()
    arr=tokenize(text)
    str=" ".join(arr)
    file_w=open('dump.txt','w')
    file_w.write(str)
