from langchain.prompts import ChatPromptTemplate
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import RunnableSerializable

from arnold.subject.base import BaseSubject
from arnold.util import format_transcript, load_model


# DEFAULT_MODEL = 'claude-3-5-sonnet-20240620'
DEFAULT_MODEL = 'gpt-4o'
ANALYSIS_TEMPLATE_PATH = 'arnold/templates/selfaware/analysis.txt'
CONVERSATION_TEMPLATE_PATH = 'arnold/templates/selfaware/conversation.txt'

DEFAULT_CONVERSATION_TEMPERATURE = 0.3
DEFAULT_ANALYSIS_TEMPERATURE = 0.5


class AnalysisChain:
    def __init__(self, model_name: str = DEFAULT_MODEL, temperature: float = DEFAULT_ANALYSIS_TEMPERATURE):
        self.model_name = model_name
        self.temperature = temperature
        self.llm = load_model(self.model_name, temperature)
        self.prompt = self.load_template(ANALYSIS_TEMPLATE_PATH)
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

    def load_chain(self) -> RunnableSerializable:
        chain = self.prompt | self.llm
        return chain
        # return RunnableWithMessageHistory(
        #     chain, # type: ignore
        #     lambda session_id: self.history,
        #     input_messages_key="input",
        #     history_messages_key="chat_history"
        # )

    def run(self, transcript: str) -> str:
        response = self.chain.invoke({"input": transcript})
        return response.content


class SelfAwareSubject(BaseSubject):
    def __init__(self, 
                 model_name: str = DEFAULT_MODEL, 
                 conversation_temperature: float = DEFAULT_CONVERSATION_TEMPERATURE, 
                 analysis_temperature: float = DEFAULT_ANALYSIS_TEMPERATURE):
        super().__init__()
        self.model_name = model_name
        self.conversation_temperature = conversation_temperature
        self.analysis_temperature = analysis_temperature
        self.llm = load_model(self.model_name, self.conversation_temperature)
        self.analysis_chain = AnalysisChain(self.model_name, self.analysis_temperature)
        self.history = ChatMessageHistory()
        self.prompt = self.load_template(CONVERSATION_TEMPLATE_PATH)
        self.chain = self.load_chain()

    def load_template(self, filename: str = CONVERSATION_TEMPLATE_PATH) -> ChatPromptTemplate:
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

    def run(self, interviewer_input: str) -> str:
        transcript = format_transcript(self.history)
        transcript += f"Interviewer: {interviewer_input}\n"
        analysis = self.analysis_chain.run(transcript)
        response = self.chain.invoke(
            {"input": interviewer_input, "analysis": analysis}, 
            {"configurable": {"session_id": "unused"}}
        )
        return response.content