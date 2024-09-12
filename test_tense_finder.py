# test_tense_finder.py
from TenseFinder.TenseParser import TenseParser

text = "I shall go to market."
parser = TenseParser()
result = parser.find_tense_simple_form_str(text)
print(result)

'''from TenseFinder.TenseParser import TenseParser

text = "I shall go to market. It was raining yesterday. She has been studying all day."
parser = TenseParser()
results = parser.parse(text)

for result in results:
    print(f"Sentence: {result['sentence']}")
    print(f"Tense: {result['tense']}")
    print()'''
