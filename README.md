This is a QT version of the same script, also AI generated using PyCharm's AI assistant.

The AI input was: 

"Create a Python QT script that imports UK bank holidays for current year and the following one and stores them in a tuple, which is updated on 1 January each year. Then the script is to take a user input date in the format day/month/year. It will then request how many days to add for the reply by date which it will add straight away without avoiding weekends. It will then ask if the reply by date must not land on a weekend or UK bank holiday, so after the days added have been added if the result is a weekend or bank holiday it will add one day and then recheck to see if that is a weekend or bank holiday and add 1 day if necessary until the result is not a weekend or bank holiday, for example if the reply by date results as 25 December 2024 it should change the date to 27 December 2024. The script will then ask if any days need to be added for post processing. once these days are added it will ask if this needs to avoid landing on a weekend or UK bank holiday, if so it will automatically adjust to the next working day eg if it lands on a Saturday it should move to the next available Monday. Finally it will print the reply by date and Post processing date to the screen."

This current version is working on Mac OS.
