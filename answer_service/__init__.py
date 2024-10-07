"""
This package contains all the necessary modules for processing text, encoding sentences, 
and providing answers based on text embeddings and span-based question answering. The 
`answer_service` package includes the following modules:

- `text_pre_processor`: Responsible for processing raw text by splitting it into 
  paragraphs, identifying subtitles, and extracting structured information from essays.
  
- `encoder`: Provides a pre-trained SentenceTransformer model to encode sentences into 
  embeddings, which can be used for similarity computations, such as finding the most 
  similar sentence or subtitle in an essay.
  
- `answer_service`: The main service class that answers queries based on sentence and 
  subtitle similarity in essays by leveraging sentence embeddings.
  
- `answer_service_span`: A service class that uses a pre-trained BERT model fine-tuned 
  on the SQuAD dataset to answer questions by identifying the start and end span of 
  the answer in the essay text.

This package also includes bindings to a C++ extension (located in the `sentence_embedding` 
submodule) that handles sentence embeddings and efficiently computes similarities.
"""

from .text_pre_processor import TextPreProcessor
from .encoder import Encoder
from .answer_service import AnswerService
from .answer_service_span import AnswerServiceSpan
