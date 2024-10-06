"""
This module contains unit tests using pytest for the AnswerService 
class. The tests validate the behavior of the AnswerService class in 
handling queries, processing essays, and providing the most relevant 
answers.
"""

import os
import sys
from typing import List, Dict

import pytest

from answer_service.answer_service import AnswerService, Encoder

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
build_path = os.path.join(project_root, 'answer_service', 'sentence_embedding', 'build')
sys.path.append(build_path)

from sentence_embedding import SentenceEmbedding # type: ignore

class TestAnswerService:
    """
    Unit tests for the AnswerService class.

    The tests validate the correct functionality of processing essays 
    and queries, ensuring the right answers and subtitles are provided
    in various scenarios, including edge cases.
    """

    def test_get_best_answers(self) -> None:
        """
        Test get_best_answers to ensure detailed answers with
        similarity scores are returned for each query.

        Asserts:
            Correct detailed answers are returned in the expected 
            format.
        """
        essay: str = "This is the first sentence. This is the second sentence."
        queries: List[str] = [
            "What is the first sentence?",
            "What is the second sentence?"
        ]

        answer_service: AnswerService = AnswerService()
        answers: Dict[str, tuple[str, float]] = answer_service.get_best_answers(
            essay,
            queries
        )

        assert "What is the first sentence?" in answers

    def test_answer_questions(self) -> None:
        """
        Test answer_questions to ensure a list of answers is returned 
        for each query.

        Asserts:
            The length of returned answers matches the number of 
            queries.
        """
        essay: str = "This is the first sentence. This is the second sentence."
        queries: List[str] = [
            "What is the first sentence?",
            "What is the second sentence?"
        ]

        answer_service: AnswerService = AnswerService()
        answers: List[str] = answer_service.answer_questions(essay, queries)

        assert len(answers) == len(queries)

    def test_get_best_subtitles(self, encoder: Encoder) -> None:
        """
        Test get_best_subtitles to ensure the best matching subtitles 
        are returned for the queries.

        Asserts:
            Correct subtitles are matched to the queries.
        """
        essay: str = "Title\nThis is the content."
        queries: List[str] = ["What is the title?"]

        embedded_queries: List[SentenceEmbedding] = encoder.encode_string_list(queries)

        answer_service: AnswerService = AnswerService()
        best_subtitles: Dict[str, tuple[str, float]] = answer_service.get_best_subtitles(
            essay,
            embedded_queries
        )

        assert "Title" == best_subtitles["What is the title?"][0]

    def test_answer_questions_based_on_subtitle(self) -> None:
        """
        Test answer_questions_based_on_subtitle to ensure correct 
        answers are returned based on subtitles for each query.

        Asserts:
            Correct answers are returned based on subtitle matching.
        """
        essay: str = "Title\nThis is the content under the title. This is a sentence."
        queries: List[str] = ["What is under the title?"]

        answer_service: AnswerService = AnswerService()
        answers: List[str] = answer_service.answer_questions_based_on_subtitle(
            essay,
            queries
        )

        assert len(answers) == 1
        assert answers[0] == "This is the content under the title"

    def test_empty_essay(self) -> None:
        """
        Test the edge case where an empty essay is provided to ensure 
        the service handles it correctly by returning no answers.

        Asserts:
            No answers are returned for an empty essay.
        """
        essay: str = ""
        queries: List[str] = ["What is the first sentence?"]

        answer_service: AnswerService = AnswerService()
        answers: List[str] = answer_service.answer_questions(essay, queries)

        assert len(answers) == 0

    def test_empty_essay_based_on_subtitle(self) -> None:
        """
        Test the edge case where an empty essay is provided when trying 
        to get answers based on subtitle to ensure the service handles 
        it correctly by returning no answers.

        Asserts:
            No answers are returned for an empty essay.
        """
        essay: str = ""
        queries: List[str] = ["What is the first sentence?"]

        answer_service: AnswerService = AnswerService()
        answers: List[str] = answer_service.answer_questions_based_on_subtitle(
            essay,
            queries
        )

        assert len(answers) == 0

    def test_empty_queries(self) -> None:
        """
        Test the edge case where an empty list of queries is provided to
        ensure the service handles it correctly by returning no answers.

        Asserts:
            No answers are returned for empty queries.
        """
        essay: str = "This is the first sentence. This is the second sentence."
        queries: List[str] = []

        answer_service: AnswerService = AnswerService()
        answers: List[str] = answer_service.answer_questions(essay, queries)

        assert len(answers) == 0

    def test_subtitle_only_text(self) -> None:
        """
        Test the case where the text contains only subtitles to ensure
        no answers are returned if there is no content under the 
        subtitles.

        Asserts:
            No answers are returned if the text only contains subtitles.
        """
        essay: str = "Subtitle\nSubtitle2\n"
        queries: List[str] = ["What is subtitle?"]

        answer_service: AnswerService = AnswerService()
        answers: List[str] = answer_service.answer_questions_based_on_subtitle(
            essay,
            queries
        )

        assert len(answers) == 0

    def test_single_subtitle_answer_questions(self) -> None:
        """
        Test the case where the text contains a single subtitle to 
        ensure no answers are returned if there is no content under 
        the subtitle.

        Asserts:
            No answers are returned if the text only contains a single 
            subtitle.
        """

        essay: str = "Write your essay here."
        queries: List[str] = ["Write your query 1 here.", "Write your query 2 here."]

        answer_service: AnswerService = AnswerService()
        answers: List[str] = answer_service.answer_questions(essay, queries)

        assert answers == ["Write your essay here", "Write your essay here"]
        assert len(answers) == 2

    def test_full_essay_answer_questions(self) -> None:
        """
        Test the case where a full essay is provided to ensure the
        service returns the correct answers for each query.

        Asserts:
            Correct answers are returned for each query of a full essay.
        """

        with open('./tests/docs/full_essay.txt', 'r', encoding='utf-8') as file:
            full_essay: str = file.read()

        full_essay_query_1: str = "What is courage?"
        full_essay_query_2: str = "What is bravery?"
        full_essay_query_3: str = ("An example of a character in the literature who"
                              " displays courage"
                              )
        full_essay_query_4: str = ("An example of a character in the literature who"
                              " exhibits bravery"
                              )
        full_essay_query_5: str = "What risks a courageous act entails?"
        full_essay_query_6: str = "What risks a brave act entails?"

        full_essay_queries: List[str] = [
            full_essay_query_1,
            full_essay_query_2,
            full_essay_query_3,
            full_essay_query_4,
            full_essay_query_5,
            full_essay_query_6
        ]

        answer_service: AnswerService = AnswerService()
        answers: List[str] = answer_service.answer_questions(
            full_essay,
            full_essay_queries
        )

        path_to_expected_answers: str = './tests/docs/expected_answers_full_essay.txt'
        with open(path_to_expected_answers, 'r', encoding='utf-8') as file:
            expected_answers: List[str] = file.read().splitlines()

        assert all(answer in answers for answer in expected_answers)

    def test_get_best_answers_based_on_subtitle(self) -> None:
        """
        Test get_best_answers_based_on_subtitle to ensure detailed 
        answers with similarity scores are returned for each query 
        based on subtitle matching.

        Asserts:
            Correct detailed answers are returned in the expected 
            format.
        """

        essay: str = "Title\nThis is the content under the title. This is a sentence."
        queries: List[str] = ["What is under the title?"]

        answer_service: AnswerService = AnswerService()
        best_answers: Dict[str, tuple[str, float]] = (
            answer_service.get_best_answers_based_on_subtitle(essay, queries)
        )

        assert "What is under the title?" in best_answers
        answer: str = "This is the content under the title"
        assert best_answers["What is under the title?"][0] == answer

    def test_empty_queries_based_on_subtitle(self) -> None:
        """
        Test the edge case where an empty list of queries is provided 
        when trying to get answers based on subtitle to ensure the 
        service handles it correctly by returning no answers.

        Asserts:
            No answers are returned for empty queries.
        """

        essay: str = "This is the first sentence. This is the second sentence."
        queries: List[str] = []

        answer_service: AnswerService = AnswerService()
        best_answers: Dict[str, tuple[str, float]] = (
            answer_service.get_best_answers_based_on_subtitle(essay, queries)
        )

        assert len(best_answers) == 0

    def test_subtitle_only_text_for_get_best_answers_based_on_subtitle(self) -> None:
        """
        Test the case where the text contains only subtitles to ensure 
        no answers are returned if there is no content under the 
        subtitles when using get_best_answers_based_on_subtitle.

        Asserts:
            No answers are returned if the text only contains subtitles.
        """

        essay: str = "Subtitle\nSubtitle2\n"
        queries: List[str] = ["What is subtitle?"]

        answer_service: AnswerService = AnswerService()
        best_answers: Dict[str, tuple[str, float]] = (
            answer_service.get_best_answers_based_on_subtitle(essay, queries)
        )

        assert len(best_answers) == 0

    def test_get_best_subtitles_empty_essay(self) -> None:
        """
        Test get_best_subtitles with an empty essay to ensure the 
        service handles it correctly by returning no subtitles.

        Asserts:
            No subtitles are returned for an empty essay.
        """

        essay: str = ""
        queries: List[str] = ["What is the title?"]

        encoder: Encoder = Encoder()
        embedded_queries: List[SentenceEmbedding] = encoder.encode_string_list(queries)

        answer_service: AnswerService = AnswerService()
        best_subtitles: Dict[str, tuple[str, float]] = answer_service.get_best_subtitles(
            essay,
            embedded_queries
        )

        assert len(best_subtitles) == 0

    def test_get_best_subtitles_no_subtitles_in_single_paragraph(self) -> None:
        """
        Test get_best_subtitles when the text contains no subtitles and 
        a single paragraph to ensure the service handles it correctly 
        by returning a default subtitle called "Introduction".

        Asserts:
            Subtitle "Introduction" returned if the essay has no 
            subtitles.
        """

        essay: str = "This is the first sentence. This is the second sentence."
        queries: List[str] = ["What is the first sentence?"]

        encoder: Encoder = Encoder()
        embedded_queries: List[SentenceEmbedding] = encoder.encode_string_list(queries)

        answer_service: AnswerService = AnswerService()
        best_subtitles: Dict[str, tuple[str, float]] = answer_service.get_best_subtitles(
            essay,
            embedded_queries
        )

        assert best_subtitles["What is the first sentence?"][0] == "Introduction"


if __name__ == '__main__':
    pytest.main()
