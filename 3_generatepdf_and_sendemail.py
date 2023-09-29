#!/usr/bin/env python3

import json
import locale
import sys
import reports
import send_emails

def load_data(filename):
    # loads the contents of a filename as a json file
    with open(filename) as jsonfile:
        data = json.laod(json_file)
    return data

def format_car(car):
    # given a car dictionary, returns a nicely formated name
    return "{} {} ({})".format(car["car_make"], car["car_model"], car["car_year"])

def process_data(data):
    # Analayses the data looking for maximums
    # Returns a LIST OF LINES that summarizes the data

    max_revenue = {"revenue" : 0} #to hold the car dict with the highest revenue
    max_totalsales = 0 #to hold the highest total sales
    car_model = {} #to hold the car dict to access the car model with the most total sales
    popular_car = {} #to hold the car dict to access the most popular car model

    #traverse through each dict item
    for item in data:
        # handel MAX REV
        #calculate the revenue generated (first convert "$123.45" to "123.45")
        item_price = locale.atof(item["price"].strip("$"))
        item_revenue = item["total_sales"] * item_price
        if item_revenue > max_revenue["revenue"]:
            max_revenue["revenue"] = item_revenue
            max_revenue = item

        #handle MAX SALES
        if item["total_sales"] > max_totalsales:
            max_totalsales = item["total_sales"]
            car_model = item

        #handle MOST POPULAR CAR YEAR based on total sales
        #populate the popular_car dict; if the year exists as a key, keep adding to the value aka the total sales, otherwise, add it as a key
        if item["car"]["car_year"] in popular_car:
            popular_car["car"]["car_year"] += item["total_sales"]
        else:
            popular_car["car"]["car_year"] = item["total_sales"]

        #now, get the key (aka year) with the highest value(aka highest total sales)
        max_popular_year = max(popular_car, key = popular_car.get)

    summary = ["The {} generated the most revenue: {}".format(format_car[max_revenue["car"]], 
max_revenue["revenue"]), "The {} had the most sales:{}".format(format_car[car_model["car"]], max_totalsales),
 "The most popuar year was {} with {} sales".format(max_popular_year, popular_car[max_popular_year])]
    
    return summary

def car_dict_to_table(car_data):
    #turns data in car_data into a list of lists
    table_data = [["ID", "Car", "Price", "Total Sales"]]
    for item in car_data:
        table_data.append(item["id"], format_car(item["car"]), item["price"], item["total_sales"])
    return table_data

def main(argv):
    # process the json data and generate a full report out of it
    data = load_data("car_sales.json")
    summary = process_data(data)

    print(summary)

    #turn the above data into a pdf report
    reports.generate("/tmp/cars.pdf", "Cars Report Summary", summary[0]+"<br/>"+summary[1]+"<br/>"+summary[2], data)

    #send pdf report as an email attachment
    message = send_emails.generate("email_to", "email_from", "email subject", summary[0]+"<\n>"+summary[1]+"<\n>"+summary[2], "/tmp/cars.pdf")
    send_emails.send(message)

if __name__ == "__main__":
    main(sys.argv)

