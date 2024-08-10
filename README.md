# Google-Flight-Web-Scraping

- Design to collect flight information, reformat variables and save data for easiness in analysis, package used 
including Selenium and Beautiful Soup.
- Data comes from Google Flight scraped on August 9, 2024; flight data may change after.

## Variables

- **Fixed Variables:** Economy class, 1 person, one-way ticket, departure city (Toronto), and arrival city (Vancouver).
- **Date Range:** Flight data collected for dates from August 19, 2024, to August 24, 2024 (Monday to Friday).
- **Dataset Variables:**
  - `departure time`: Time of departure (local time in 24-hour format).
  - `arrival time`: Time of arrival (local time in 24-hour format).
  - `date change`: Number of days changed during the flight according to local time of departure and arrival.
  - `departure airport`: IATA code of the departure airport.
  - `arrival airport`: IATA code of the arrival airport.
  - `price`: Ticket price in the CAD.
  - `airline`: List of airlines operating the flight, converted to IATA codes, possible to represent same airline 
multiple times. Airlines will be present as what is on the html of the web page with only their names abbreviated.
  - `airline count`: Number of distinct airlines operating the flight.
  - `stop airport`: IATA code of the stop airport (if applicable, possible to be NA).
  - `stop count`: Number of stops during the flight.
  - `overhead bin access`: 1 if access to the overhead bin is available, 0 if not.
  - `day`: Index of the day in the week (1 for Monday, 2 for Tuesday, and so on).


