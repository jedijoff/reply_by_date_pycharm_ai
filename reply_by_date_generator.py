import toga
from toga.style import Pack
from toga.style.pack import COLUMN
import requests
from datetime import datetime, timedelta


class BankHolidayApp(toga.App):
    bank_holidays = ()

    def startup(self):
        self.main_window = toga.MainWindow(title=self.name)

        # Update holidays at startup
        self.update_holidays()

        # Create the input fields and buttons
        self.start_date_input = toga.TextInput(placeholder='Enter start date (DD/MM/YYYY)', style=Pack(flex=1))
        self.days_input = toga.TextInput(placeholder='Enter days to add', style=Pack(flex=1))

        self.avoid_weekends_holidays_input = toga.TextInput(placeholder='Avoid weekends/holidays? (y/n)',
                                                            style=Pack(flex=1))
        self.processing_days_input = toga.TextInput(placeholder='Enter additional processing days', style=Pack(flex=1))
        self.avoid_weekends_holidays_processing_input = toga.TextInput(
            placeholder='Avoid weekends/holidays for processing? (y/n)', style=Pack(flex=1))

        self.generate_button = toga.Button('Generate', on_press=self.on_generate, style=Pack(padding=5))

        # Layout the inputs and button
        main_box = toga.Box(
            children=[
                self.start_date_input,
                self.days_input,
                self.avoid_weekends_holidays_input,
                self.processing_days_input,
                self.avoid_weekends_holidays_processing_input,
                self.generate_button
            ],
            style=Pack(direction=COLUMN, padding=10)
        )

        self.result_label = toga.Label('', style=Pack(padding=5))
        main_box.add(self.result_label)

        self.main_window.content = main_box
        self.main_window.show()

    def update_holidays(self):
        current_year = datetime.now().year
        next_year = current_year + 1
        self.bank_holidays = self.get_uk_bank_holidays(current_year) + self.get_uk_bank_holidays(next_year)

    def get_uk_bank_holidays(self, year):
        url = f"https://www.gov.uk/bank-holidays.json"
        try:
            response = requests.get(url)
            holidays = response.json()['england-and-wales']['events']
        except requests.RequestException as e:
            print(f"Error fetching holidays: {e}")
            holidays = []

        return tuple(datetime.strptime(holiday['date'], "%Y-%m-%d").date() for holiday in holidays if
                     datetime.strptime(holiday['date'], "%Y-%m-%d").year == year)

    def on_generate(self, widget):
        try:
            start_date_str = self.start_date_input.value
            days_to_add = int(self.days_input.value)
            avoid_weekends_holidays = self.avoid_weekends_holidays_input.value.lower() == 'y'

            start_date = datetime.strptime(start_date_str, "%d/%m/%Y").date()

            reply_by_date = self.adjust_date(start_date, days_to_add)
            if avoid_weekends_holidays:
                reply_by_date = self.adjust_for_weekends_and_holidays(reply_by_date)

            extra_days = int(self.processing_days_input.value)
            avoid_weekends_holidays_processing = self.avoid_weekends_holidays_processing_input.value.lower() == 'y'

            processing_date = self.adjust_date(reply_by_date, extra_days)
            if avoid_weekends_holidays_processing:
                processing_date = self.adjust_for_weekends_and_holidays(processing_date)

            self.result_label.text = (
                f"Reply by Date: {reply_by_date.strftime('%d/%m/%Y')}\n"
                f"Processing Date: {processing_date.strftime('%d/%m/%Y')}"
            )
        except Exception as e:
            self.result_label.text = f"Error: {str(e)}"

    def adjust_date(self, start_date, days_to_add):
        return start_date + timedelta(days=days_to_add)

    def adjust_for_weekends_and_holidays(self, date):
        while date.weekday() >= 5 or date in self.bank_holidays:
            date += timedelta(days=1)
        return date


def main():
    return BankHolidayApp('Bank Holiday App', 'com.example.bankholiday')


if __name__ == '__main__':
    main().main_loop()
