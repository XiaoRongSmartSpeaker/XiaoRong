import json

def setup(data):
    data = json.loads(data)
    print(data)
    return True