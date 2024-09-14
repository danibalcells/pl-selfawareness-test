from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.prompts import ChatPromptTemplate
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from arnold.subject.base import BaseSubject

DEFAULT_MODEL = 'gpt-4o'

class BaselineSubject(BaseSubject):
    def __init__(self, model_name: str = DEFAULT_MODEL, temperature: float = 0):
        super().__init__()
        self.model_name = model_name
        self.load_model(self.model_name)
        self.history = ChatMessageHistory()
        self.prompt = self.load_template()
        self.chain = self.load_chain()

    def load_model(self, model_name: str, temperature: float = 0) -> None:
        if model_name.startswith('gpt'):
            self.llm = ChatOpenAI(model=model_name, temperature=temperature)
        elif model_name.startswith('claude'):
            self.llm = ChatAnthropic(model=model_name, temperature=temperature)
        else:
            raise ValueError(f'Unknown model: {model_name}')
        
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
        response = self.chain.invoke({"input": interviewer_input}, {"configurable": {"session_id": "unused"}})
        return response.content