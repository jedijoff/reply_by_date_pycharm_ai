from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import QDate
import requests
from datetime import datetime, timedelta


def fetch_uk_bank_holidays():
    current_year = datetime.now().year
    url = "https://www.gov.uk/bank-holidays.json"
    response = requests.get(url)
    holidays = response.json()['england-and-wales']['events']
    return set(datetime.strptime(holiday['date'], "%Y-%m-%d").date() for holiday in holidays
               if int(holiday['date'].split('-')[0]) in [current_year, current_year + 1])


class HolidayChecker(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("UK Bank Holidays Checker")
        self.setGeometry(100, 100, 400, 250)
        self.holidays = fetch_uk_bank_holidays()

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
    from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
    from datetime import datetime, timedelta
    import requests
    import sys


    def get_uk_bank_holidays(year):
        url = f"https://www.gov.uk/bank-holidays.json"
        response = requests.get(url)
        holidays = response.json()['england-and-wales']['events']
        return tuple(datetime.strptime(holiday['date'], "%Y-%m-%d") for holiday in holidays if
                     datetime.strptime(holiday['date'], "%Y-%m-%d").year == year)


    class HolidayApp(QWidget):
        def __init__(self):
            super().__init__()
            self.initUI()
            self.update_holidays()

        def initUI(self):
            self.layout = QVBoxLayout()

            self.date_label = QLabel('Enter start date (DD/MM/YYYY):')
            self.layout.addWidget(self.date_label)

            self.date_input = QLineEdit(self)
            self.layout.addWidget(self.date_input)

            self.add_days_label = QLabel('Enter number of days to add:')
            self.layout.addWidget(self.add_days_label)

            self.add_days_input = QLineEdit(self)
            self.layout.addWidget(self.add_days_input)

            self.calc_button = QPushButton('Calculate Dates', self)
            self.calc_button.clicked.connect(self.calculate_dates)
            self.layout.addWidget(self.calc_button)

            self.result_label = QLabel('')
            self.layout.addWidget(self.result_label)

            self.setLayout(self.layout)
            self.setWindowTitle('Bank Holiday Calculator')

        def update_holidays(self):
            current_year = datetime.now().year
            next_year = current_year + 1
            self.bank_holidays = get_uk_bank_holidays(current_year) + get_uk_bank_holidays(next_year)

        def adjust_date(self, date, avoid_weekends, avoid_holidays):
            while avoid_weekends and date.weekday() >= 5 or date in self.bank_holidays:
                date += timedelta(days=1)
            return date

        def calculate_dates(self):
            try:
                start_date_str = self.date_input.text()
                start_date = datetime.strptime(start_date_str, "%d/%m/%Y")
                days_to_add = int(self.add_days_input.text())

                reply_by_date = start_date + timedelta(days=days_to_add)
                reply_by_date = self.adjust_date(reply_by_date, True, self.bank_holidays)

                QMessageBox.question(self, 'Avoid Bank Holidays?',
                                     'Do you want to avoid UK Bank Holidays and weekends for reply by date?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

                # Adjust the post-processing date
                adjust_reply_by = QMessageBox.Yes
                if adjust_reply_by == QMessageBox.Yes:
                    reply_by_date = self.adjust_date(reply_by_date, True, self.bank_holidays)

                extra_days_input, ok = QMessageBox.getText(self, 'Post processing',
                                                           'Enter additional days for processing:')
                if ok:
                    extra_days = int(extra_days_input)
                    processing_date = reply_by_date + timedelta(days=extra_days)
                    processing_date = self.adjust_date(processing_date, True, self.bank_holidays)

                    self.result_label.setText(
                        f'Reply by Date: {reply_by_date.strftime("%d/%m/%Y")}\nProcessing Date: {processing_date.strftime("%d/%m/%Y")}')
            except Exception as e:
                QMessageBox.warning(self, "Invalid Input", str(e))


    def main():
        app = QApplication(sys.argv)
        ex = HolidayApp()
        ex.show()
        sys.exit(app.exec_())


    if __name__ == '__main__':
        main()

    app = QApplication(sys.argv)
    window = HolidayChecker()
    window.show()
    sys.exit(app.exec_())
