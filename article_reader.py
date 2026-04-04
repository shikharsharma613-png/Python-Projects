import pyttsx3
import requests
from bs4 import BeautifulSoup

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

url = input("Enter URL: ")

res = requests.get(url)
soup = BeautifulSoup(res.text, 'html.parser')

articles = []
for p in soup.find_all('p'):
    articles.append(p.get_text().strip())

text = " ".join(articles)

print("Speaking...")
speak(text)