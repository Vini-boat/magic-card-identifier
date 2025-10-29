from datetime import date
from pydantic import BaseModel , RootModel, HttpUrl, model_validator
from typing import Any, Dict, List

class Card(BaseModel):
    name: str
    scryfall_uri: HttpUrl
    image_uri: HttpUrl
    set_name: str
    released_at: date

    @model_validator(mode='before')
    @classmethod
    def remove_uri_utm_source(cls, data: Any) -> Dict[str, Any]:
        data["scryfall_uri"] = data["scryfall_uri"].removesuffix("?utm_source=api")
        return data

    @model_validator(mode='before')
    @classmethod
    def extract_image_uri(cls, data: Any) -> Dict[str, Any]:
        data["image_uri"] = data["image_uris"]["normal"]
        return data
    



class CardList(RootModel):
    root: List[Card]