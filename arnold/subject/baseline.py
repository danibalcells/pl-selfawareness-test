from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.prompts import ChatPromptTemplate
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from arnold.subject.base import BaseSubject
from arnold.util import load_model

DEFAULT_SUBJECT_MODEL = 'gpt-4o'
DEFAULT_SUBJECT_TEMPERATURE = 0

class BaselineSubject(BaseSubject):
    def __init__(self, model_name: str = DEFAULT_SUBJECT_MODEL, temperature: float = DEFAULT_SUBJECT_TEMPERATURE):
        super().__init__()
        self.model_name = model_name
        self.llm = load_model(self.model_name, temperature)
        self.history = ChatMessageHistory()
        self.prompt = self.load_template()
        self.chain = self.load_chain()

    def load_template(self) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages([
            ("placeholder", "{chat_history}"),
            ("human", "{input}")
        ])

    def load_chain(self) -> RunnableWithMessageHistory:
        chain = self.prompt | self.llm
        return RunnableWithMessageHistory(
            chain, # type: ignore
            lambda session_id: self.history,
            input_messages_key="input",
            history_messages_key="chat_history"
        )

    def run(self, interviewer_input: str) -> str:
        response = self.chain.invoke(
            {"input": interviewer_input},
            {"configurable": {"session_id": "unused"}}
        )
        return response.content