import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from datetime import datetime, timedelta
import requests


class BankHolidayApp(toga.App):

    def startup(self):
        self.main_window = toga.MainWindow(title=self.name)

        # Interface elements
        self.date_input = toga.TextInput(placeholder='Enter start date (DD/MM/YYYY)')
        self.days_to_add_input = toga.NumberInput(min_value=0, step=1)
        self.avoid_reply_weekends_checkbox = toga.CheckBox('Avoid weekends and holidays for reply by date')
        self.extra_days_input = toga.NumberInput(min_value=0, step=1, placeholder='Additional processing days')
        self.avoid_processing_weekends_checkbox = toga.CheckBox('Avoid weekends and holidays for processing date')

        self.calculate_button = toga.Button('Generate Dates', on_press=self.on_calculate_dates)
        self.result_label = toga.Label('Result will be shown here')

        # Layout the interface
        main_box = toga.Box(
            children=[
                toga.Box(children=[toga.Label('Start Date:'), self.date_input], style=Pack(direction=ROW, padding=5)),
                toga.Box(children=[toga.Label('Days to Add:'), self.days_to_add_input],
                         style=Pack(direction=ROW, padding=5)),
                toga.Box(children=[self.avoid_reply_weekends_checkbox], style=Pack(direction=ROW, padding=5)),
                toga.Box(children=[toga.Label('Additional Days:'), self.extra_days_input],
                         style=Pack(direction=ROW, padding=5)),
                toga.Box(children=[self.avoid_processing_weekends_checkbox], style=Pack(direction=ROW, padding=5)),
                self.calculate_button,
                self.result_label
            ],
            style=Pack(direction=COLUMN, padding=10)
        )

        self.main_window.content = main_box
        self.main_window.show()

    def get_uk_bank_holidays(self):
        year = datetime.now().year
        url = f"https://www.gov.uk/bank-holidays.json"
        response = requests.get(url)
        holidays = response.json()['england-and-wales']['events']
        return set(datetime.strptime(holiday['date'], "%Y-%m-%d") for holiday in holidays if
                   datetime.strptime(holiday['date'], "%Y-%m-%d").year in {year, year + 1})

    def adjust_date(self, date, exclude_weekends=False, exclude_holidays=()):
        while (exclude_weekends and date.weekday() >= 5) or (date in exclude_holidays):
            date += timedelta(days=1)
        return date

    def on_calculate_dates(self, widget):
        try:
            start_date = datetime.strptime(self.date_input.value, '%d/%m/%Y')
            days_to_add = int(self.days_to_add_input.value)
            holidays = self.get_uk_bank_holidays()

            # Calculate reply by date
            reply_by_date = start_date + timedelta(days=days_to_add)

            if self.avoid_reply_weekends_checkbox.is_checked:
                reply_by_date = self.adjust_date(reply_by_date, exclude_weekends=True, exclude_holidays=holidays)

            # Add post-processing days
            extra_days = int(self.extra_days_input.value)
            post_processing_date = reply_by_date + timedelta(days=extra_days)

            if self.avoid_processing_weekends_checkbox.is_checked:
                post_processing_date = self.adjust_date(post_processing_date, exclude_weekends=True,
                                                        exclude_holidays=holidays)

            # Present the results
            self.result_label.text = (
                f'Reply by Date: {reply_by_date.strftime("%d/%m/%Y")}, '
                f'Processing Date: {post_processing_date.strftime("%d/%m/%Y")}'
            )

        except ValueError:
            self.result_label.text = 'Error: Invalid date format.'
        except Exception as e:
            self.result_label.text = f'Error: {e}'


def main():
    return BankHolidayApp('Bank Holiday Manager', 'org.beeware.examples.bankholiday')


if __name__ == '__main__':
    main().main_loop()
