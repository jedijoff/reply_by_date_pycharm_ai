import requests
from datetime import datetime, timedelta


# Function to get UK bank holidays for a specific year
def get_uk_bank_holidays(year):
    url = "https://www.gov.uk/bank-holidays.json"
    response = requests.get(url)
    holidays = response.json()['england-and-wales']['events']
    return tuple(
        datetime.strptime(holiday['date'], "%Y-%m-%d") for holiday in holidays if holiday['date'].startswith(str(year)))


# Initialize holidays for the current and next year
def update_holidays():
    current_year = datetime.now().year
    next_year = current_year + 1
    holidays = get_uk_bank_holidays(current_year) + get_uk_bank_holidays(next_year)
    return holidays


# Initialize the global holidays variable
bank_holidays = update_holidays()


def get_next_working_day(date, exclude_holidays, avoid_weekends=True):
    while avoid_weekends and (date.weekday() >= 5 or date in exclude_holidays):
        date += timedelta(days=1)
    return date


def main():
    date_str = input("Enter start date (DD/MM/YYYY): ")
    start_date = datetime.strptime(date_str, "%d/%m/%Y")

    days_to_add = int(input("Enter number of days to add: "))
    reply_by_date = start_date + timedelta(days=days_to_add)

    avoid_holidays = input("Avoid landing on weekends or UK Bank Holidays for reply by date? (y/n): ").lower() == 'y'
    if avoid_holidays:
        reply_by_date = get_next_working_day(reply_by_date, bank_holidays)

    extra_days = int(input("Enter additional days for post processing: "))
    processing_date = reply_by_date + timedelta(days=extra_days)

    avoid_holidays_processing = input("Avoid weekends or holidays for processing date? (y/n): ").lower() == 'y'
    if avoid_holidays_processing:
        processing_date = get_next_working_day(processing_date, bank_holidays)

    print(f"Reply by Date: {reply_by_date.strftime('%d/%m/%Y')}")
    print(f"Processing Date: {processing_date.strftime('%d/%m/%Y')}")


if __name__ == "__main__":
    main()
