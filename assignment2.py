import argparse
from unicodedata import name
import urllib.request
import logging
from datetime import datetime

# url = 'http://s3.amazonaws.com/cuny-is211-spring2015/birthdays100.csv'
# For this assignment, you will be reading data from a file located on the internet. The file is a listing of
# people’s name, their birthdays and an ID number in CSV format. This file, however, has some problems with
# it. Mostly, some of the birthdays are in an invalid format. The other columns in the CSV will be guaranteed to
# be in a proper format, so your code can assume so.
# Using the modules that we learned about, you will design a program to do two things: write an output file
# recording which lines in the file cannot be processed correctly due to an improperly formatted date; and
# allow a user to enter in an ID number and print out that person’s information.


logger = logging.getLogger(__name__)  
logger.setLevel(logging.ERROR)

file_handler = logging.FileHandler('error.log')
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

logger.error('Invalid birthday format')



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
        name = person[1]
        id = person[0]
        birthday = person[2]
        try:
            birthday = datetime.strptime(person[2], '%d/%m/%Y')
        except ValueError:
            logger.error(f"Error processing line {line} for ID #{person[0]}")
        else:
            personData[id] = (name, birthday)
    return personData


def displayPerson(id, personData):
    """Displays the person"""
    if id in personData:
        print(f"Person {id} is {personData[id][0]} with a birthday of {personData[id][1]}")
    else:
        print("No user found with that id")

def main(url):
    print(f"Running main with URL = {url}...")
    csvData = downloadData(url)
    personData = processData(csvData)
    while True:
        id = input("Enter an ID number: ")
        if id == "exit":
            break
        displayPerson(id, personData)
        print('Type "exit" to quit')


if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)
