from arnold.subject.base import BaseSubject

class HumanSubject(BaseSubject):
    def __init__(self):
        super().__init__()

    def run(self, interviewer_input: str) -> str:
        print(interviewer_input)
        return input('> ')