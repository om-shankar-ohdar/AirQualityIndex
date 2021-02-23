import pandas as pd
import matplotlib.pyplot as plt


def getDailyAvgData(year):
    filename = "Data/AQI/aqi" + str(year) + ".csv"
    avg = []
    for rows in pd.read_csv(filename, chunksize=24):
        df = pd.DataFrame(rows)
        df = df['PM2.5']
        df.replace(['NoData', 'PwrFail', '---', 'InVld'], 0, inplace=True)
        df = df.astype(float)
        avg.append(df.mean())
    data = pd.DataFrame(data=avg)
    return data


if __name__ is "__main__":
    data = getDailyAvgData(2013)
    plt.plot(data)