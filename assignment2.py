import argparse
import urllib.request
import logging
import datetime

def downloadData(url):
    """Downloads the data"""
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        file_content = response.read()

def processData(file_content):
    for line in file_content:
        print(line)


def displayPerson(id, personData):
    pass

def main(url):
    print(f"Running main with URL = {url}...")


if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)
