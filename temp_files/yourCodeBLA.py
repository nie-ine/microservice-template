# Your python 3 code goes here
import json

def show_message(json_file):
    with open(json_file, 'r') as f:
        content = json.load(f)

return content['message']

if __name__ == "__main__":
    print(show_message("yourData.json"))
