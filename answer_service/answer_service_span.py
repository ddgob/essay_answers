"""
This module provides the `AnswerServiceSpan` class, which leverages a 
pre-trained BERT model fine-tuned on the SQuAD dataset to answer 
questions based on a given body of text (essay) and one or more queries.

The module uses the BERT model for question answering, which works by 
identifying the start and end positions of the answer within the input 
text (essay). The `AnswerServiceSpan` class provides methods for 
answering both a single question and a list of questions, returning the 
relevant span of the essay as the answer.

Classes:
    - AnswerServiceSpan: A service class for answering questions based 
      on a pre-trained BERT model.

Example usage:
    answer_service = AnswerServiceSpan()
    essay = "The quick brown fox jumps over the lazy dog."
    query = "What does the quick brown fox jump over?"
    answer = answer_service.answer_single_question_span(essay, query)
    print(answer)
"""


from typing import Dict
import logging
from logging import Logger

from transformers import BertForQuestionAnswering, BertTokenizer
from torch import Tensor, no_grad

class AnswerServiceSpan:
    """
    A class for answering questions using a pre-trained BERT model.

    Attributes:
        model (BertForQuestionAnswering): The pre-trained BERT model for 
        question answering.
        tokenizer (BertTokenizer): The tokenizer used to preprocess the 
        input text.
    """

    def __init__(self) -> None:
        """
        Initializes the AnswerServiceSpan with a pre-trained BERT model 
        and tokenizer.

        Model used: 
            bert-large-uncased-whole-word-masking-finetuned-squad
        How the model works:
            The model is fine-tuned on the SQuAD dataset for question 
            answering tasks. It returns the start and end logits for the
            answer span in the input text. Therefore, when we infer the
            answer, and convert it to text, we get the answer to the
            question as a substring of the input text (essay).
        """

        self.model = BertForQuestionAnswering.from_pretrained(
            'bert-large-uncased-whole-word-masking-finetuned-squad'
        )
        self.tokenizer = BertTokenizer.from_pretrained(
            'bert-large-uncased-whole-word-masking-finetuned-squad'
        )

        self.logger: Logger = logging.getLogger(__name__)
        self.logger.info("Span Answer Service initialized.")

    def answer_single_question_span(self, essay: str, query: str) -> str:
        """
        Answers a single question based on the given essay and query.

        Args:
            essay (str): The input essay containing the answer to the 
            question.
            query (str): The input question to answer.

        Returns:
            str: The answer (span of essay) to the question based on 
            the given essay.
        """

        inputs: Dict[str, Tensor] = self.tokenizer(
            query,
            essay,
            return_tensors='pt',
            max_length=512,
            truncation=True
        )

        with no_grad():
            outputs = self.model(**inputs)

        answer_start_index: Tensor = outputs.start_logits.argmax()
        answer_end_index: Tensor = outputs.end_logits.argmax()
        answer_tokens: Tensor = inputs['input_ids'][0, answer_start_index:answer_end_index+1]

        answer: str = self.tokenizer.decode(answer_tokens, skip_special_tokens=True)

        return answer

    def answer_questions_span(self, essay: str, queries: list) -> list:
        """
        Answers a list of questions based on the given essay and 
        queries.

        Args:
            essay (str): The input essay containing the answers to the 
            questions.
            queries (List[str]): A list of questions to answer.

        Returns:
            List[str]: A list of answers to the questions based on the 
            given essay.
        """

        self.logger.info("Answering questions based on essay span...")

        answers = [self.answer_single_question_span(essay, query) for query in queries]

        self.logger.info("Finished answering questions based on essay span.")

        return answers
