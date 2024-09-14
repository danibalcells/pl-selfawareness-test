import asyncio
from typing import Type

from tqdm import tqdm
from tqdm.asyncio import tqdm as async_tqdm
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
        subject_kwargs: dict = {},
        n_interviews: int = DEFAULT_N_INTERVIEWS,
        verbose: bool = False
    ):
        self.n_interviews = n_interviews
        self.subject_type = subject_type
        self.subject_kwargs = subject_kwargs
        self.scorer = Scorer()
        self.scores = []
        self.transcripts = []
        self.verbose = verbose

    def run_interview(self) -> None:
        interviewer = Interviewer()
        subject = self.subject_type(**self.subject_kwargs)
        interview = Interview(interviewer, subject)
        interview.run(self.verbose)
        self.transcripts.append(interview.transcript)
        self.scores.append(self.scorer.run(interview.transcript))

    def run(self) -> None:
        for _ in tqdm(range(self.n_interviews)):
            self.run_interview()

    async def run_async(self) -> None:
        loop = asyncio.get_running_loop()
        tasks = [loop.run_in_executor(None, self.run_interview) for _ in range(self.n_interviews)]
        for task in async_tqdm(asyncio.as_completed(tasks), total=self.n_interviews):
            await task

    def as_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(self.scores)

    def get_median_scores(self) -> pd.Series:
        df = self.as_dataframe()
        score_columns = [col for col in df.columns if 'score' in col]
        return df[score_columns].median()

    def get_self_awareness_score(self) -> float:
        return self.get_median_scores().mean()