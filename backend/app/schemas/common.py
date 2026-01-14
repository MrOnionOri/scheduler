# backend/app/schemas/common.py
import re
from pydantic import BaseModel, field_validator

HEX_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")

class ColorMixin(BaseModel):
    color_hex: str | None = None

    @field_validator("color_hex")
    @classmethod
    def validate_hex(cls, v: str | None):
        if v is None:
            return v
        if not HEX_RE.match(v):
            raise ValueError("color_hex must be like #RRGGBB (e.g. #3B82F6)")
        return v
