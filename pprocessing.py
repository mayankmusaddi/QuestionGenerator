import os
from textblob import TextBlob
def read_data(file_path):
    file = open(file_path, 'r')
    text = file.read()
    return text

toRemove = ['Table', '*', 'Fig', 'Activity', 'Figure', 'Problem', 'Fig.','Example','Answer']

def processText(file_path):
    text = read_data(file_path)
    paras = text.split('\n')
    paras = [i.strip() for i in paras]
    paras = list(filter(None, paras))
    # print(paras)
    final = ""
    for para in paras:
        c = 0
        for word in toRemove:
            if not word in para.split()[0]:
                c+=1
        if c is len(toRemove):
            if not para.split()[0].replace('.','').isdigit() and len(para.split()) > 5:
                blob_text = TextBlob(para)
                newpara = ''
                for text in blob_text.sentences:
                    if str(text).endswith('.') or str(text).endswith('!') or str(text).endswith('?') or str(text).endswith(';'):
                        newpara+=str(text)
                if newpara != '':
                    final+=newpara+"\n"
    return final


def preprocess(DirectoyPath):
    files = []
    for file in os.listdir(DirectoyPath):
        if file.endswith(".txt"):
            files.append(os.path.join(DirectoyPath, file))
    for file in files:
        data = processText(file)
        filename = file.replace(".txt", "_final")
        extension = ".txt"
        filename = filename + extension
        f = open(filename, "w")
        f.write(data)
        f.close()

if __name__ == "__main__":
    command = ''
    import sys
    from os import path
    if len(sys.argv) < 2:
        print("Please Enter a Directory Path")
        print("Usage: python3 pprocessing.py ''dirname''")
        sys.exit(1)
    else:
        command = sys.argv
        directorypath = sys.argv[1]
        # file_path = 'files/' + filename
        if (path.exists(directorypath) == False):
            print("Directory Does Not Exist")
        else:
            preprocess(directorypath)
