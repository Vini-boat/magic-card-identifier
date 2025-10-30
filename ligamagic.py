from datetime import date
from pydantic import BaseModel , RootModel, HttpUrl, model_validator
from typing import Any, Dict, List, Optional

extra_types = {
  "0": {
    "id": 0,
    "acron": "N",
    "label": "Normal"
  },
  "2": {
    "id": 2,
    "acron": "F",
    "label": "Foil"
  },
  "3": {
    "id": 3,
    "acron": "P",
    "label": "Promo"
  },
  "5": {
    "id": 5,
    "acron": "PL",
    "label": "Pre Release"
  },
  "7": {
    "id": 7,
    "acron": "F",
    "label": "FNM"
  },
  "11": {
    "id": 11,
    "acron": "D",
    "label": "DCI"
  },
  "13": {
    "id": 13,
    "acron": "T",
    "label": "Textless"
  },
  "17": {
    "id": 17,
    "acron": "A",
    "label": "Assinada"
  },
  "19": {
    "id": 19,
    "acron": "B",
    "label": "Buy A Box"
  },
  "23": {
    "id": 23,
    "acron": "OV",
    "label": "Oversize"
  },
  "29": {
    "id": 29,
    "acron": "AL",
    "label": "Alterada"
  },
  "31": {
    "id": 31,
    "acron": "FE",
    "label": "Foil Especial / Foil Etched"
  },
  "37": {
    "id": 37,
    "acron": "MP",
    "label": "Misprint"
  },
  "41": {
    "id": 41,
    "acron": "MC",
    "label": "Miscut"
  }
}

class Price(BaseModel):
    min: float
    avg: float
    max: float 

    @model_validator(mode='before')
    @classmethod
    def change_names(cls, data: Any) -> Dict[str, Any]:
        data["min"] = data["p"]
        data["avg"] = data["m"]
        data["max"] = data["g"]
        return data


class ExtraPrice(BaseModel):
    type: str
    price: Optional[Price]

class Edition(BaseModel):
    name: str
    code: str
    img: HttpUrl
    date: date
    price: List[ExtraPrice]

    @model_validator(mode='before')
    @classmethod
    def add_http_protocol_to_img(cls, data: Any) -> Dict[str, Any]:
        data["img"] = "http:" + data["img"]
        return data

    @model_validator(mode='before')
    @classmethod
    def convert_price_types(cls, data: Any) -> Dict[str, Any]:
        original: dict = data["price"].copy() 
        if isinstance(data["price"],dict):
          temp = []
          for k,v in original.items():
              if isinstance(v,dict):
                  temp.append(ExtraPrice(
                    type=extra_types[k]["label"],
                    price=Price(**v)
                  ))
                  continue
              if isinstance(v,list):
                  temp.append(ExtraPrice(type=extra_types[k]["label"],price=None))
          data["price"] = temp

          # data["price"] = [
          #     ExtraPrice(
          #         type=extra_types[k]["label"],
          #         price=Price(**v)
          #     )
          #     for k,v in original.items()    
          # ]
          return data
    
        if isinstance(data["price"],list):
          data["price"] = [
              ExtraPrice(
                  type=extra_types["0"]["label"],
                  price=Price(**data["price"][0])
              )
              for v in original
          ]
          return data
      
        return data



class EditionList(RootModel):
    root: List[Edition]

class CardInLigaMagic(BaseModel):
    name: str
    editions: List[Edition]