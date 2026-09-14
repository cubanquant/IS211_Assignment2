import argparse
import csv
import datetime
import io
import logging
import urllib.request

def downloadData(url):
    """
    Download CSV data from a URL and returns the data as a string

    :param url: URL to the CSV data
    :return: CSV data as a string
    """
    # read the URL
    with urllib.request.urlopen(url) as response:
        response = response.read().decode('utf-8')

    # return the data
    return response


def processData(file_content):
    """
    Process CSV data and return a dictionary mapping each valid ID to a tuple containing the person's name and birthday.

    :param file_content: CSV data as a string
    :return: Dictionary mapping IDs to (name, birthday) tuples
    """
    # Create a dictionary to store the processed data
    personData = {}
    logger = logging.getLogger("assignment2")

    # Make the downloaded string readable by csv.reader
    csv_file = io.StringIO(file_content)
    reader = csv.reader(csv_file)

    # Skip the header: id, name, birthday
    next(reader)

    # The first data record is on physical line 2.
    for line_number, row in enumerate(reader, start=2):
        person_id = int(row[0])
        name = row[1]
        birthday_string = row[2]

        try:
            birthday = datetime.datetime.strptime(
                birthday_string,
                "%d/%m/%Y"
            )

            personData[person_id] = (name, birthday)

        except ValueError:
            logger.error(
                "Error processing line #%s for ID #%s",
                line_number,
                person_id
            )

    return personData


def displayPerson(id, personData):
    """
    Display the information belonging to the requested ID.
    """
    if id not in personData:
        print("No user found with that id")
    else:
        name, birthday = personData[id]
        formatted_birthday = birthday.strftime("%Y-%m-%d")

        print(
            f"Person #{id} is {name} with a birthday of "
            f"{formatted_birthday}"
        )


def main(url):
    """
    Download and process the data, then repeatedly ask the user
    for an ID.
    """
    try:
        csvData = downloadData(url)

    except Exception as error:
        print(f"Error downloading data: {error}")
        return

    # Configure the required logger.
    logger = logging.getLogger("assignment2")
    logger.setLevel(logging.ERROR)

    # Prevent duplicate handlers if main() is called more than once.
    if not logger.handlers:
        file_handler = logging.FileHandler(
            "error.log",
            mode="w"
        )
        file_handler.setLevel(logging.ERROR)

        # Only place the required message in the log.
        formatter = logging.Formatter("%(message)s")
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

    personData = processData(csvData)

    while True:
        try:
            user_id = int(input("Enter an ID to look up: "))

            if user_id <= 0:
                break

            displayPerson(user_id, personData)

        except ValueError:
            print("Please enter a valid whole number.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download and search birthday information."
    )

    parser.add_argument(
        "--url",
        help="URL to the birthday CSV data file",
        type=str,
        required=True
    )

    args = parser.parse_args()
    main(args.url)

  
