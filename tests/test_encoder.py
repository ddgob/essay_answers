"""
Test module for Encoder class in the sentence embedding system.

This module uses pytest to test the functionality of the Encoder class,
including embedding sentences and handling edge cases.
"""

import os
import sys
from typing import List

import pytest

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
build_path = os.path.join(project_root, 'answer_service', 'sentence_embedding', 'build')
sys.path.append(build_path)

from sentence_embedding import SentenceEmbedding # type: ignore

class TestEncoder:
    """
    Test class for the Encoder class, which encodes sentences using a 
    pre-trained SentenceTransformer model and returns SentenceEmbedding 
    objects.

    The tests cover edge cases such as empty inputs, non-string inputs,
    and the correct functionality of embedding lists of sentences.
    """

    MODEL_OUTPUT_DIMENSION = 768

    def test_encode_valid_sentence(self, encoder) -> None:
        """
        Test encoding a valid sentence.

        Ensures that the returned SentenceEmbedding contains the correct 
        sentence and embedding shape.
        """

        sentence: str = "This is a test sentence."
        embedding_obj: SentenceEmbedding = encoder.encode(sentence)

        assert embedding_obj.get_sentence() == sentence

    def test_encode_embedding_length(self, encoder) -> None:
        """
        Test that the embedding returned has the correct length.

        Verifies that the length of the embedding matches the expected 
        dimensions for the model.
        """

        sentence: str = "This is a test sentence."
        embedding_obj: SentenceEmbedding = encoder.encode(sentence)

        assert len(embedding_obj.get_embedding()) == self.MODEL_OUTPUT_DIMENSION

    def test_encode_empty_sentence(self, encoder) -> None:
        """
        Test encoding an empty string.

        Verifies that the Encoder can handle an empty string without 
        crashing.
        """

        sentence: str = ""
        embedding_obj: SentenceEmbedding = encoder.encode(sentence)

        assert embedding_obj.get_sentence() == sentence

    def test_encode_empty_sentence_embedding_length(self, encoder) -> None:
        """
        Test encoding an empty string.

        Verifies that the length of the embedding matches the expected 
        dimensions for the model.
        """

        sentence: str = ""
        embedding_obj: SentenceEmbedding = encoder.encode(sentence)

        assert len(embedding_obj.get_embedding()) == self.MODEL_OUTPUT_DIMENSION

    def test_encode_string_list(self, encoder) -> None:
        """
        Test encoding a list of sentences.

        Ensures that the Encoder correctly returns a list of 
        SentenceEmbedding objects for a list of sentences.
        """

        sentences: List[str] = ["First sentence.", "Second sentence."]
        embeddings: SentenceEmbedding = encoder.encode_string_list(sentences)

        assert len(embeddings) == len(sentences)

    def test_encode_empty_list(self, encoder) -> None:
        """
        Test encoding an empty list of sentences.

        Verifies that the Encoder handles an empty list by returning an 
        empty list of SentenceEmbedding objects.
        """

        sentences: List[str] = []
        embeddings: SentenceEmbedding = encoder.encode_string_list(sentences)

        assert len(embeddings) == 0, "The embedding list should be empty."

    def test_encode_list_with_empty_string(self, encoder) -> None:
        """
        Test encoding a list with one empty string.

        Ensures that the Encoder handles the empty string in a list of 
        sentences.
        """

        sentences: List[str] = ["", "Non-empty sentence."]
        embeddings: SentenceEmbedding = encoder.encode_string_list(sentences)

        assert embeddings[0].get_sentence() == ""

    def test_encode_list_with_empty_string_embedding_length(self, encoder) -> None:
        """
        Test encoding a list with one empty string.

        Verifies that the length of the embedding matches the expected 
        dimensions for the model in a list with an empty string.
        """

        sentences: List[str] = ["", "Non-empty sentence."]
        embeddings: SentenceEmbedding = encoder.encode_string_list(sentences)

        assert len(embeddings[0].get_embedding()) == self.MODEL_OUTPUT_DIMENSION

    def test_encode_non_string_input(self, encoder) -> None:
        """
        Test that encoding non-string input raises an appropriate error.

        Ensures that passing non-string data to the Encoder raises a 
        TypeError or ValueError.
        """

        non_string_input: int = 12345
        with pytest.raises(TypeError):
            encoder.encode(non_string_input)

if __name__ == '__main__':
    pytest.main()
