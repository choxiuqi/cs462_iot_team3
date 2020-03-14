import json

def getjson(data):
    with open('output.csv', 'w') as f1:
        json.dump(data, f1)