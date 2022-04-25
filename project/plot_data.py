import matplotlib.pyplot as plt
import statistics
import datetime
import time
import csv
from collections import defaultdict
import numpy

'''
Data we are interested in:
Prices
Time Deltas
Trade profits
When NFT was last traded relative to data collection time

Graphs:
Price vs Time delta scatterplot
Trade profit vs Time delta scatterplot
Histogram of trade profits
'''

plt.rcParams.update({'figure.figsize':(7,5), 'figure.dpi':100})
COLLECTION_TIME = 1650829317.1939192

def get_number_of_times_traded(data):
    return [len(line[-1]) for line in data]

def get_stats(data):
    print("STATS")
    print("Min")
    print(min(data))
    print("Max")
    print(max(data))
    print("Mean")
    print(statistics.mean(data))
    print("Median")
    print(statistics.median(data))

def get_prices(data):
    return [float(line[3]) for line in data]

def get_avg_time_deltas_per_trade(data):
    avg_diffs = []
    for line in data:
        sum = 0
        for i in range(1, len(line[-1])):
            sum += (line[-1][i][0] - line[-1][i - 1][0]) / (24 * 3600) # convert to days
        avg_diff = float(sum) / (len(line[-1]) - 1)
        avg_diffs.append(float(avg_diff))
    return avg_diffs

def get_avg_profits_per_trade(data):
    deltas = []
    for line in data:
        sum = 0
        print(line)
        for i in range(1, len(line[-1])):
            sum += line[-1][i][1] - line[-1][i - 1][1]
        avg_delta = float(sum) / (len(line[-1]) - 1)
        deltas.append(float(avg_delta))
    return deltas

def get_time_since_last_traded(data):
    time_diffs = []
    for line in data:
        time_diffs.append((COLLECTION_TIME - line[-1][-1][0]) / (3600 * 24))
    return time_diffs

def cleanData():
    data = []
    with open("../data/new_data.csv", mode="r") as data_file:
        reader = list(csv.reader(data_file))
        for l in reader:
            if (len(l) < 11 or l[4] == "None"):
                continue
            curr_data = []
            curr_data += l[1:5]
            print(curr_data)
            txn_strs = l[9:]
            txns = []
            for s in txn_strs:
                arr = s.split(';')
                try:
                    unix_time = time.mktime(datetime.datetime.strptime(arr[-1], '%b-%d-%Y %I:%M:%S %p +%Z').timetuple())
                except:
                    pass
                txns.append([float(unix_time), float(arr[0])])
            txns = sorted(txns,key=lambda x: (x[0]))
            print(txns)
            curr_data.append(txns)
            data.append(curr_data)
    return data

def box_and_histogram(data, title, xlabel, b=True):
    get_stats(data)
    plt.boxplot(data)
    if (b):
        plt.yscale('log')
    plt.show()

    plt.hist(data, bins=100, log=b)
    plt.gca().set(title=title, xlabel=xlabel, ylabel='Frequency')
    plt.show()

def log_regression(x, y, title, xlabel, ylabel):
    d = defaultdict(list)
    for i in range(len(x)):
        d[x[i]].append(y[i])
    
    convx = []
    convy = []
    for p in d:
        d[p] = sorted(d[p])
        ct = 0
        for i in range(len(d[p]) - 1, -1, -1):
            convx.append(p)
            convy.append(d[p][i])
            ct += 1
            if (ct == 1):
                break
    arr = numpy.polyfit(numpy.log(convx), convy, 1)
    def f(x):
        return arr[0] * numpy.log(x) + arr[1]
    label = 'fit: y = ' + str(arr[0]) + 'log(x) + ' + str(arr[1])
    print("Equation: " + label)
    plt.plot(list(set(x)), f(list(set(x))), 'g--', color='red', label=label)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.scatter(x, y)
    plt.legend(loc='best')
    plt.show()

if __name__ == "__main__":
    clean_data = cleanData()
    for line in clean_data:
        print(line)

    prices = get_prices(clean_data)
    avg_time_deltas_per_nft = get_avg_time_deltas_per_trade(clean_data)
    avg_profits = get_avg_profits_per_trade(clean_data)
    times_since_last_traded = get_time_since_last_traded(clean_data)
    number_of_times_traded = get_number_of_times_traded(clean_data)

    # box_and_histogram(times_since_last_traded, 'Frequencies of Time Since Last Traded', 'Time in Days', False)
    # box_and_histogram(prices, 'NFT Price Frequencies', 'NFT Price in ETH')
    # box_and_histogram(avg_time_deltas_per_nft, 'Time Delta Frequencies', 'Time Delta in Days')
    # box_and_histogram(avg_profits, 'Trade Profit Frequencies', 'Profit in ETH')

    # plt.title("Price of NFT vs Average length of time between trades")
    # plt.xlabel("Price in ETH")
    # plt.ylabel("Average time length between trades in days")
    # plt.scatter(prices, avg_time_deltas_per_nft, )
    # plt.show()

    # plt.title("Average Profit vs Average length of time between trades")
    # plt.xlabel("Profit in ETH")
    # plt.ylabel("Average time length between trades in days")
    # plt.scatter(avg_profits, avg_time_deltas_per_nft)
    # plt.show()

    log_regression(number_of_times_traded, prices, "Number of transactions vs Price in ETH", 
        "Number of transactions", "Prices in ETH")
    log_regression(number_of_times_traded, avg_time_deltas_per_nft, "Number of transactions vs Average time deltas between trades", 
        "Number of transactions", "Average time lengths between trades in days")