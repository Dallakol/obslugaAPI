import requests
import csv
from flask import Flask, render_template, request, redirect


app = Flask(__name__)


def get_rates():
    response = requests.get(
        "http://api.nbp.pl/api/exchangerates/tables/C?format=json"
    )
    data = response.json()
    rates = data[0].get('rates')
    return rates


def get_codes():
    rates = get_rates()
    codes = []
    for data in rates:
        codes.append(data.get('code'))
    return sorted(codes)


def rates_to_csv():
    rates = get_rates()
    fieldnames = ['currency', 'code', 'bid', 'ask']
    with open('rates.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, delimiter=';', fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rates)


rates_to_csv()


@app.route('/form', methods=["GET", "POST"])
def form():
    rates = get_rates()
    codes = get_codes()
    if request.method == "POST":
        data = request.form
        currency = data.get('code')
        amount = data.get('amount')
        for data in rates:
            if data.get('code') == currency:
                ask = data.get('ask')
                break
        cost = float(amount) * ask
        return (render_template("form.html", codes = codes) +
            f"Całkowity koszt po przeliczeniu: {cost:.2f} PLN")
        
    return render_template("form.html", codes = codes)