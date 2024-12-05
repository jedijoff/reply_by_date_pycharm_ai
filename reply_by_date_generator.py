import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

import requests
from datetime import datetime, timedelta


class BankHolidayApp(toga.App):

    def startup(self):
        # Setup the main window of the app
        self.main_window = toga.MainWindow(title=self.name)

        # Create date input, number of days input and the main button
        self.date_input = toga.TextInput(placeholder='Enter start date (DD/MM/YYYY)')
        self.days_to_add_input = toga.NumberInput(min_value=0, step=1)
        self.result_label = toga.Label('Result will be shown here')

        self.add_button = toga.Button('Calculate Dates', on_press=self.on_calculate_dates)

        # Use a container to hold everything
        box = toga.Box(
            children=[
                toga.Box(children=[toga.Label('Start Date:'), self.date_input], style=Pack(direction=ROW, padding=5)),
                toga.Box(children=[toga.Label('Days to Add:'), self.days_to_add_input],
                         style=Pack(direction=ROW, padding=5)),
                self.add_button,
                self.result_label
            ],
            style=Pack(direction=COLUMN, padding=10)
        )

        # Add the box to the main window
        self.main_window.content = box
        self.main_window.show()

    def get_uk_bank_holidays(self, year):
        url = f"https://www.gov.uk/bank-holidays.json"
        response = requests.get(url)
        holidays = response.json()['england-and-wales']['events']
        return set(datetime.strptime(holiday['date'], "%Y-%m-%d") for holiday in holidays if
                   datetime.strptime(holiday['date'], "%Y-%m-%d").year in (year, year + 1))

    def adjust_date(self, date, exclude_weekends=False, exclude_holidays=()):
        while exclude_weekends and date.weekday() >= 5 or date in exclude_holidays:
            date += timedelta(days=1)
        return date

    def on_calculate_dates(self, widget):
        try:
            start_date = datetime.strptime(self.date_input.value, '%d/%m/%Y')
            days_to_add = int(self.days_to_add_input.value)

            holidays = self.get_uk_bank_holidays(start_date.year)

            # Calculate Reply by Date
            reply_by_date = start_date + timedelta(days=days_to_add)

            # Check if the reply date must avoid weekends or holidays
            avoid_reply_weekends = toga.dialogs.ok_cancel_dialog('Avoid weekends or holidays for reply by date?',
                                                                 parent=self.main_window)
            if avoid_reply_weekends:
                reply_by_date = self.adjust_date(reply_by_date, exclude_weekends=True, exclude_holidays=holidays)

            # Process additional post-processing days
            extra_days = toga.NumberInput(prompt='Any additional days for processing?', parent=self.main_window)
            post_processing_date = reply_by_date + timedelta(days=int(extra_days.value))

            # Check if the processing date must avoid weekends or holidays
            avoid_post_processing_weekends = toga.dialogs.ok_cancel_dialog(
                'Avoid weekends or holidays for processing date?', parent=self.main_window)
            if avoid_post_processing_weekends:
                post_processing_date = self.adjust_date(post_processing_date, exclude_weekends=True,
                                                        exclude_holidays=holidays)

            # Show the results
            self.result_label.text = f'Reply by Date: {reply_by_date.strftime("%d/%m/%Y")}, Processing Date: {post_processing_date.strftime("%d/%m/%Y")}'

        except Exception as e:
            self.result_label.text = f'Error: {e}'


def main():
    return BankHolidayApp('Bank Holiday Manager', 'org.beeware.examples.bankholiday')


if __name__ == '__main__':
    main().main_loop()
