from enum import Enum

class ToneEnum(str, Enum):
    formal = "formal"
    sarcastic = "sarcastic"
    enthusiastic = "enthusiastic"
    firm = "firm"
    neutral = "neutral"
    polite = "polite"
    calm = "calm"
    friendly = "friendly"
    playful = "playful"
    witty = "witty"
    dry = "dry"
    assertive = "assertive"
    confident = "confident"
    empathetic = "empathetic"
    escalation = "escalation"


class StyleEnum(str, Enum):
    respectful = "respectful"
    conversational = "conversational"
    professional = "professional"
    corporate = "corporate"
    casual = "casual"
    deadpan = "deadpan"
    minimal = "minimal"
    direct = "direct"
    supportive = "supportive"


class LengthEnum(str, Enum):
    very_short = "very_short" # 1 short sentence
    short = "short"  # 1 sentence
    medium = "medium" # 2–3 sentences

class SeverityEnum(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    extreme = "extreme"

class ViolationType(str, Enum):
    unsolicited_image = "unsolicited_image"
    harassment = "harassment"
    hate_speech = "hate_speech"
    spam = "spam"
    threats = "threats"
    explicit_content = "explicit_content"
    misinformation = "misinformation"
    privacy_violation = "privacy_violation"
    other = "other"
