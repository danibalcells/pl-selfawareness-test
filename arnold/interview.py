from arnold.interviewer import Interviewer
from arnold.subject.base import BaseSubject
from arnold.util import format_transcript


DEFAULT_MAX_TURNS = 25
DEFAULT_END_OF_INTERVIEW = '<END>'

class Interview:
    def __init__(self,
                 interviewer: Interviewer,
                 subject: BaseSubject,
                 max_turns: int = DEFAULT_MAX_TURNS,
                 end_of_interview: str = DEFAULT_END_OF_INTERVIEW):
        self.interviewer = interviewer
        self.subject = subject
        self.turns = 0
        self.max_turns = max_turns
        self.end_of_interview = end_of_interview

    def run(self, verbose: bool = False) -> None:
        interviewer_message = self.interviewer.run('<SYSTEM>Begin now</SYSTEM>')
        for _ in (range(self.max_turns)):
            if verbose:
                print(f'{self.turns}. Interviewer: {interviewer_message}')
            subject_message = self.subject.run(interviewer_message)
            if verbose:
                print(f'{self.turns}. Subject: {subject_message}')
            interviewer_message = self.interviewer.run(subject_message)
            self.turns += 1
            if interviewer_message == self.end_of_interview:
                break
        self.transcript = format_transcript(self.interviewer.history)