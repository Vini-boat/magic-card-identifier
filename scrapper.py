from curl_cffi import requests as curl
import re
import json
import html
from ligamagic import CardInLigaMagic

print("Nome da carta: ",end="")
busca = input()

get_card_editions = r"var cards_editions = ([\s\S]+?);\s*var card"
get_card_name = r"<title>([\s\S]+?)\s*\/"

url = "https://www.ligamagic.com.br/"
params = {
    "view": "cards/card",
    "card": busca
}
resp = curl.get(url, params=params, impersonate="chrome")
resp.raise_for_status()


card_name = re.findall(get_card_name,resp.text)[0]
card_name = html.unescape(card_name)

matches = re.findall(get_card_editions,resp.text)
j = json.loads(matches[0])

search = CardInLigaMagic.model_validate({"name": card_name, "editions": j})
print(search.model_dump_json(indent=4))