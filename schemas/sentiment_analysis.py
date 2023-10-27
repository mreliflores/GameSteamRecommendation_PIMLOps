from typing import Optional
from pydantic import BaseModel

class SentimentAnalysis(BaseModel):
  negative: Optional[int]
  neutral: Optional[int]
  positive: Optional[int]
  def __getitem__(self, item):
    return getattr(self, item)