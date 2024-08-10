import re

from selenium import webdriver
from bs4 import BeautifulSoup
import time
from datetime import datetime

import csv

# Abbreviated according to the IATA airline code
airline_dict = {
    "Air Canada": "AC",
    "WestJet": "WS",
    "Porter Airlines": "PD",
    "Flair Airlines": "F8",
    "Porter AirlinesAir Transat": "PD, TS",
    "Air CanadaOperated by Air Canada Express - Jazz": "AC(Jazz)",
    "Air Canada Express - Jazz": "AC(Jazz)",
    "Air CanadaOperated by Air Canada Rouge": "AC(Rouge)",
    "Air Canada Rouge": "AC(Rouge)",
    "Porter AirlinesOperated by Porter Airlines Inc": "PD(Inc)",
    "Porter Airlines Inc": "PD(Inc)",
    "Air Canada Express - Pal Airlines": "AC(Pal)",
    "Air CanadaOperated by Air Canada Express - Pal Airlines": "AC(Pal)",
    "WestJetOperated by Westjet Encore": "WS(Encore)",
    "WestJetAir Transat": "WS, TS",
    "Westjet Encore": "WS(Encore)",
    "Air Transat": "TS",
    "WestJetOperated by Air Canada Rouge": "WS, AC(Rouge)"
}

# File title
csv_title = ["departure time", "arrival time", "date change", "departure airport", "arrival airport", "price",
             "airline", "distinct airline count", "stop airport", "stop count", "overhead bin access", "day"]

csv_filename = 'flight_info.csv'


# Functions

def str_to_int(num):
    if len(num) == 5:
        return int(num[:1] + num[2:])
    else:
        return int(num)


def convert_time(time_str):
    # Split the time and the additional info
    if '+' in time_str:
        time_part, add_info = time_str.split('+')
        add_info = int(add_info)
    else:
        time_part = time_str
        add_info = 0

    # Convert to 24-hour format if it is PM
    if 'PM' in time_part:
        time_part = datetime.strptime(time_part.strip('\u202fPM'), '%I:%M').strftime('%H:%M')
        temp = time_part[:2]
        temp = int(temp) + 12
        time_part = str(temp) + time_part[2:]
    else:
        time_part = datetime.strptime(time_part.strip('\u202fAM'), '%I:%M').strftime('%H:%M')

    return [time_part, add_info]


def convert_stop(stop_str):
    if stop_str == "Nonstop":
        return [0, ""]
    stop_n = int(stop_str[:1])
    if stop_n == 1:
        temp = stop_str[10:]
    else:
        temp = stop_str[11:]
    return [stop_n, temp]


def convert_airline(airline_str):
    air_lst = airline_str.split(",")
    return_air = ""
    for a in air_lst:
        a = a.strip()
        return_air += (airline_dict[a] + ", ")
    return return_air[:-2]


# Start with file writer
with open(csv_filename, mode='a', newline="") as file:
    writer = csv.writer(file)
    writer.writerow(csv_title)

    # Setup Selenium WebDriver

    driver = webdriver.Chrome()  # Make sure you have the ChromeDriver installed and in your PATH
    url_change_lst = ['E5', 'Iw', 'Ix', 'Iy', 'Iz']

    # Open the website
    for i in range(5):
        url = (f"https://www.google.com/travel/flights/search?tfs=CBwQAhooEgoyMDI0LTA4LT{url_change_lst[i]}agwI" +
               f"AhIIL20vMGg3aDZyDAgDEggvbS8wODBoMkABSAFwAYIBCwj___________8BmAEC&tfu=EgYIABABGAA&hl=en-US")

        driver.get(url)
        # Wait for the page to load completely (you may need to adjust the wait time or conditions)
        time.sleep(5)  # wait for up to 10 seconds

        # Get the page source
        html = driver.page_source

        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # Now you can use BeautifulSoup to find elements

        departure_time = []
        arrival_time = []
        date_changed = []
        departure_airport = []
        arrival_airport = []
        price_list = []
        airline_list = []
        stop_info = []
        stop_count = []
        bin_access = []
        airline_count = []
        day_index = []

        time_depart = soup.findAll("div", attrs={"class": "wtdjmc YMlIz ogfYpf tPgKwe"})
        time_arrive = soup.findAll("div", attrs={"class": "XWcVob YMlIz ogfYpf tPgKwe"})
        airport_depart = soup.findAll("div", attrs={"class": "G2WY5c sSHqwe ogfYpf tPgKwe"})
        airport_arrive = soup.findAll("div", attrs={"class": "c8rWCd sSHqwe ogfYpf tPgKwe"})
        price = soup.findAll("div", attrs={"class": "BVAVmf tPgKwe"}, class_=re.compile(r"YMlIz FpEdX( jLMuyc)?"))
        overhead_bin = soup.findAll("div", attrs={"class": "JMnxgf"})
        airline = soup.findAll("span", attrs={"class": "h1fkLb"})
        stop = soup.findAll("span", attrs={"class": "rGRiKd"})

        unique_prices = []
        seen_data_gs = set()

        for t1 in time_depart:
            t_string = t1.text.strip()
            t_list = convert_time(t_string)
            departure_time.append(t_list[0])
            day_index.append(i + 1)
        for t2 in time_arrive:
            t_string = t2.text.strip()
            t_list = convert_time(t_string)
            arrival_time.append(t_list[0])
            date_changed.append(t_list[1])
        for a1 in airport_depart:
            departure_airport.append(a1.text.strip())
        for a2 in airport_arrive:
            arrival_airport.append(a2.text.strip())
        for p in price:
            span = p.find("span")
            txt = p.text
            data_gs = span['data-gs']
            if data_gs not in seen_data_gs:
                seen_data_gs.add(data_gs)
                unique_prices.append(str_to_int(txt[3:]))
        for air in airline:
            air_txt = convert_airline(air.text.strip())
            airline_list.append(air_txt)
            lst_air = air_txt.split(',')
            lst_distinct = []
            for l in lst_air:
                if l not in lst_distinct:
                    lst_distinct.append(l)
            airline_count.append(len(lst_distinct))
        for s in stop:
            s_info = convert_stop(s.text.strip())
            stop_info.append(s_info[1])
            stop_count.append(s_info[0])
        for b in overhead_bin:
            temp = str(b)[:-6]
            temp = temp[20:]
            if temp == "":
                bin_access.append(1)
            else:
                bin_access.append(0)
        bin_info = []
        for i in range(0, len(bin_access), 3):
            bin_info.append(bin_access[i])
        # both departure time and arrival time are based on local time

        summation = []
        for i in range(len(airport_arrive)):
            summation.append(
                [departure_time[i], arrival_time[i], date_changed[i], departure_airport[i], arrival_airport[i],
                 unique_prices[i], airline_list[i], airline_count[i], stop_info[i], stop_count[i], bin_info[i],
                 day_index[i]])

        sorted_summation = sorted(summation, key=lambda x: x[5])

        for row in sorted_summation:
            writer.writerow(row)

    driver.quit()
