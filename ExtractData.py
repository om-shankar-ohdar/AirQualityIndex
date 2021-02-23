import os
import time
import requests
import sys


def getHtml():
    for year in range(2013, 2019):
        for month in range(1, 13):
            if month < 10:
                url = 'http://en.tutiempo.net/climate/0{}-{}/ws-421820.html'.format(month, year)
            else:
                url = 'http://en.tutiempo.net/climate/{}-{}/ws-421820.html'.format(month, year)

            sourceText = requests.get(url)
            # the html code has some special characters so we need to get the utf-8 encoding text data
            textUtf = sourceText.text.encode('utf=8')

            # Create folders for each year data
            if not os.path.exists("Data/Html_Data/{}".format(year)):
                os.makedirs("Data/Html_Data/{}".format(year))

            # Write html data for each month
            with open("Data/Html_Data/{}/{}.html".format(year, month), "wb") as output:
                output.write(textUtf)

        sys.stdout.flush()


if __name__ == "__main__":
    startTime = time.time()
    getHtml()
    endTime = time.time()
    print("Time Take : {}".format(endTime - startTime))
