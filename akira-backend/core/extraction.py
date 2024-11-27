from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


class TopicExtractor:
    def __init__(self) -> None:
        nltk.download("punkt")
        nltk.download("stopwords")
        nltk.download("wordnet")
        nltk.download("averaged_perceptron_tagger")

        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words("english"))
        self.vectorizer = TfidfVectorizer(
            max_features=100, stop_words="english", ngram_range=(1, 2)
        )

    def preprocess_text(self, text):
        """Preprocess text for topic extraction"""
        # tokenize into sentences
        sentences = sent_tokenize(text)

        # processed text
        processed_sentences = []
        for sentence in sentences:
            # tokenize words
            tokens = word_tokenize(sentence.lower())

            tokens = [
                self.lemmatizer.lemmatize(token)
                for token in tokens
                if token.isalnum() and token not in self.stop_words and len(token) > 2
            ]

            if tokens:
                processed_sentences.append(" ".join(tokens))
        return processed_sentences

    def extract_topics(self, text, min_score_percentile=75):
        """
        Extract topics from text using TF-ID scores
        """
        processed_sentences = self.preprocess_text(text)
        if not processed_sentences:
            return []

        tfid_matrix = self.vectorizer.fit_transform(processed_sentences)
        feature_names = self.vectorizer.get_feature_names_out()

        avg_tfid_scores = np.mean(tfid_matrix.toarray(), axis=0)

        score_threshold = np.percentile(avg_tfid_scores, min_score_percentile)

        term_scores = list(zip(feature_names, avg_tfid_scores))
        signficant_terms = [
            term for term, score in term_scores if score >= score_threshold
        ]

        term_scores.sort(key=lambda x: x[1], reverse=True)
        topics = signficant_terms

        remaining_topics = [term for term, _ in term_scores if term not in topics]

        num_sentences = len(processed_sentences)
        min_topics = max(5, num_sentences // 10)

        if len(topics) < min_topics:
            additional_topics = [
                term for term in remaining_topics if term not in topics
            ][: min_topics - len(topics)]

        return topics

    def get_topic_scores(self, text):
        """
        Get topics with their tfid scores for analysis
        """

        processed_sentences = self.preprocess_text(text)
        if not processed_sentences:
            return []

        tfid_matrix = self.vectorizer.fit_transform(processed_sentences)
        feature_names = self.vectorizer.get_feature_names_out()
        avg_tfid_scores = np.mean(tfid_matrix.toarray(), axis=0)

        term_scores = list(zip(feature_names, avg_tfid_scores))
        term_scores.sort(key=lambda x: x[1], reverse=True)

        return term_scores
