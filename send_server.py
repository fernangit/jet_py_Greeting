import requests

def send_utterance(url, utterance):
    print(url)
    print(utterance)
    payload = {'utterance':utterance}
    response = requests.post(url, data = payload)
    print(response)
    
if __name__ == '__main__':
    send_utterance('http://localhost:8000/StreamingAssets/Utterance', 'テスト')
