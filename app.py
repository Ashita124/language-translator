from flask import Flask, render_template, request
import re
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

languages = {'1': 'Arabic', '2': 'German', '3': 'English', '4': 'Spanish', '5': 'French', '6': 'Hebrew',
             '7': 'Japanese', '8': 'Dutch', '9': 'Polish', '10': 'Portuguese', '11': 'Romanian', '12': 'Russian',
             '13': 'Turkish'}

def response_function(input_data):
    user_agent = 'Mozilla/5.0'
    try:
        response = requests.get(f'https://context.reverso.net/translation/{languages[input_data[0]].lower()}-{languages[input_data[1]].lower()}/{input_data[2]}', headers={'User-Agent': user_agent})
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find translations and examples
        translations = [word.text.strip() for word in soup.find_all('a', class_='translation')]
        examples = [word.text.strip() for word in soup.find_all('div', class_='example')]
        
        # If translations are not found but examples are available, prioritize examples
        if not translations and examples:
            translations = ['Translations not directly available. See examples below.']
        
        return translations, examples
    except:
        return None, None



@app.route('/')
def index():
    return render_template('index.html', languages=languages)

@app.route('/translate', methods=['POST'])
def translate():
    if request.method == 'POST':
        language_from = request.form['language_from']
        language_to = request.form['language_to']
        word = request.form['word'].lower()

        translations, examples = response_function([language_from, language_to, word])

        if translations and examples:
            return render_template('translation_result.html', translations=translations, examples=examples)
        else:
            return "Error occurred while fetching translations."


@app.route('/faq')
def faq():
    return render_template('faq.html')

if __name__ == '__main__':
    app.run(debug=True)
