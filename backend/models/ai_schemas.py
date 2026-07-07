from enum import StrEnum

from pydantic import BaseModel, Field


class Category(StrEnum):
    research = "Research"
    engineering = "Engineering"
    business = "Business"
    policy = "Policy"
    general = "General"


class ProcessingResult(BaseModel):
    is_relevant: bool
    title: str = ""
    summary_engineer: str = ""
    summary_enthusiast: str = ""
    category: Category = Category.general
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
