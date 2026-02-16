from pydantic import BaseModel, validator, Field
from app.model.ugh_enums import ToneEnum, LengthEnum, StyleEnum, SeverityEnum


class BaseUghModel(BaseModel):
    tone: ToneEnum
    humour_level: int = Field(..., ge=0, le=10)
    directness: int = Field(..., ge=0, le=10)
    length: LengthEnum = LengthEnum.short
    style: StyleEnum
    severity_level: SeverityEnum = SeverityEnum.low

    @validator('humour_level')
    def validate_humour_level(cls, value):
        if not (0 <= value <= 10):
            raise ValueError('humour_level must be between 0 and 10')
        return value

    @validator('directness')
    def validate_directness(cls, value):
        if not (0 <= value <= 10):
            raise ValueError('directness must be between 0 and 10')
        return value

class UghNoRequest(BaseUghModel):
    instant_mode: bool = True

    def __str__(self):
        return (f"UghNoRequest(tone={self.tone}, humor_level={self.humour_level}, "
                f"directness={self.directness}, length={self.length}, style={self.style})")

class UghNoResponse(BaseUghModel):
    response: str

    def __str__(self):
        return str(self.response)