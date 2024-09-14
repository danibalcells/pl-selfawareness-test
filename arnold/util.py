from typing import Union

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

def format_transcript(history: ChatMessageHistory) -> str:
    formatted_history = ''
    for message in history.messages[1:]:
        if message.type == 'human':
            formatted_history += f'Subject: {message.content}\n'
        elif message.type == 'ai':
            formatted_history += f'Interviewer: {message.content}\n'
    return formatted_history


def load_model(model_name: str, temperature: float = 0) -> Union[ChatOpenAI, ChatAnthropic]:
    if model_name.startswith('gpt'):
        return ChatOpenAI(model=model_name, temperature=temperature)
    elif model_name.startswith('claude'):
        return ChatAnthropic(model=model_name, temperature=temperature)
    else:
        raise ValueError(f'Unknown model: {model_name}')