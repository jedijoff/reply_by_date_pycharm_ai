from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import QDate
import requests
from datetime import datetime, timedelta

def fetch_uk_bank_holidays(year):
    url = "https://www.gov.uk/bank-holidays.json"
    response = requests.get(url)
    holidays = response.json()['england-and-wales']['events']
    return set(datetime.strptime(holiday['date'], "%Y-%m-%d").date() for holiday in holidays if
               int(holiday['date'].split('-')[0]) in [year, year + 1])


class HolidayChecker(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("UK Bank Holidays Checker")
        self.setGeometry(100, 100, 400, 250)
        self.current_year = datetime.now().year
        self.holidays = fetch_uk_bank_holidays(self.current_year)

        self.layout = QVBoxLayout()

        self.date_label = QLabel("Enter date (DD/MM/YYYY):")
        self.date_input = QLineEdit()

        self.days_label = QLabel("Days to add for reply:")
        self.days_input = QLineEdit()

        self.avoid_label = QLabel("Avoid weekends and UK bank holidays for reply? (y/n):")
        self.avoid_input = QLineEdit()

        self.processing_days_label = QLabel("Days to add for post-processing:")
        self.processing_days_input = QLineEdit()

        self.avoid_processing_label = QLabel("Avoid weekends and holidays for post-processing? (y/n):")
        self.avoid_processing_input = QLineEdit()

        self.result_button = QPushButton("Calculate")
        self.result_button.clicked.connect(self.calculate_dates)

        self.layout.addWidget(self.date_label)
        self.layout.addWidget(self.date_input)
        self.layout.addWidget(self.days_label)
        self.layout.addWidget(self.days_input)
        self.layout.addWidget(self.avoid_label)
        self.layout.addWidget(self.avoid_input)
        self.layout.addWidget(self.processing_days_label)
        self.layout.addWidget(self.processing_days_input)
        self.layout.addWidget(self.avoid_processing_label)
        self.layout.addWidget(self.avoid_processing_input)
        self.layout.addWidget(self.result_button)

        self.setLayout(self.layout)

    def adjust_date(self, date, avoid_weekends_holidays):
        while date.weekday() >= 5 or date in self.holidays:
            date += timedelta(days=1)
        return date

    def calculate_dates(self):
        date_str = self.date_input.text()
        days_to_add = int(self.days_input.text())
        avoid_reply = self.avoid_input.text().lower() == 'y'
        extra_processing_days = int(self.processing_days_input.text())
        avoid_processing = self.avoid_processing_input.text().lower() == 'y'

        try:
            date = datetime.strptime(date_str, "%d/%m/%Y").date()
        except ValueError:
            QMessageBox.warning(self, "Input Error", "The date format should be DD/MM/YYYY")
            return

        reply_by_date = date + timedelta(days=days_to_add)

        if avoid_reply:
            reply_by_date = self.adjust_date(reply_by_date, avoid_reply)

        processing_date = reply_by_date + timedelta(days=extra_processing_days)

        if avoid_processing:
            processing_date = self.adjust_date(processing_date, avoid_processing)

        QMessageBox.information(
            self,
            "Results",
            f"Reply By Date: {reply_by_date.strftime('%d/%m/%Y')}\n"
            f"Processing Date: {processing_date.strftime('%d/%m/%Y')}"
        )


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = HolidayChecker()
    window.show()
    sys.exit(app.exec_())
