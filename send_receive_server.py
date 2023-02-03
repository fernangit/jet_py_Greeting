import requests

def send_utterance(url, utterance):
    print(url)
    print(utterance)
    payload = {'utterance':utterance}
    response = requests.post(url, data = payload)
    print(response)

def receive_utterance(url):
    print(url)
    utterance = requests.get(url).content.decode('cp932')
    print(utterance)
    return utterance

if __name__ == '__main__':
    send_utterance('http://localhost:8000/StreamingAssets/Utterance', 'テスト')
    utterance = receive_utterance('http://localhost:8000/StreamingAssets/Utterance/utter.txt')
    print(utterance)
