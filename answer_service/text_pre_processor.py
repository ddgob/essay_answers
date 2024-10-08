"""
This module contains the TextPreProcessor class for processing text.
It includes methods for splitting text into paragraphs and sentences,
identifying subtitles, and preprocessing the text for further analysis.
"""


from typing import List, Dict
import logging
from logging import Logger
import re

class TextPreProcessor:
    """
    A class to preprocess text by splitting it into paragraphs and 
    sentences.

    Attributes:
        text (str): The input text to be processed.
        MAX_CHARACTERS_SUBTITLE (int): The maximum number of characters
            allowed in a subtitle.
    """

    MAX_CHARACTERS_SUBTITLE: int = 100

    def __init__(self, text) -> None:
        """
        Initializes the TextPreProcessor with the given text, removing 
        all trailing whitespaces.

        Args:
            text (str): The text to be processed.
        """

        self.text: str = text.strip()
        self.logger: Logger = logging.getLogger(__name__)
        self.logger.info("Text Pre-Processor initialized.")

    def split_paragraphs(self) -> List[str]:
        """
        Splits the text into paragraphs based on newline characters.

        Returns:
            List[str]: A list of non-empty paragraphs.
        """

        paragraphs: List[str] = self.text.split("\n")
        paragraphs = [paragraph for paragraph in paragraphs if paragraph != '']

        return paragraphs

    def split_sentences(self, paragraph: str) -> List[str]:
        """
        Splits a given paragraph into sentences based on period 
        characters.

        Args:
            paragraph (str): The paragraph to be split into sentences.

        Returns:
            List[str]: A list of non-empty sentences with no trailing 
            whitespaces.
        """

        paragraph = paragraph.strip()

        sentences: List[str] = re.split(r'[.!?]', paragraph)
        sentences = [sentence.strip() for sentence in sentences if sentence != '']

        return sentences

    def is_subtitle(self, paragraph: str) -> bool:
        """
        Determines if a given paragraph is a subtitle.

        A paragraph is considered a subtitle if it contains exactly one
        sentence and contains 100 characters or less.

        Args:
            paragraph (str): The paragraph to check.

        Returns:
            bool: True if the paragraph is a subtitle, False otherwise.
        """

        paragraph = paragraph.strip()
        sentences: List[str] = self.split_sentences(paragraph)

        if len(sentences) == 1 and len(sentences[0]) <= self.MAX_CHARACTERS_SUBTITLE:
            return True

        return False

    def preprocess_text(self) -> Dict[str, List[str]]:
        """
        Processes the text by splitting it into paragraphs and 
        sentences.

        This method identifies subtitles and organizes sentences under
        their respective subtitles in a dictionary format.

        Returns:
            Dict[str, List[str]]: A dictionary where keys are subtitles
            and values are lists of sentences.
        """

        paragraphs: List[str] = self.split_paragraphs()
        preprocessed_text: Dict[str, List[str]] = {}
        last_subtitle: str = 'Introduction'

        for paragraph in paragraphs:
            if self.is_subtitle(paragraph):
                subtitle = self.split_sentences(paragraph)[0]
                preprocessed_text[subtitle] = []
                last_subtitle = subtitle
            else:
                if last_subtitle not in preprocessed_text:
                    preprocessed_text[last_subtitle] = []

                sentences: List[str] = self.split_sentences(paragraph)
                preprocessed_text[last_subtitle].extend(sentences)

        return preprocessed_text

    def get_text_body(self) -> List[str]:
        """
        Retrieves the body of the text, excluding subtitles.

        This method processes the text and returns a list of all 
        sentences found in the paragraphs, excluding the subtitles.

        Returns:
            List[str]: A list of sentences from the body of the text.
        """

        self.logger.info("Getting text body...")

        preprocessed_text: Dict[str, List[str]] = self.preprocess_text()
        text_body: List[str] = []

        if self.is_text_only_subtitles():
            text_body = list(preprocessed_text.keys())
            return text_body

        for paragraph in preprocessed_text.values():
            for sentence in paragraph:
                text_body.append(sentence)

        self.logger.info("Got text body successfully.")

        return text_body

    def get_subtitles(self) -> List[str]:
        """
        Retrieves all subtitles found in the text.

        This method processes the text and returns a list of all 
        subtitles found in the paragraphs.

        Returns:
            List[str]: A list of subtitles from the text.
        """

        self.logger.info("Getting subtitles...")

        preprocessed_text: Dict[str, List[str]] = self.preprocess_text()

        self.logger.info("Got subtitles successfully.")

        return list(preprocessed_text.keys())

    def get_all_text_sentences(self) -> List[str]:
        """
        Retrieves all sentences in the text, including subtitles and 
        body sentences.

        This method combines both subtitles and body sentences into a 
        single list.

        Returns:
            List[str]: A list of all sentences from the text, including 
            subtitles.
        """

        self.logger.info("Getting all text sentences...")

        all_text_sentences: List[str] = self.get_text_body() + self.get_subtitles()

        self.logger.info("Got all text sentences successfully.")

        return all_text_sentences

    def is_text_only_subtitles(self) -> bool:
        """
        Checks if the text contains only subtitles.

        This method determines if the text consists solely of subtitles 
        without any body sentences.

        Returns:
            bool: True if the text contains only subtitles, False 
            otherwise.
        """

        preprocessed_text: Dict[str, List[str]] = self.preprocess_text()
        if any(preprocessed_text.values()):
            return False
        return True
