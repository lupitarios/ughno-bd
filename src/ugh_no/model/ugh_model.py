from pydantic import BaseModel
from src.ugh_no.model.ugh_enums import ToneEnum, LengthEnum, StyleEnum, SeverityEnum


class BaseUghModel(BaseModel):
    tone: ToneEnum
    humour_level: int
    directness: int
    length: LengthEnum = LengthEnum.short
    style: StyleEnum
    severity_level: SeverityEnum = SeverityEnum.low

class UghNoRequest(BaseUghModel):
    instant_mode: bool = True

    def __str__(self):
        return (f"UghNoRequest(tone={self.tone}, humor_level={self.humour_level}, "
                f"directness={self.directness}, length={self.length}, style={self.style})")

class UghNoResponse(BaseUghModel):
    response: str

    def __str__(self):
        return str(self.response)