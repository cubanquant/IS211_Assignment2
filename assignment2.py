import argparse
import urllib.request
import logging
import datetime

LOG_FILENAME = 'error.log'
logging.basicConfig(
    filename=LOG_FILENAME,
    level=logging.DEBUG,
)


def downloadData(url):
    """Downloads the data"""
    content = urllib.request.urlopen(url).read().decode('utf-8')
    return content


def processData(file_content):
    person_data = dict()

    for i, line in enumerate(file_content.split("\n")):
        if i == 0:
            # skip the header
            continue
        if len(line) == 0:
            # skip blank lines
            continue

        elements = line.split(",")
        id = int(elements[0])
        name = elements[1]
        try:
            birthday = datetime.datetime.strptime(elements[2], "%d/%m/%Y")
        except ValueError:
            logging.error(f"Error processing line #{i} for ID #{id}")

        person_data[id] = (name, birthday)

    return person_data


def displayPerson(id, personData):
    try:
        name, birthday = personData[id]
        print(f"Person #{id} is {name} with a birthday of {birthday:%Y-%m-%d}")
    except KeyError:
        print(f"No user found with that id")


def main(url):
    print(f"Running main with URL = {url}...")
    content = downloadData(url)
    personData = processData(content)
    while True:
        id = int(input("Enter an ID:"))
        if id < 0:
            break
        displayPerson(id, personData)


if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)
