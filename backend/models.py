from pydantic import BaseModel
from typing import Optional


class BrandRequest(BaseModel):
    industry: Optional[str] = "Technology"
    keywords: Optional[str] = ""
    tone: Optional[str] = "Professional"
    language: Optional[str] = "en"


class ContentRequest(BaseModel):
    brand_description: Optional[str] = ""
    tone: Optional[str] = "Professional"
    content_type: Optional[str] = "product_description"
    language: Optional[str] = "en"


class SentimentRequest(BaseModel):
    text: Optional[str] = ""
    brand_tone: Optional[str] = "Professional"


class ColorRequest(BaseModel):
    tone: Optional[str] = "Professional"
    industry: Optional[str] = "Technology"


class ChatRequest(BaseModel):
    message: Optional[str] = ""


class LogoRequest(BaseModel):
    brand_name: Optional[str] = ""
    industry: Optional[str] = "Technology"
    keywords: Optional[str] = ""
