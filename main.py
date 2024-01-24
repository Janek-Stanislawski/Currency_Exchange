import tkinter
from tkinter import Entry
import httpx
import datetime
import matplotlib.pyplot as plt


def get_rate(currency: str):
    response = httpx.get(f"https://api.nbp.pl/api/exchangerates/rates/a/{currency}/last")
    rate_dict = response.json()["rates"][0]
    return rate_dict["mid"]


def get_historical_data(currency: str):
    today = datetime.date.today()
    start_date = datetime.date.today() - datetime.timedelta(days=365)
    response = httpx.get(f"http://api.nbp.pl/api/exchangerates/rates/a/{currency}/{start_date}/{today}/")
    historical_rates = response.json()["rates"]

    dates = [instance["effectiveDate"] for instance in historical_rates]
    rates = [instance["mid"] for instance in historical_rates]

    days = [(datetime.datetime.strptime(date, "%Y-%m-%d").date() - start_date).days for date in dates]

    return days, rates

class Window:

    def __init__(self):
        self.currency = None

    def handle_button_press(self, event):
        rate = get_rate(self.currency.get())
        print(rate)
        self.label.config(text=f"Current rate of {self.currency.get()} is: {rate} PLN")
        self.label.place(x=250, y=110)
        if self.amount_entry.get().isdigit():
            self.label_2.config(text=f"Current cost of {self.amount_entry.get()} {self.currency.get()} is: "
                                     f"{"{:.2f}".format(rate * int(self.amount_entry.get()))} PLN")
            self.label_2.place(x=250, y=90)
        else:
            self.label_2.config(text=f"Please enter the number")
            self.label_2.place(x=250, y=90)

        days, rates = get_historical_data(self.currency.get())

        plt.plot(days, rates)
        plt.title(f"Exchange Rates for {self.currency.get()} in the Last 365 Days")
        plt.xlabel("Days")
        plt.ylabel("Exchange Rate")
        plt.xticks(rotation=45)
        plt.tight_layout()

        plt.show()

    def main(self):
        window = tkinter.Tk()
        window.title("Currency Exchanger")
        window.geometry("500x250")

        button = tkinter.Button(text="GET RATE")
        button.place(x=270, y=10)
        button.bind("<Button-1>", self.handle_button_press)
        button_description = tkinter.Label(window, text="Click this button to calculate rate")
        button_description.place(x=70, y=10)

        options = [
            "AUD", "BGN", "BRL", "CAD", "CHF", "CLP", "CNY", "CZK", "DKK", "EUR", "GBP", "HKD", "HUF",
            "ILS", "INR", "ISK", "JPY", "KRW", "MXN", "MYR", "NOK", "NZD", "PHP", "RON", "SEK", "SGD",
            "TRY", "UAH", "USD", "XDR", "ZAR"
        ]

        self.currency = tkinter.StringVar()
        self.currency.set("EUR"),
        currencies = tkinter.OptionMenu(window, self.currency, *options)
        currencies.place(x=267, y=40)
        self.options_label = tkinter.Label(window, text="Choose the currency").place(x=70, y=40)
        self.label = tkinter.Label(window, text="")

        self.amount_entry = tkinter.StringVar()
        amount_entry = Entry(window, textvariable=self.amount_entry)
        amount_entry.place(x=269, y=70)
        self.amount_entry_label = (tkinter.Label(window, text="Input amount of currency").place(x=70, y=70))

        self.label_2 = tkinter.Label(window, text="")

        window.mainloop()


Window().main()
