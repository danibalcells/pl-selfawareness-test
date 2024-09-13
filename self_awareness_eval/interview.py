from langchain_community.chat_message_histories import ChatMessageHistory

from self_awareness_eval.interviewer import Interviewer
from self_awareness_eval.subject.base import BaseSubject

MAX_TURNS = 50
END_OF_INTERVIEW = '<END>'

class Interview:
    def __init__(self, interviewer: Interviewer, subject: BaseSubject):
        self.interviewer = interviewer
        self.subject = subject

    def run(self) -> str:
        turns = 0
        interviewer_message = self.interviewer.run('<SYSTEM>Begin now</SYSTEM>')
        while interviewer_message != END_OF_INTERVIEW and turns < MAX_TURNS:
            subject_message = self.subject.run(interviewer_message)
            interviewer_message = self.interviewer.run(subject_message)
            turns += 1

        return self.format_history(self.interviewer.history)

    def format_history(self, history: ChatMessageHistory) -> str:
        formatted_history = ''
        for message in history.messages:
            formatted_history += f'{message.type}: {message.content}\n'
        return formatted_history