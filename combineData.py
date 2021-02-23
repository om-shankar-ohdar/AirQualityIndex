from getAQI import getDailyAvgData
import requests
import pandas as pd
import os
from bs4 import BeautifulSoup


def getMetadata(month, year):
    htmlFile = open('Data/Html_Data/{}/{}.html'.format(year, month), "rb")
    totalText = htmlFile.read()
    tempData = []
    finalData = []

    soup = BeautifulSoup(totalText, "lxml")
    for table in soup.findAll('table', {'class': 'medias mensuales numspan'}):
        for tBody in table:
            for tr in tBody:
                trData = tr.get_text()
                tempData.append(trData)

    numberOfRows = len(tempData) // 15

    for rowData in range(numberOfRows):
        tempRowData = []
        for i in range(15):
            tempRowData.append(tempData[0])
            tempData.pop(0)
        finalData.append(tempRowData)

    df = pd.DataFrame.from_records(finalData)
    df = pd.DataFrame(df.values[1:])
    df.drop(df.tail(1).index, inplace=True)
    df.drop(columns=[0, 6, 10, 11, 12, 13, 14], inplace=True)

    return df


def combineData():
    data = pd.DataFrame()
    for year in range(2013, 2019):
        fileName = "Data/FinalData/yearlyData_{}.csv".format(year)
        dataFrame = pd.read_csv(fileName)
        if data.empty:
            data = pd.DataFrame(dataFrame)
        else:
            data = data.append(dataFrame, ignore_index=True)
    data.drop(data.columns[0], axis=1, inplace=True)
    data.to_csv("Data/FinalData/FinalData.csv")


if __name__ == '__main__':
    if not os.path.exists("Data/FinalData"):
        os.mkdir("Data/FinalData")

    # To make yearly Data
    for year in range(2013, 2019):
        finalData = pd.DataFrame()
        for month in range(1, 13):
            temp = getMetadata(month, year)
            if finalData.empty:
                finalData = pd.DataFrame(temp)
            else:
                finalData = finalData.append(temp, ignore_index=True)
        pm = getDailyAvgData(year)
        if len(pm) == 364:
            pm.loc[364] = ''
        finalData['PM 2.5'] = pm
        finalData.columns = ['T', 'TM', 'Tm', 'SLP', 'H', 'VV', 'V', 'VM', 'PM 2.5']
        finalData = finalData[(finalData != '').all(axis=1)]
        finalData = finalData[(finalData != '-').all(axis=1)]
        fileName = "Data/FinalData/yearlyData_{}.csv".format(year)
        finalData.to_csv(fileName)

    # To make final csv data
    combineData()
