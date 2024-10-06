"""
This package contains all the necessary modules to process text, encode sentences,
and provide answers based on text embeddings. The `answer_service` package includes
the following modules:

- `text_pre_processor`: Responsible for processing raw text by splitting it into paragraphs,
  identifying subtitles, and extracting structured information.
  
- `encoder`: Provides a pre-trained model to encode sentences into embeddings, which can be
  used for similarity computations.
  
- `answer_service`: The main service class that answers queries based on sentence and subtitle
  similarity in essays.

This package also includes bindings to a C++ extension (located in the `sentence_embedding`
submodule) that handles sentence embeddings and computes similarities more efficiently.
"""

from .text_pre_processor import TextPreProcessor
from .encoder import Encoder
from .answer_service import AnswerService
