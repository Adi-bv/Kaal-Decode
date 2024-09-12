# Define a dictionary to map emojis to words (reverse of text-to-emoji)
emoji_dict = {
    "😊": "happy",
    "😢": "sad",
    "❤️": "love",
    "😠": "angry",
    "🏃‍♂️": "running",
    "🍽️": "eating",
    "😴": "sleeping",
    "🕒": "time",
    "🌅": "morning",
    "🌙": "night",
    "☀️": "sun",
    "🌧️": "rain",
    "🎉": "party",
    "📖": "reading",
    "💻": "working",
    "✈️": "flying",
    "🚗": "driving",
    "🏫": "studying",
    "💼": "working",
    "🎶": "listening to music",
    "🔮": "predicting",
    "⌛": "waiting",
    "⏳": "present"
}

def convert_emoji_to_text(sentence):
    words = sentence.split()
    converted_sentence = ' '.join([emoji_dict.get(word, word) for word in words])
    return converted_sentence

# Function to convert emoji sequence to text
# def emoji_to_text(emoji_text):
#     words = emoji_text.split()  # Split the input into individual elements
#     text_output = []
   
#     for word in words:
#         # Check if the word (emoji) exists in the emoji_to_text_dict, else keep it unchanged
#         text_word = emoji_to_text_dict.get(word, word)
#         text_output.append(text_word)
   
#     return " ".join(text_output)

# # Example Usage
# input_emoji_text = "I am 😊 to 📖 a 📖 in the 🌅"
# text_sequence = emoji_to_text(input_emoji_text)
# print("Original Emoji Text:", input_emoji_text)
# print("Converted Text:", text_sequence)

