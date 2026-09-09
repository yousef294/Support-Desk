from typing import List

from pydantic import BaseModel, Field, field_validator


class QueryRequest(BaseModel):
    """POST /query request body."""

    question: str = Field(
        ...,
        min_length=1,
        description="The question the assistant should answer from the indexed documents.",
        examples=["What is the standard return window?"],
    )

    @field_validator("question")
    @classmethod
    def question_not_blank(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Question cannot be blank.")
        return cleaned


class QueryResponse(BaseModel):
    """POST /query response: a grounded answer plus the sources it came from."""

    answer: str = Field(..., description="Grounded answer generated from the retrieved context.")
    sources: List[str] = Field(..., description="Citations, e.g. ['FAQs.pdf (Pg. 4)'].")