import requests

usd_request = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
usd_data = usd_request.json()
usd_price = usd_data["Valute"]["USD"]["Value"]

eur_request = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
eur_data = eur_request.json()
eur_price = eur_data["Valute"]["EUR"]["Value"]

cad_request = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
cad_data = cad_request.json()
cad_price = cad_data["Valute"]["CAD"]["Value"]


currencies = {
	"USA Dollar": "USD",
	"Euro": "EUR",
	"Canadian Dollar": "CAD"
}