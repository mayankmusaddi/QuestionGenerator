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
                    # print(">> ",str(text))
                    if str(text).endswith('.') or str(text).endswith('!') or str(text).endswith('?') or str(text).endswith(';'):
                        newpara+=str(text)
                        # print(":: ")
                if newpara != '':
                    # print(">>> ",newpara)
                    final+=newpara+"\n"
    return final

print(processText('chemistry_data/5.txt'))