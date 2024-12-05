import requests
from datetime import datetime, timedelta
import collections

collections.Callable = collections.abc.Callable

def get_uk_bank_holidays(year):
    url = "https://www.gov.uk/bank-holidays.json"
    response = requests.get(url)
    holidays = response.json()['england-and-wales']['events']
    return tuple(datetime.strptime(holiday['date'], "%Y-%m-%d") for holiday in holidays if
                 datetime.strptime(holiday['date'], "%Y-%m-%d").year == year)


# Function to update holidays tuple every year
def update_holidays():
    current_year = datetime.now().year
    next_year = current_year + 1
    holidays = get_uk_bank_holidays(current_year) + get_uk_bank_holidays(next_year)
    return holidays


# Global variable to hold bank holidays
bank_holidays = update_holidays()


def adjust_for_weekends_and_holidays(date, exclude_holidays):
    while date.weekday() >= 5 or (exclude_holidays and date in bank_holidays):
        date += timedelta(days=1)
    return date


def main():
    date_str = input("Enter start date (DD/MM/YYYY): ")
    start_date = datetime.strptime(date_str, "%d/%m/%Y")

    days_to_add = int(input("Enter number of days for reply by date: "))
    reply_by_date = start_date + timedelta(days=days_to_add)

    avoid_weekends_or_holidays = input("Avoid weekends or UK Bank Holidays for reply by date? (y/n): ").lower() == 'y'
    if avoid_weekends_or_holidays:
        reply_by_date = adjust_for_weekends_and_holidays(reply_by_date, True)

    print(f"Reply by Date: {reply_by_date.strftime('%d/%m/%Y')}")

    extra_days = int(input("Enter additional days for post processing: "))
    post_processing_date = reply_by_date + timedelta(days=extra_days)

    avoid_processing_weekends_or_holidays = input(
        "Avoid weekends or UK Bank Holidays for post processing date? (y/n): ").lower() == 'y'
    if avoid_processing_weekends_or_holidays:
        post_processing_date = adjust_for_weekends_and_holidays(post_processing_date, True)

    print(f"Post Processing Date: {post_processing_date.strftime('%d/%m/%Y')}")


if __name__ == "__main__":
    main()
