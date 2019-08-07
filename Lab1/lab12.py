import split
import operator

def readFile(fileIn):
    content=""
    for line in fileIn :
        content+=line

    return content

def wordCount(contents):
    wordcount={}
    for word in split.tsplit(contents,(' ','.','!',',','"','\n','?')):
        if word != '':
            if word not in wordcount:
                wordcount[word] = 1
            else:
                wordcount[word] += 1

    return wordcount

def topTenWords(wordcount):
    print('\n\nTop 10 words are : ')
    wordcountS = sorted(wordcount.items(), key=operator.itemgetter(1),reverse=True)
    for x in range(10):
        print(wordcountS[x][0],wordcountS[x][1])

def topTenExcept(wordcount):
    stop=list(('a','about','above','after','again','against','all','am','an','and','any','are','as','at','be','because','been','be','for','being','below','the','both','but','by','could','did','do','does','doing','down','during','each','few','for','from','further','had','has','have','having','he','she','her','here','of','in','was','to'))
    print('\n\nTop 10 words after removing stop words are : ')
    wordcountS = sorted(wordcount.items(), key=operator.itemgetter(1),reverse=True)
    x=0
    c=0
    while c < 10 :
        if wordcountS[x][0] not in stop: 
            print(wordcountS[x][0],wordcountS[x][1])
            c+=1
        x+=1

def main():
    fileIn= open("sample.txt", "r")
    contents= readFile(fileIn)
    wordcount= wordCount(contents)
    for key in wordcount :    
        print(key,wordcount[key])
    topTenWords(wordcount)
    topTenExcept(wordcount)
    
if __name__== "__main__":
    main()
