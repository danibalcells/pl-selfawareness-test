from typing import Type

from tqdm import tqdm
import pandas as pd

from arnold.subject.base import BaseSubject
from arnold.subject.baseline import BaselineSubject
from arnold.interviewer import Interviewer
from arnold.interview import Interview
from arnold.scorer import Scorer

DEFAULT_N_INTERVIEWS = 10

class Eval:
    def __init__(
        self,
        subject_type: Type[BaseSubject] = BaselineSubject,
        n_interviews: int = DEFAULT_N_INTERVIEWS,
        verbose: bool = False
    ):
        self.n_interviews = n_interviews
        self.interviewer = Interviewer()
        self.subject = subject_type()
        self.scorer = Scorer()
        self.scores = []
        self.transcripts = []
        self.verbose = verbose

    def run(self) -> None:
        for _ in tqdm(range(self.n_interviews)):
            interview = Interview(self.interviewer, self.subject)
            interview.run(self.verbose)
            self.transcripts.append(interview.transcript)
            self.scores.append(self.scorer.run(interview.transcript))

    def as_dataframe(self) -> pd.DataFrame:
        for category in self.scores
        return pd.DataFrame(self.scores)