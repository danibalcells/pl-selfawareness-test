class BaselineSubject(BaseSubject):
    def __init__(self):
        super().__init__()

    def run(self, interviewer_input: str) -> str:
        return 'I am a baseline subject.'