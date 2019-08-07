def readFile(fileIn):
    content=""
    for line in fileIn :
        content+=line

    return content
while True:
    x=input('\nEnter:\n1 to copy\n2 to copy in reverse\n3 to quit\n')
    if x=='1' :
        fileIn=open("sample.txt","r")
        fileOut=open("output.txt","w")
        contents = readFile(fileIn)
        fileOut.write(contents)
        fileIn.close()
        fileOut.close()
        print('\nCopied Successfully!!')

    elif x=='3':
        break

    elif x=='2':
        fileO=open("outputReverse.txt","w")
        for line in reversed(list(open("sample.txt"))):
            fileO.write(line[::-1])

       

        fileO.close()




