from langchain_community.chat_message_histories import ChatMessageHistory

from arnold.interviewer import Interviewer
from arnold.subject.base import BaseSubject

MAX_TURNS = 50
END_OF_INTERVIEW = '<END>'

class Interview:
    def __init__(self, interviewer: Interviewer, subject: BaseSubject):
        self.interviewer = interviewer
        self.subject = subject

    def run(self, verbose: bool = False) -> str:
        turns = 0
        interviewer_message = self.interviewer.run('<SYSTEM>Begin now</SYSTEM>')
        while interviewer_message != END_OF_INTERVIEW and turns < MAX_TURNS:
            if verbose:
                print(f'{turns}. Interviewer: {interviewer_message}')
            subject_message = self.subject.run(interviewer_message)
            if verbose:
                print(f'{turns}. Subject: {subject_message}')
            interviewer_message = self.interviewer.run(subject_message)
            turns += 1

        return self.format_history(self.interviewer.history)

    def format_history(self, history: ChatMessageHistory) -> str:
        formatted_history = ''
        for message in history.messages[1:]:
            if message.type == 'human':
                formatted_history += f'Subject: {message.content}\n'
            elif message.type == 'ai':
                formatted_history += f'Interviewer: {message.content}\n'
        return formatted_history