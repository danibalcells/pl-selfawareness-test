from langchain.prompts import ChatPromptTemplate
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from arnold.util import load_model

# DEFAULT_MODEL = 'claude-3-5-sonnet-20240620'
DEFAULT_MODEL = 'gpt-4o'
TEMPLATE_PATH = 'arnold/templates/interviewer/interviewer.txt'


class Interviewer:
    def __init__(self, model_name: str = DEFAULT_MODEL, temperature: float = 0):
        self.model_name = model_name
        self.llm = load_model(self.model_name, temperature)
        self.prompt = self.load_template()
        self.history = ChatMessageHistory()
        self.chain = self.load_chain()

    def load_template(self, filename: str = TEMPLATE_PATH) -> ChatPromptTemplate:
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