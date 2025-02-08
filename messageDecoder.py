import requests
from bs4 import BeautifulSoup
from collections import defaultdict

# This was a program I wrote to decode a message hidden in a google doc, but I have since lost the URL

URL = ''

# Prints the sorted array of the characters and their coorisponding x and y coordinates
def printCode(dataArray, largestY):

    currentY = largestY
    currentX = 0

    # Loops through the sorted array and prints the characters in the correct order
    # prints from top down, left to right
    for x, char, y in dataArray:
        if y == currentY:
            if x == currentX:
                print(char, end='')
            else:
                print(' ' * (int)(x - currentX), end='')
                print(char, end='')
            currentX += (x - currentX) + 1
        else:
            print()
            currentY = y
            currentX = 1
            print(char, end='')

# Fetches the table of data from the URL and calls printCode to print the message
def printCodeFromURL(URL):
    response = requests.get(URL)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Finds all the tables in the html
        tables = soup.find_all('table')

        data = []
        largestY = -1

        # loops through all the found tables and rows
        for table in tables:
            rowCount = 0
            for row in table.find_all('tr'):
                cells = row.find_all(['td', 'th'])
                rowData = [cell.get_text().strip() for cell in cells]

                # added this to skip over the header row
                if rowCount == 0:
                    rowCount = 1
                    continue

                # Breaks down and casts the data into a tuple
                if len(rowData) == 3:
                    x = float(rowData[0])
                    character = rowData[1]

                    y = float(rowData[2])
                    largestY = max(largestY, y)

                    data.append((x, character, y))

        # sort the data by Y value
        groupDataY = defaultdict(list)
        for x, char, y in data:
            groupDataY[y].append((x, char))

        # Sort each Y value by X value
        sortedData = sorted(groupDataY.items(), key=lambda item: item[0], reverse=True)
        finalSorted = []

        # Combine all the sorted data into one array
        for y, items in sortedData:
            sortedByX = sorted(items, key=lambda item: float(item[0]))
            for x, char in sortedByX:
                finalSorted.append((x, char, y))

        printCode(finalSorted, largestY)

    # If the URL is invalid, print an error message
    else:
        return 'Failed to fetch the URL:', response.status_code


printCodeFromURL(URL)
