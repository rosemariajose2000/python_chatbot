from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "fca_live_1u1Qpi7l1eojFs631JnL5XnJUkeWyM0mHRNEqCAK"


@app.route('/', methods=["GET", "POST"])
def index():

    # Allow browser test
    if request.method == "GET":
        return "Rosebot webhook is running!"

    data = request.get_json()

    parameters = data.get("queryResult", {}).get("parameters", {})
    unit_currency = parameters.get("unit-currency", {})

    source_currency = unit_currency.get("currency")
    amount = unit_currency.get("amount")
    target_currency = parameters.get("currency-name")

    print(source_currency)
    print(amount)
    print(target_currency)

    if not source_currency or not amount or not target_currency:
        return jsonify({
            "fulfillmentText": "Please provide amount and currencies properly."
        })

    cf = fetch_conversion_factor(source_currency, target_currency)

    if not cf:
        return jsonify({
            "fulfillmentText": "Sorry, I could not fetch exchange rate."
        })

    final_amount = float(amount) * float(cf)

    response = {
        "fulfillmentText": "{} {} is {} {}".format(
            amount, source_currency, round(final_amount, 2), target_currency
        )
    }

    return jsonify(response)


def fetch_conversion_factor(source, target):
    url = "https://api.freecurrencyapi.com/v1/latest?apikey={}&base_currency={}&currencies={}".format(
        API_KEY, source, target
    )

    response = requests.get(url)
    response = response.json()

    return response.get("data", {}).get(target)


if __name__ == '__main__':
    app.run(debug=True)
