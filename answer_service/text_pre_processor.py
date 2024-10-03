"""
This module contains the TextPreProcessor class for processing text.
It includes methods for splitting text into paragraphs and sentences,
identifying subtitles, and preprocessing the text for further analysis.
"""


from typing import List, Dict

class TextPreProcessor:
    """
    A class to preprocess text by splitting it into paragraphs and 
    sentences.

    Attributes:
        text (str): The input text to be processed.
    """

    def __init__(self, text) -> None:
        """
        Initializes the TextPreProcessor with the given text, removing 
        all trailing whitespaces.

        Args:
            text (str): The text to be processed.
        """

        self.text: str = text.strip()

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

        sentences: List[str] = paragraph.split(".")
        sentences = [sentence.strip() for sentence in sentences if sentence != '']

        return sentences

    def is_subtitle(self, paragraph: str) -> bool:
        """
        Determines if a given paragraph is a subtitle.

        A paragraph is considered a subtitle if it contains exactly one
        sentence.

        Args:
            paragraph (str): The paragraph to check.

        Returns:
            bool: True if the paragraph is a subtitle, False otherwise.
        """

        paragraph = paragraph.strip()
        sentences: List[str] = self.split_sentences(paragraph)

        if len(sentences) == 1:
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
        text_body: Dict[str, List[str]] = {}
        last_subtitle: str = 'Introduction'

        for paragraph in paragraphs:
            if self.is_subtitle(paragraph):
                subtitle = self.split_sentences(paragraph)[0]
                text_body[subtitle] = []
                last_subtitle = subtitle
            else:
                if last_subtitle not in text_body:
                    text_body[last_subtitle] = []

                sentences: List[str] = self.split_sentences(paragraph)
                text_body[last_subtitle].extend(sentences)

        return text_body
