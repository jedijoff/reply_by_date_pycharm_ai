import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from datetime import datetime, timedelta
import requests


def get_uk_bank_holidays(year):
    url = "https://www.gov.uk/bank-holidays.json"
    response = requests.get(url)
    holidays = response.json()['england-and-wales']['events']
    return [
        datetime.strptime(holiday['date'], "%Y-%m-%d").date()
        for holiday in holidays if datetime.strptime(holiday['date'], "%Y-%m-%d").year == year
    ]


class UKBankHolidayApp(toga.App):
    def startup(self):
        self.main_box = toga.Box(style=Pack(direction=COLUMN, padding=10))

        self.date_input = toga.TextInput(placeholder='Enter Start Date (dd/mm/yyyy)', style=Pack(flex=1))
        self.days_to_add_input = toga.NumberInput(min_value=0, placeholder='Days to Add', style=Pack(flex=1))
        self.avoid_weekends_holidays = toga.Switch('Avoid Weekends & UK Bank Holidays for Reply Date')
        self.process_days_input = toga.NumberInput(min_value=0, placeholder='Post Processing Days', style=Pack(flex=1))
        self.avoid_weekends_holidays_process = toga.Switch('Avoid Weekends & UK Bank Holidays for Processing Date')

        self.generate_button = toga.Button('Generate Dates', on_press=self.generate_dates, style=Pack(padding_top=20))

        self.result_label = toga.Label('', style=Pack(padding_top=10))

        self.main_box.add(self.date_input)
        self.main_box.add(self.days_to_add_input)
        self.main_box.add(self.avoid_weekends_holidays)
        self.main_box.add(self.process_days_input)
        self.main_box.add(self.avoid_weekends_holidays_process)
        self.main_box.add(self.generate_button)
        self.main_box.add(self.result_label)

        self.main_window = toga.MainWindow(title=self.name)
        self.main_window.content = self.main_box
        self.main_window.show()

    def generate_dates(self, widget):
        try:
            start_date = datetime.strptime(self.date_input.value, "%d/%m/%Y").date()
            days_to_add = int(self.days_to_add_input.value)
            add_process_days = int(self.process_days_input.value)

            # Initialize holidays for the current year and next year
            current_year = start_date.year
            next_year = current_year + 1

            holidays = set(get_uk_bank_holidays(current_year) + get_uk_bank_holidays(next_year))

            reply_by_date = start_date + timedelta(days=days_to_add)

            if self.avoid_weekends_holidays.value:
                while reply_by_date.weekday() >= 5 or reply_by_date in holidays:
                    reply_by_date += timedelta(days=1)

            processing_date = reply_by_date + timedelta(days=add_process_days)

            if self.avoid_weekends_holidays_process.value:
                while processing_date.weekday() >= 5 or processing_date in holidays:
                    processing_date += timedelta(days=1)

            self.result_label.text = f"Reply by Date: {reply_by_date}\nProcessing Date: {processing_date}"

        except Exception as e:
            self.result_label.text = f"Error: {e}"


def main():
    return UKBankHolidayApp('UK Bank Holiday Processor', 'org.beeware.ukbankholiday')


if __name__ == '__main__':
    main().main_loop()
