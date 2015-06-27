import re

# Global variable
stems=None

suffixes = {
    1: ['छ', 'ा', 'न', 'ए', 'े', 'ी', 'ि', 'ै', 'ई', 'ओ', 'उ'],
    2: ['ले', 'को', 'का', 'की', 'ँछ', 'छु', 'छे', 'छौ', 'ने', 'यो', 'दा', 'दै', 'नु', 'एँ', 
        'ेँ', 'छौ', 'तै', 'थे', 'औं', 'ौं', 'यौ', 'ला', 'ली', 'मा', 'उँ', 'ुँ', 'ेर', 
        'एर', 'ाइ', 'आइ', 'इन', 'कै', 'ता', 'दो', 'ाए', 'ना', 'ौँ', 'िक','ाइ','ाउ'],
    3: ['हरू', 'लाई', 'बाट', 'एका', 'ँछु', 'इने', 'ँदै', 'छौँ', 'छस्', 'छन्', 
        'थेँ', 'एस्', 'ेस्', 'ओस्', 'ोस्', 'उन्', 'ुन्', 'एन्', 'ेन्', 'यौं', 'इस्', 'िस्',
        '्नो', 'साथ', 'नन्', 'िया', 'झैँ', 'न्छ', 'ेका', 'एको', 'ेको', 'शील', 'सार', 'ालु',
        'ईन्', 'ीन्', 'िलो', 'ाडी'],
    4: ['छेस्', 'छ्यौ', 'ँछन्', 'छिन्', 'थ्यौ', 'थिन्', 'औंला', 'ौंला', 'लिन्', 'लान्', 
        'लास्', 'लिस्', 'होस्', 'माथी', 'तर्फ', 'मुनि', 'पर्छ', 'ियाँ', 'न्छौ', 'सम्म', 
        'ाएको', 'सुकै', 'यालु', 'डालु', 'उँला', 'ुँला'],
    5: ['थ्यौँ', 'स्थित', 'तुल्य', 'चाँहि', 'चाहीँ', 'मात्र', 'न्छन्', 'न्छस्', 'मध्ये'],
    6: ['पालिका', 'अनुसार', 'न्छ्यौ', 'न्छेस्', 'न्छिन्', 'इन्जेल', 'िन्जेल', 'ुन्जेल', 'उन्जेल'],
    7: []
}

# Read stems from file
def read_stems():
    # Reads the word stems
    file=open('word_stem.txt')
    lines=file.readlines()
    file.close()

    # Constructing stems set
    _stems=set()
    for line in lines:
        new_line=line.replace('\n','')
        stem=new_line.split('|')[0]
        _stems.add(stem)

    return(_stems)

# Removes suffix
def remove_suffix(word):
    for L in 2,3,4,5,6,7:
        if len(word) > L + 1:
            for suf in suffixes[L]:
                if word.endswith(suf):
                    return word[:-L]
        else:
            break
    return word

# Tokenizes the given text
def tokenize(text):
    # Removing unnecessary items
    remove_exp= re.compile("[\d]+")
    removed_text= remove_exp.sub("",text)

    # Extracting words from text
    # Splits complex combinations in single step
    extract_exp= re.compile("[\s।|!?.,:;%+\-–*/'‘’“\"()]+")
    words= extract_exp.split(removed_text)

    # Returns the non-empty items only
    return([word for word in words if word!=''])

# Returns the stem
def stem(word):
    word_stem=remove_suffix(word)
    if(word_stem in stems):
        return word_stem
    else:
        return word

# Returns stems list
def get_stems(text):
    # Obtain tokens of the text
    tokens=tokenize(text)

    return([stem(token) for token in tokens])

# Returns known stems list
def get_known_stems(text):
    # Obtain tokens of the text
    tokens=tokenize(text)

    # Obtain the stem list
    stems_list=[stem(token) for token in tokens]

    # Returns known stem list
    return([stem for stem in stems_list if stem in stems])

stems=read_stems()

if __name__ == '__main__':
    stems=get__stems("""  पिट्सवर्ग (बीबीसी), कार्तिक २३ - अमरिकाको न्युरोसाइन्टिस्ट ६६ वर्षे रबर्ट फेर्रान्टेलाई पत्नी हत्याको लागि दोषी ठहर 
        गरिएको छ । पिट्सवर्ग विश्वविद्यालयका पूर्व शोधकर्ता फेर्रान्टेमाथि ४१ वर्षीया डा. अटमन क्लेनलाई पेय पदार्थमा साइनाइड खुवाएर 
        मारेको अभियोग थियो । उनी न्युरोलोजिस्ट थिइन् । श्रीमतीले अर्को शिशु जन्माउनलाई दबाब दिन थालेपछि उनले हत्याको षड्यन्त्र 
        रचेका थिए । फेर्रान्टेलाई आजीवन कारावास हुन सक्छ । पिट्सवर्ग अदालतमा उनी दोषी भएको फैसला सुनाएपछि क्लेनका आफन्त रोएका थिए । 
        'अटमनले न्याय पाइन्,' आमा लुइस क्लेनले अदालत बाहिर भनिन् । सोचीविचारी हत्या गरेको अभियोगमा उनलाई दोषी ठहराउनुअघि अदालतले 
        करिब दुई दिनको समयावधिमा १५ घन्टा विचार विमर्श गरेका थिए । प्रहरीको अनुसार फेर्रान्टेले सन् २०१३ को १७ अपि्रलमा श्रीमतीलाई
        उक्त विष खुवाएका थिए । यसको तीन दिनपछि क्लेनको मृत्यु भएको थियो । उनले विष खुवाएको आरोपको खण्डन गरेका थिए । श्रीमती बिरामी 
        हुनु दुई दिनअघि विश्वविद्यालयको क्रेडिट कार्डले उनले २ सय २० ग्रामभन्दा बढी साइनाइड किनेको प्रहरीको अनुसन्धानमा खुल्यो । 
        फेर्रान्टेले स्टेम सेल -शरीरको विशेष खाले कोष) प्रयोगको लागि साइनाइड किनेको दाबी गरे । पत्नी क्लेनको रगत जाँचमा शरीरमा
        अत्यधिक परिमाणमा साइनाइड फेला परेको थियो ।  """)
    
    print(stems)