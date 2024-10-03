"""
This module contains unit tests for the TextPreProcessor class,
which is responsible for processing text by splitting it into
paragraphs and sentences, identifying subtitles, and preprocessing
text into a structured format.
"""


from typing import List, Dict

from answer_service.text_pre_processor import TextPreProcessor

class TestTextPreProcessor:
    """
    Unit tests for the TextPreProcessor class.

    This class tests various scenarios to validate the behavior of
    the TextPreProcessor methods. It checks the correct splitting of
    paragraphs and sentences, the identification of subtitles, and 
    the overall text preprocessing functionality.
    """

    def test_split_paragraphs_normal(self) -> None:
        """
        Test that the split_paragraphs method correctly splits a normal
        text input into paragraphs.
        """

        text: str = (
               "Introduction\n"
               "This is the first paragraph. It contains two sentences.\n"
               "This is the second paragraph. It also has two sentences.\n"
                "Conclusion.\n"
                "This is the conclusion paragraph. It contains two sentences.\n"
               )

        processor: TextPreProcessor = TextPreProcessor(text)

        expected_paragraphs: List[str] = [
            "Introduction",
            "This is the first paragraph. It contains two sentences.",
            "This is the second paragraph. It also has two sentences.",
            "Conclusion.",
            "This is the conclusion paragraph. It contains two sentences."
        ]

        assert processor.split_paragraphs() == expected_paragraphs

    def test_split_paragraphs_empty(self) -> None:
        """
        Test that the split_paragraphs method returns an empty list 
        when given an empty string.
        """

        empty_processor: TextPreProcessor = TextPreProcessor("")

        assert empty_processor.split_paragraphs() == []

    def test_split_paragraphs_multiple_newlines(self) -> None:
        """
        Test that the split_paragraphs method returns an empty list
        when given multiple newlines.
        """

        newlines_processor: TextPreProcessor = TextPreProcessor("\n\n\n")

        assert newlines_processor.split_paragraphs() == []

    def test_split_sentences_normal(self) -> None:
        """
        Test that the split_sentences method correctly splits a normal
        paragraph into sentences.
        """

        paragraph: str = "This is a sentence. This is another."
        processor: TextPreProcessor = TextPreProcessor(paragraph)

        expected_sentences: List[str] = ["This is a sentence", "This is another"]

        assert processor.split_sentences(paragraph) == expected_sentences

    def test_split_sentences_single_sentence(self) -> None:
        """
        Test that the split_sentences method returns a list containing
        a single sentence when only one sentence is provided.
        """

        single_sentence: str = "Only one sentence."
        processor: TextPreProcessor = TextPreProcessor(single_sentence)

        assert processor.split_sentences(single_sentence) == ["Only one sentence"]

    def test_split_sentences_empty(self) -> None:
        """
        Test that the split_sentences method returns an empty list 
        when given an empty string.
        """

        processor: TextPreProcessor = TextPreProcessor("")

        assert processor.split_sentences("") == []

    def test_split_sentences_with_spaces(self) -> None:
        """
        Test that the split_sentences method correctly handles trailing
        spaces in a sentence.
        """

        paragraph_with_spaces: str = "   This is a sentence.   "
        processor: TextPreProcessor = TextPreProcessor(paragraph_with_spaces)

        expected_sentence: List[str] = [
            "This is a sentence"
            ]

        assert processor.split_sentences(paragraph_with_spaces) == expected_sentence

    def test_is_subtitle_true(self) -> None:
        """
        Test that the is_subtitle method returns True for a valid
        subtitle.
        """

        processor: TextPreProcessor = TextPreProcessor("Introduction")

        assert processor.is_subtitle("Introduction") is True

    def test_is_subtitle_with_period_true(self) -> None:
        """
        Test that the is_subtitle method returns True for a subtitle
        that ends with a period.
        """

        processor: TextPreProcessor = TextPreProcessor("This is a subtitle.")

        assert processor.is_subtitle("This is a subtitle.") is True

    def test_is_subtitle_empty(self) -> None:
        """
        Test that the is_subtitle method returns False for an empty 
        string.
        """

        processor: TextPreProcessor = TextPreProcessor("")

        assert processor.is_subtitle("") is False

    def test_preprocess_text_normal(self) -> None:
        """
        Test that the preprocess_text method returns the correct
        structured result for normal text input.
        """

        text: str = (
               "Introduction\n"
               "This is the first paragraph. It contains two sentences.\n"
               "This is the second paragraph. It also has two sentences.\n"
                "Conclusion.\n"
                "This is the conclusion paragraph. It contains two sentences.\n"
               )

        processor: TextPreProcessor = TextPreProcessor(text)

        expected_result: Dict[str, List[str]] = {
            "Introduction": [
                'This is the first paragraph',
                'It contains two sentences',
                'This is the second paragraph',
                'It also has two sentences'
            ],
            "Conclusion": [
                "This is the conclusion paragraph",
                 "It contains two sentences"
                ]
        }

        assert processor.preprocess_text() == expected_result

    def test_preprocess_text_empty(self) -> None:
        """
        Test that the preprocess_text method returns an empty dictionary
        when given an empty string.
        """

        empty_processor: TextPreProcessor = TextPreProcessor("")

        assert not empty_processor.preprocess_text()

    def test_preprocess_text_only_subtitles(self) -> None:
        """
        Test that the preprocess_text method handles only subtitles
        correctly.
        """

        subtitle_only: str = "Subtitle\n\nSubtitle2\n\n"
        subtitle_processor: TextPreProcessor = TextPreProcessor(subtitle_only)

        expected_subtitle_result: Dict[str, List[str]] = {
            "Subtitle": [],
            "Subtitle2": []
        }

        assert subtitle_processor.preprocess_text() == expected_subtitle_result

    def test_preprocess_text_only_sentences(self) -> None:
        """
        Test that the preprocess_text method returns the correct
        structure when only sentences are provided without any
        subtitles.
        """
        sentences_only: str = "This is the first sentence. This is the second."
        sentences_processor: TextPreProcessor = TextPreProcessor(sentences_only)

        expected_sentences_result: Dict[str, List[str]] = {
            "Introduction": [
                "This is the first sentence",
                "This is the second"
                ]
        }

        assert sentences_processor.preprocess_text() == expected_sentences_result
