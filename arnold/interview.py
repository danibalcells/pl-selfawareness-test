from tqdm import tqdm
from langchain_community.chat_message_histories import ChatMessageHistory

from arnold.interviewer import Interviewer
from arnold.subject.base import BaseSubject
from arnold.util import format_transcript


MAX_TURNS = 25
END_OF_INTERVIEW = '<END>'

class Interview:
    def __init__(self, interviewer: Interviewer, subject: BaseSubject):
        self.interviewer = interviewer
        self.subject = subject
        self.turns = 0

    def run(self, verbose: bool = False) -> None:
        interviewer_message = self.interviewer.run('<SYSTEM>Begin now</SYSTEM>')
        for _ in (range(MAX_TURNS)):
            if verbose:
                print(f'{self.turns}. Interviewer: {interviewer_message}')
            subject_message = self.subject.run(interviewer_message)
            if verbose:
                print(f'{self.turns}. Subject: {subject_message}')
            interviewer_message = self.interviewer.run(subject_message)
            self.turns += 1
            if interviewer_message == END_OF_INTERVIEW or self.turns >= MAX_TURNS:
                break
        self.transcript = format_transcript(self.interviewer.history)