from stop_words import get_stop_words
import config
import emoji
import pymorphy2
import requests

extrasymb = ['-', '!', '?', '(', ')', '[', ']', ',', '.', '\n']

morph = pymorphy2.MorphAnalyzer()
stop_words = get_stop_words('ru')

def get_wall(owner_id: str='',
    domain: str='',
    offset: int=0,
    count: int=10,
    filter: str='owner',
    extended: int=0,
    fields: str='',
    v: str='5.103'):
    code = ("return API.wall.get({" +
        f"'owner_id': '{owner_id}'," +
        f"'domain': '{domain}'," +
        f"'offset': {offset}," +
        f"'count': {count}," +
        f"'filter': '{filter}'," +
        f"'extended': {extended}," +
        f"'fields': '{fields}'," +
        f"'v': {v}," +
    "});")
    response = requests.post( url="https://api.vk.com/method/execute", data={
                "code": code,
                "access_token": config.access_token,
                "v": config.v})
    list = []
    for i in range(10):
        list.append(response.json()['response']['items'][i]['text'])
    return list

def links(text):
    if "http" in text:
        a = text.index("http")
        b = a
        while a < len(text) and text[a] != " ":
            a += 1
        text = text[:b] + text[a:]
        links(text)
    return text

def emojis(text):
  return ''.join(c for c in text if not c in emoji.UNICODE_EMOJI)

def stopword(text):
    for char in extrasymb:
        text = text.replace(char, " ")
    text = text.split()
    return " ".join([word for word in text if not word in stop_words])

def redact(text):
    text = links(emojis(stopword(text)))
    return [morph.parse(word)[0].normal_form for word in text.split()]

def redact_finish(domain):
    posts = get_wall(domain)
    posts_texts = []
    for i in range(len(posts)):
        reday = redact(posts[i])
        posts_texts.append(reday)
    return posts_texts
