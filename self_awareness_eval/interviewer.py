import os

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from self_awareness_eval import constants

DEFAULT_MODEL = 'gpt-4o'
TEMPLATE_PATH = os.path.join(constants.TEMPLATES_DIR, 'interviewer/base.txt')


class Interviewer:
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

    def run(self, subject_input: str) -> str:
        response = self.chain.invoke({"input": subject_input}, {"configurable": {"session_id": "unused"}})
        return response.content