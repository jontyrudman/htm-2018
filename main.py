import os
from util import *
from parser import *
from converter import *
from markov import *

def update_videos(username, password):
    get_wav(get_videos(username, password))
    for root, dirs, files in os.walk(os.getcwd()):
        for file in files:
            if file.endswith('.wav'):
                upload_blob("audioforhtm", file, file)

def extract_text():
    for blob in list_blobs("audioforhtm"):
        name = blob.name
        print(name)
        if not file_exists("transcriptforhtm", name+".txt"):
            transcribe_gcs(blob)
            upload_blob("transcriptforhtm", name+".txt", name+".txt")

def build_models():
    for blob in list_blobs("transcriptforhtm"):
        name = blob.name
        if not file_exists("modelsforhtm", name+".json"):
            output = open(name+'.json', 'w')
            output.write(markovify.Text(blob.download_as_string(), state_size=2).to_json())
            output.close()
            upload_blob("modelsforhtm", name+".json", name+".json")

def generate_model_combo():
    models = []
    for blob in list_blobs("modelsforhtm"):
        json = blob.download_as_string()
        model = markovify.Text.from_json(json)
        models.append(model)
    if len(models) == 0:
        return False
    model_combo = markovify.combine(models, [1 for i in range(len(models))])
    return model_combo

if __name__=='__main__':
#    username = raw_input("Username: ")
#    password = getpass.getpass("Password: ")
#    update_videos(username, password)
    #build_models()
    answer = 10
    while answer:
        print(
"""
[0] - exit
[1] - update videos
[2] - extract text
[3] - build models
[4] - create a sentence!!!

""")
        answer = input("Answer: ")
        if answer == "1":
            username = raw_input("Username: ")
            password = getpass.getpass("Password: ")
            update_videos(username, password)
        elif answer == "2":
            extract_text()
        elif answer == "3":
            build_models()
        elif answer == "4":
            model = generate_model_combo()
            if model == False:
                print("You need to generate models first!!!")
            else:
                print(model.make_sentence())
