from flask import Flask, request, render_template, jsonify
from TenseFinder.TenseParser import TenseParser
from emoji import convert_emoji_to_text  # Import the emoji conversion function
from googletrans import Translator  # Import the Translator from googletrans
import os

app = Flask(__name__)

# Initialize the translator once, to be used across multiple requests
translator = Translator()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    sentence = request.form['sentence']
    
    # Convert emojis to text
    sentence = convert_emoji_to_text(sentence)
    
    parser = TenseParser()
    result = parser.parse(sentence)
    
    return jsonify({"tense": result})

@app.route('/predict-paragraph', methods=['POST'])
def predict_paragraph():
    data = request.get_json()
    paragraph = data.get('paragraph')
    
    # Convert emojis to text
    paragraph = convert_emoji_to_text(paragraph)
    
    # Translate paragraph to English
    translated = translator.translate(paragraph, dest='en')
    paragraph = translated.text
    
    parser = TenseParser()
    sentences = [sentence.strip() for sentence in paragraph.split('. ') if sentence.strip()]
    
    results = []

    for sentence in sentences:
        if sentence:
            sentence = sentence if sentence.endswith('.') else sentence + '.'
            tense = parser.parse(sentence)
            # Extract only the sentence and tense type
            tense_type = tense[0][1] if tense and isinstance(tense[0], tuple) else "Unknown Tense"
            results.append(f"{sentence} -> {tense_type}")

    return jsonify({
        "tenses": "\n".join(results),  # Return each sentence in a new line
        "translated_paragraph": paragraph
    })



if __name__ == '__main__':
    # app.run(debug=True)
    port = int(os.environ.get('PORT', 5000))  # Use the 'PORT' environment variable or default to 5000
    app.run(host='0.0.0.0', port=port)



