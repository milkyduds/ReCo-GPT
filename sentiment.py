import numpy
import spacy
import pandas as pd
from textblob import TextBlob
import json
#open venv: source myenv/bin/activate
nlp = spacy.load("en_core_web_sm")

class TextAnalyzer:
    def __init__(self):
        self.df = pd.read_csv('newsletter_data.csv')
        self.total_files = len(self.df['text'])
        self.text = "".join(self.df['text'][0:self.total_files])


    def analyze_sentiment(self):
        blob = TextBlob(self.text)
        sentiment = blob.sentiment
        return sentiment

    def analyze_style(self):
        doc = nlp(self.text)
        #Extracting writing style feature
        words = [token for token in doc if not token.is_punct and not token.is_space]
        style_features = {
            'avg_num_sentences': len(list(doc.sents)) / self.total_files,
            'avg_num_tokens': len(words) / self.total_files,
            'avg_words_per_sentence' : len(words) / len(list(doc.sents)),
            'avg_token_length': sum(len(token) for token in words) / len(words) if words else 0,
            'avg_num_nouns': sum(1 for token in words if token.pos_ == "NOUN") / self.total_files,
            'avg_num_verbs': sum(1 for token in words if token.pos_ == "VERB") / self.total_files,
            'avg_num_adjectives': sum(1 for token in words if token.pos_ == "ADJ") / self.total_files,
            'avg_num_adverbs': sum(1 for token in words if token.pos_ == "ADV") / self.total_files,
            'avg_num_unique_words': len(set(token.text for token in words)) / self.total_files,
        }
        return style_features

    def main(self):
        sentiment = self.analyze_sentiment()
        style = self.analyze_style()

        # Creating a dictionary to store the results
        results = {
            "sentiment": {
                "polarity": numpy.round(sentiment.polarity, 3),
                "subjectivity": numpy.round(sentiment.subjectivity, 3)
            },
            "writing_style": {
                feature: numpy.round(value, 3) for feature, value in style.items()
            }
        }

        # Saving the results to a JSON file
        with open('analysis_results.json', 'w') as json_file:
            json.dump(results, json_file, indent=4)  # Saving results in pretty JSON format

        # Also print the results to the console
        print("\nSentiment Analysis:")
        print(f"Polarity: {results['sentiment']['polarity']}")
        print(f"Subjectivity: {results['sentiment']['subjectivity']}")

        print("\nWriting Style Analysis:")
        for feature, value in results["writing_style"].items():
            print(f"{feature}: {value}")

if __name__ == "__main__":
    analyzed_text = TextAnalyzer()
    analyzed_text.main()
