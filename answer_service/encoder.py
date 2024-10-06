"""
This module provides an Encoder class for encoding text into embeddings 
using the SentenceTransformer library. The encoded embeddings can be 
used for tasks like finding similarities between sentences or other 
machine learning applications.
"""

import sys
import os
from typing import List

from torch import Tensor, device, no_grad

from sentence_transformers import SentenceTransformer

build_path: str = os.path.join(os.path.dirname(__file__), 'sentence_embedding/build')
sys.path.append(build_path)

from sentence_embedding import SentenceEmbedding

class Encoder:
    """
    A class for encoding sentences into embeddings using a pre-trained 
    SentenceTransformer model.

    Attributes:
        device (torch.device): The device (CPU/GPU) to run the model on.
        model (SentenceTransformer): The pre-trained transformer model 
        used to encode the sentences.
    """

    def __init__(self) -> None:
        """
        Initializes the Encoder with a pre-trained SentenceTransformer 
        model and sets the device to CPU.
        """
        self.device: device = device('cpu')
        self.model: SentenceTransformer = SentenceTransformer(
            'all-mpnet-base-v2',
            device='cpu',
        )

    def encode(self, sentence: str) -> SentenceEmbedding:
        """
        Encodes a single sentence into an embedding.

        Args:
            sentence (str): The input sentence to encode.

        Returns:
            SentenceEmbedding: A SentenceEmbedding object containing 
            the original sentence and its corresponding embedding.
        """
        with no_grad():
            embedding: Tensor = self.model.encode([sentence], convert_to_tensor=True)

        numpy_embedding: List[float] = embedding.cpu().numpy()[0].tolist()
        return SentenceEmbedding(sentence, numpy_embedding)

    def encode_string_list(self, sentences: List[str]) -> List[SentenceEmbedding]:
        """
        Encodes a list of sentences into embeddings.

        Args:
            sentences (List[str]): A list of sentences to encode.

        Returns:
            List[SentenceEmbedding]: A list of SentenceEmbedding objects 
            containing the original sentences and their corresponding 
            embeddings.
        """
        sentence_embeddings: List[SentenceEmbedding] = []
        for sentence in sentences:
            sentence_embeddings.append(self.encode(sentence))
        return sentence_embeddings
