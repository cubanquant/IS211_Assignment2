import argparse
import urllib.request
import logging
import datetime


# For this assignment, you will be reading data from a file located on the internet. The file is a listing of
# people’s name, their birthdays and an ID number in CSV format. This file, however, has some problems with
# it. Mostly, some of the birthdays are in an invalid format. The other columns in the CSV will be guaranteed to
# be in a proper format, so your code can assume so.
# Using the modules that we learned about, you will design a program to do two things: write an output file
# recording which lines in the file cannot be processed correctly due to an improperly formatted date; and
# allow a user to enter in an ID number and print out that person’s information.

def downloadData(url):
    """Downloads the data"""
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    csvData = response.readlines()
    return csvData
        

def processData(file_content):
    """Processes the data"""
    personData = {}
    for line in file_content:
        line = line.decode('utf-8').rstrip('\n')
        person = line.split(',')
        personData[person[0]] = (person[1], person[2])
    return personData


def displayPerson(id, personData):
    print(f"Person {id} is {personData[id]['name']} with a birthday of {personData[id]['birthday']}")

def main(url):
    print(f"Running main with URL = {url}...")


if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)
