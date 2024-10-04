import spacy
from googletrans import Translator

class TenseParser:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')
        self.translator = Translator()

    def translate_to_english(self, text):
        """
        Translates the input text to English using Google Translate.
        """
        translated = self.translator.translate(text, dest='en')
        return translated.text

    def parse(self, text):
        """
        Translates the input text to English, splits it into sentences,
        and determines the tense of each sentence.
        """
        english_text = self.translate_to_english(text)
        doc = self.nlp(english_text)
        sentence_tenses = []

        for sentence in doc.sents:
            tense = self.identify_tense(sentence)
            sentence_tenses.append((sentence.text, tense))

        return sentence_tenses

    def identify_tense(self, doc):
        """
        Identifies the tense of the parsed sentence using Spacy's token attributes.
        """
        aux_verb = None
        main_verb = None
        is_present = False
        is_past = False
        is_future = False
        is_continuous = False
        is_perfect = False
        is_conditional = False

        # Iterate through tokens to find the main verb and auxiliaries
        for token in doc:
            if token.tag_ in ('VBP', 'VBZ', 'VBG', 'VBD', 'VBN', 'MD'):
                if token.tag_ in ('VBP', 'VBZ'):
                    is_present = True
                    main_verb = token
                elif token.tag_ == 'VBD':
                    is_past = True
                    main_verb = token
                elif token.tag_ == 'VBG':
                    is_continuous = True
                    main_verb = token
                elif token.tag_ == 'VBN':
                    is_perfect = True
                    main_verb = token
                elif token.tag_ == 'MD':
                    aux_verb = token
                    if token.lemma_ in ['will', 'shall']:
                        is_future = True
                    elif token.lemma_ in ['would', 'could', 'should', 'might', 'may']:
                        is_conditional = True

        # Determine tense based on identified tokens
        if is_conditional:
            if is_present and is_continuous:
                return "Conditional Present Continuous"
            elif is_present and is_perfect:
                return "Conditional Present Perfect"
            elif is_present:
                return "Conditional Present Simple"
            elif is_past and is_continuous:
                return "Conditional Past Continuous"
            elif is_past and is_perfect:
                return "Conditional Past Perfect"
            elif is_past:
                return "Conditional Past Simple"
            elif is_future:
                return "Conditional Future"
        elif is_future:
            if is_continuous:
                return "Future Continuous"
            elif is_perfect:
                return "Future Perfect"
            else:
                return "Future Simple"
        elif is_present and is_continuous:
            return "Present Continuous"
        elif is_present and is_perfect:
            return "Present Perfect"
        elif is_present:
            return "Present Simple"
        elif is_past and is_continuous:
            return "Past Continuous"
        elif is_past and is_perfect:
            return "Past Perfect"
        elif is_past:
            return "Past Simple"
        else:
            return "Unknown Tense"
