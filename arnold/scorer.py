from typing import Union

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import JsonOutputParser

DEFAULT_MODEL = 'gpt-4o'
TEMPLATE_PATH = 'arnold/templates/scorer/scorer.txt'


class Scorer:
    def __init__(self, model: str = DEFAULT_MODEL):
        self.model = model
        self.llm = ChatOpenAI(model=self.model, temperature=0)
        self.prompt = self.load_template(TEMPLATE_PATH)
        self.history = ChatMessageHistory()
        self.chain = self.load_chain()

    def load_template(self, filename: str) -> ChatPromptTemplate:
        with open(filename, 'r') as f:
            prompt_str = f.read()
            return ChatPromptTemplate.from_messages([
                ("system", prompt_str),
                ("human", "{transcript}")
            ])

    def load_chain(self) -> RunnableWithMessageHistory:
        chain = self.prompt | self.llm | JsonOutputParser()
        return RunnableWithMessageHistory(
            chain, # type: ignore
            lambda session_id: self.history,
            input_messages_key="transcript",
            history_messages_key="chat_history"
        )

    def run(self, transcript: str) -> dict[str, Union[int, str]]:
        response = self.chain.invoke({"transcript": transcript}, {"configurable": {"session_id": "unused"}})
        scores = {}
        for category, details in response.items():
            for key, value in details.items():
                scores[f"{category}_{key}"] = value
        return scores