from docx import Document

# def read_data(file_path):
#     file = open(file_path, 'r')
#     text = file.read()
#     return text

filenames = ['./../physics_data/keph105.txt']

for filename in filenames:
	document = Document(filename)
	print(document)