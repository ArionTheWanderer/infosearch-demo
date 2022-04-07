import os

directory_docs = "lemmas-tf-idf"

for filename in os.listdir(directory_docs):
    file_path = os.path.join(directory_docs, filename)
    # проверка на тип
    if os.path.isfile(file_path):
        print(filename)
        print(file_path)
