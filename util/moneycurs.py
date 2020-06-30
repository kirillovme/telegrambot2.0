import requests

global_request = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
global_data = global_request.json()
usd_price = global_data["Valute"]["USD"]["Value"]
eur_price = global_data["Valute"]["EUR"]["Value"]
cad_price = global_data["Valute"]["CAD"]["Value"]

currencies = {
	"USA Dollar": "USD",
	"Euro": "EUR",
	"Canadian Dollar": "CAD"
}
