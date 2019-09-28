from textblob import TextBlob

def read_data(file_path):
    file = open(file_path, 'r')
    text = file.read()
    return text

filenames = ['dataset/chemistry_data/kech101.txt']

for filename in filenames:
    text = read_data(filename)
    to_be_removed = ['Table', '*', 'Fig', 'Activity', 'Figure', 'Problem', 'Fig.']
    paragraphs = text.split('\n\n')
    new = []
    for para in paragraphs:
        # print('===========', para.strip())
        flag = 0
        lines = para.split('\n')
        for line in lines:
            line = line.strip()
            first = ((line.split(' '))[0]).strip()
            if first == 'EXERCISES' or first == 'Exercises':
                flag = 1
                break
        if flag:
            break
        para = para.replace('\t', ' ')
        para = para.strip()
        first = ((para.split(' '))[0]).strip()
        if (first == 'Summary'):
            break
        if first not in to_be_removed:
            if ((first.replace('.', '')).isdigit()) == False:
                new.append(para)
                # print(para)
    newnew = []
    for para in new:
        cpy = ""
        lines = para.split('\n')
        for line in lines:
            first = ((line.split(' '))[0]).strip()
            if ((first.replace('.', '')).isdigit()) == False:
                cpy += '\n'
                cpy += line
        newnew.append(cpy)
        print(cpy)
