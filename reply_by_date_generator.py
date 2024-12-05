import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import requests
from datetime import datetime, timedelta


# Function to fetch UK bank holidays from the API
def get_uk_bank_holidays(year):
    url = "https://www.gov.uk/bank-holidays.json"
    response = requests.get(url)
    holidays = response.json()['england-and-wales']['events']
    return tuple(datetime.strptime(holiday['date'], "%Y-%m-%d") for holiday in holidays if
                 datetime.strptime(holiday['date'], "%Y-%m-%d").year == year)


# Update global holidays tuple
current_year = datetime.now().year
next_year = current_year + 1
bank_holidays = get_uk_bank_holidays(current_year) + get_uk_bank_holidays(next_year)


def adjust_date(start_date, days_to_add, exclude_weekends=False, exclude_holidays=()):
    date = start_date + timedelta(days=days_to_add)
    if exclude_weekends or exclude_holidays:
        while date.weekday() >= 5 or date in exclude_holidays:
            date += timedelta(days=1)
    return date


class BankHolidayApp(toga.App):
    # Function to handle the user input and compute dates
    def handle_calculation(self, widget):
        start_date_input = self.start_date_input.value
        days_to_add_input = int(self.days_to_add_input.value)
        avoid_weekends_holidays_reply = self.avoid_weekends_holidays_reply_input.value.lower() == 'y'
        post_processing_days = int(self.post_processing_days_input.value)
        avoid_weekends_holidays_processing = self.avoid_weekends_holidays_processing_input.value.lower() == 'y'

        # Parse start date
        start_date = datetime.strptime(start_date_input, "%d/%m/%Y")

        # Calculate reply by date
        reply_by_date = adjust_date(start_date, days_to_add_input, avoid_weekends_holidays_reply, bank_holidays)

        # Calculate post processing date
        post_processing_date = adjust_date(reply_by_date, post_processing_days, avoid_weekends_holidays_processing,
                                           bank_holidays)

        # Display results
        self.reply_by_date_label.text = f"Reply by Date: {reply_by_date.strftime('%d/%m/%Y')}"
        self.processing_date_label.text = f"Post Processing Date: {post_processing_date.strftime('%d/%m/%Y')}"

    def startup(self):
        # Main window
        main_box = toga.Box(style=Pack(direction=COLUMN, padding=10))

        # Start date input
        start_date_box = toga.Box(style=Pack(direction=ROW, padding=5))
        start_date_label = toga.Label('Start Date (DD/MM/YYYY): ', style=Pack(padding=(0, 5)))
        self.start_date_input = toga.TextInput(style=Pack(flex=1))
        start_date_box.add(start_date_label)
        start_date_box.add(self.start_date_input)

        # Days to add input
        days_to_add_box = toga.Box(style=Pack(direction=ROW, padding=5))
        days_to_add_label = toga.Label('Days to Add: ', style=Pack(padding=(0, 5)))
        self.days_to_add_input = toga.TextInput(style=Pack(flex=1))
        days_to_add_box.add(days_to_add_label)
        days_to_add_box.add(self.days_to_add_input)

        # Avoid weekends for reply by date
        avoid_weekends_holidays_reply_box = toga.Box(style=Pack(direction=ROW, padding=5))
        avoid_weekends_holidays_reply_label = toga.Label('Adjust for weekend/ Bank hols? (y/n): ',
                                                         style=Pack(padding=(0, 5)))
        self.avoid_weekends_holidays_reply_input = toga.TextInput(style=Pack(flex=1))
        avoid_weekends_holidays_reply_box.add(avoid_weekends_holidays_reply_label)
        avoid_weekends_holidays_reply_box.add(self.avoid_weekends_holidays_reply_input)

        # Post processing days
        post_processing_days_box = toga.Box(style=Pack(direction=ROW, padding=5))
        post_processing_days_label = toga.Label('Post Processing Days: ', style=Pack(padding=(0, 5)))
        self.post_processing_days_input = toga.TextInput(style=Pack(flex=1))
        post_processing_days_box.add(post_processing_days_label)
        post_processing_days_box.add(self.post_processing_days_input)

        # Avoid weekends for post processing date
        avoid_weekends_holidays_processing_box = toga.Box(style=Pack(direction=ROW, padding=5))
        avoid_weekends_holidays_processing_label = toga.Label('Adjust for weekend/ Bank hols? (y/n): ',
                                                              style=Pack(padding=(0, 5)))
        self.avoid_weekends_holidays_processing_input = toga.TextInput(style=Pack(flex=1))
        avoid_weekends_holidays_processing_box.add(avoid_weekends_holidays_processing_label)
        avoid_weekends_holidays_processing_box.add(self.avoid_weekends_holidays_processing_input)

        # Button to generate dates
        generate_button = toga.Button('Generate Dates', on_press=self.handle_calculation, style=Pack(padding=10))

        # Display labels for results
        self.reply_by_date_label = toga.Label('Reply by Date: ', style=Pack(padding=(5, 0)))
        self.processing_date_label = toga.Label('Post Processing Date: ', style=Pack(padding=(5, 0)))

        main_box.add(start_date_box)
        main_box.add(days_to_add_box)
        main_box.add(avoid_weekends_holidays_reply_box)
        main_box.add(post_processing_days_box)
        main_box.add(avoid_weekends_holidays_processing_box)
        main_box.add(generate_button)
        main_box.add(self.reply_by_date_label)
        main_box.add(self.processing_date_label)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()


def main():
    return BankHolidayApp('Reply by date generator', 'org.example.replybygenerator')


if __name__ == '__main__':
    main().main_loop()
