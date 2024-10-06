"""
This module contains the AnswerService class, responsible for processing
essays and queries to provide relevant answers using text embedding 
models. It utilizes the TextPreProcessor for parsing the essay and the 
Encoder class for embedding the queries and essay sentences.
"""

import sys
import os
from typing import List, Dict

from .encoder import Encoder
from .text_pre_processor import TextPreProcessor

build_path = os.path.join(os.path.dirname(__file__), 'sentence_embedding/build')
sys.path.append(build_path)

from sentence_embedding import SentenceEmbedding  # type: ignore

class AnswerService:
    """
    A service class for processing essays and queries. It uses a 
    pre-trained SentenceTransformer model to encode the essay and 
    queries, providing answers based on subtitle or overall similarity.

    Methods:
        answer_questions_detailed: Returns detailed answers with 
        similarity scores. 
        answer_questions: Returns a simple list of best answers for 
        each query.
        get_best_subtitles: Finds the best-matching subtitles for the 
        queries.
        answer_based_on_subtitle: Answers queries by finding the 
        best-matching subtitles and sentences in the essay.
    """

    def answer_questions_detailed(
            self,
            essay: str,
            queries: List[str]
        ) -> Dict[str, tuple[str, float]]:
        """
        Provides detailed answers to the queries, returning the most 
        similar sentence from the essay with its similarity score.

        Args:
            essay (str): The full essay text.
            queries (List[str]): A list of queries (sentences) to find 
            answers for.

        Returns:
            Dict[str, tuple[str, float]]: A dictionary where keys are 
            queries, and values are tuples containing the most similar 
            sentence from the essay and its similarity score.
        """

        preprocessor = TextPreProcessor(essay)
        essay_sentences: List[str] = preprocessor.get_text_body()

        encoder: Encoder = Encoder()
        embedded_queries: List[SentenceEmbedding] = encoder.encode_string_list(queries)
        embedded_essay_sentences: List[SentenceEmbedding] = encoder.encode_string_list(
            essay_sentences
        )
        if not embedded_essay_sentences:
            return {}

        answers: Dict[str, tuple[str, float]] = {}
        for query in embedded_queries:
            index, similarity = query.most_similar(embedded_essay_sentences)
            current_answer: str = embedded_essay_sentences[index].get_sentence()
            answers[query.get_sentence()] = (current_answer, similarity)

        return answers

    def answer_questions(self, essay: str, queries: List[str]) -> List[str]:
        """
        Provides simple answers to the queries, returning the most 
        similar sentence for each query.

        Args:
            essay (str): The full essay text.
            queries (List[str]): A list of queries (sentences) to find 
            answers for.

        Returns:
            List[str]: A list of the most similar sentences from the 
            essay.
        """

        detailed_answers: Dict[str, tuple[str, float]] = self.answer_questions_detailed(
            essay,
            queries
        )

        answers: List[str] = []
        for query, (answer, similarity) in detailed_answers.items():
            answers.append(answer)

        return answers

    def get_best_subtitles(
        self,
        essay: str,
        queries: List[str]
    ) -> Dict[str, tuple[str, float]]:
        """
        Finds the best-matching subtitles in the essay for each query.

        Args:
            essay (str): The full essay text.
            queries (List[str]): A list of queries to find the best 
            matching subtitles.

        Returns:
            Dict[str, tuple[str, float]]: A dictionary where keys are 
            queries, and values are tuples containing the best matching 
            subtitle and its similarity score.
        """

        preprocessor: TextPreProcessor = TextPreProcessor(essay)
        essay_subtitles: List[str] = preprocessor.get_subtitles()

        encoder: Encoder = Encoder()
        embedded_queries: List[SentenceEmbedding] = encoder.encode_string_list(queries)
        embedded_essay_subtitles: List[SentenceEmbedding] = encoder.encode_string_list(
            essay_subtitles
        )
        if not embedded_essay_subtitles:
            return {}

        best_subtitles: Dict[str, tuple[str, float]] = {}
        for query in embedded_queries:
            index, similarity = query.most_similar(embedded_essay_subtitles)
            current_best_subtitle: str = embedded_essay_subtitles[index].get_sentence()
            best_subtitles[query.get_sentence()] = (current_best_subtitle, similarity)

        return best_subtitles

    def answer_based_on_subtitle(self, essay: str, queries: List[str]) -> List[str]:
        """
        Provides answers to queries by finding the best-matching 
        subtitle to the query and then finding the sentence that best 
        matches the query in the paragraph corresponding to that 
        subtitle. If the text contains only subtitles, an empty list is 
        returned.

        Args:
            essay (str): The full essay text.
            queries (List[str]): A list of queries to find answers for.

        Returns:
            List[str]: A list of the most similar sentences from the 
            essay based on the best matching subtitles.
        """

        preprocessor: TextPreProcessor = TextPreProcessor(essay)

        if preprocessor.is_text_only_subtitles():
            return []

        encoder: Encoder = Encoder()
        embedded_queries: List[SentenceEmbedding] = encoder.encode_string_list(queries)

        best_subtitles: Dict[str, tuple[str, float]] = self.get_best_subtitles(
            essay,
            queries
        )

        preprocessed_essay: Dict[str, List[str]] = preprocessor.preprocess_text()
        best_answers: Dict[str, tuple[str, float]] = {}

        for query in embedded_queries:
            best_subtitle_for_query = best_subtitles[query.get_sentence()][0]
            paragraph: List[str] = preprocessed_essay[best_subtitle_for_query]

            embedded_paragraph: List[SentenceEmbedding] = encoder.encode_string_list(
                paragraph
            )

            index, similarity = query.most_similar(embedded_paragraph)
            current_best_answer: str = embedded_paragraph[index].get_sentence()
            best_answers[query.get_sentence()] = (current_best_answer, similarity)

        answers: List[str] = []
        for query, (answer, similarity) in best_answers.items():
            answers.append(answer)

        return answers