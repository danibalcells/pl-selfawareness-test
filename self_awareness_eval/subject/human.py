from self_awareness_eval.subject.base import BaseSubject

class HumanSubject(BaseSubject):
    def __init__(self):
        super().__init__()

    def run(self, interviewer_input: str) -> str:
        return input(interviewer_input)