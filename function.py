import azure.functions as func
import requests
import os
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    currencies = req.params.get('currencies')
    if not currencies:
        return func.HttpResponse(
             "Please pass one or more currencies in the query string",
             status_code=400
        ) 

    # Use your API key from currencylayer.com
    api_key = os.environ.get('CURRENCY_LAYER_API_KEY')
    url = f'http://apilayer.net/api/live?access_key={api_key}&currencies={currencies}&format=1'
    
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200 and 'quotes' in data:
        # Extract the exchange rates from the response data
        rates = {currency[3:]: rate for currency, rate in data['quotes'].items() if currency != 'USDUSD'}  # Exclude USD to USD
        return func.HttpResponse(json.dumps(rates), mimetype="application/json")
    else:
        return func.HttpResponse(
             "Failed to fetch the exchange rates",
             status_code=500
        )
