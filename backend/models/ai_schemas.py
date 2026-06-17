from pydantic import BaseModel


class ClassificationResult(BaseModel):
    is_relevant: bool


class SummaryResult(BaseModel):
    summary: str
