# test_tense_finder.py
from TenseFinder.TenseParser import TenseParser

text = "I shall go to market."
parser = TenseParser()
result = parser.parse(text)
print(result)
