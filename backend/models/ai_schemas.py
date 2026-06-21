from enum import StrEnum

from pydantic import BaseModel


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
