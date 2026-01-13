from pydantic import BaseModel

class FeaturesOut(BaseModel):
    features: list[str]
