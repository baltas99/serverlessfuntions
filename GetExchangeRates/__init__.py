import azure.functions as func
import requests
import os
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    # Get the base and target currencies from the query parameters
    base_currency = req.params.get('source', 'USD')  # Default to 'USD' if no base is provided
    target_currencies = req.params.get('currencies')

    if not target_currencies:
        return func.HttpResponse(
            "Please pass one or more target currencies in the query string",
            status_code=400
        )

    # Use your API key from currencylayer.com
    api_key = os.environ.get('CURRENCY_LAYER_API_KEY')
    # Construct the API request URL with the base and target currencies
    url = f"https://apilayer.net/api/live?access_key={api_key}&currencies={target_currencies}&source={base_currency}&format=1"

    response = requests.get(url)
    data = response.json()

    if response.status_code == 200 and 'quotes' in data:
        # The API returns keys like 'EURGBP', 'EURCAD', etc.
        # We need to remove the source currency from the beginning of these keys
        source_prefix = f"{base_currency}"  # e.g., "EUR"
        rates = {currency[len(source_prefix):]: rate for currency, rate in data['quotes'].items() if currency.startswith(source_prefix)}

        return func.HttpResponse(json.dumps({'rates': rates}), mimetype="application/json")
    else:
        # It's a good practice to return the error from the external API
        error_message = data.get('error', {}).get('info', 'Failed to fetch the exchange rates')
        return func.HttpResponse(error_message, status_code=response.status_code)

