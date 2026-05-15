from pydantic import BaseModel, Field
from typing import List, Optional

class SummarizeInput(BaseModel):
    text: str = Field(..., min_length=10, description="The text to summarize")

class EmailDraftInput(BaseModel):
    topic: str = Field(..., min_length=3, description="Main topic of the email")
    tone: str = Field("professional", description="Tone of the email (e.g., professional, friendly)")
    key_points: List[str] = Field(..., min_length=1, description="List of key points to cover")

class ExtractJsonInput(BaseModel):
    text: str = Field(..., min_length=10, description="The text to extract data from")
    # For simplicity, we just use a string description of the schema
    schema_description: str = Field(..., description="Description of the JSON schema to output")

class ReportInput(BaseModel):
    data: str = Field(..., min_length=10, description="Raw data or bullet points to compile into a report")
