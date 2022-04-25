from re import A
import numpy
import csv
import time
import datetime

# y = Alog(x) + B
FUNCTION_A = -108.57585595332759
FUNCTION_B = 293.62987007437505

def final_regression_function(x, A, B):
    return A * numpy.log(x) + B

if __name__ == "__main__":
    with open("../data/test_data.csv", mode="r") as data_file:
        reader = list(csv.reader(data_file))
        num_txns = []
        prices = []
        times = []
        for l in reader:
            if (len(l[-1].split(',')) <= 1):
                continue
            txn_strs = l[-1].split(',')
            num_txns.append(len(txn_strs))
            timestamps = []
            for s in txn_strs:
                arr = s.split(';')
                try:
                    unix_time = time.mktime(datetime.datetime.strptime(arr[-1], '%b-%d-%Y %I:%M:%S %p +%Z').timetuple())
                except:
                    pass
                timestamps.append(float(unix_time))
            timestamps = sorted(timestamps)
            sum = 0
            for i in range(1, len(timestamps)):
                sum += timestamps[i] - timestamps[i - 1]
            times.append((sum / float(len(timestamps) - 1)) / (24 * 3600))
            avg_price = float(l[4])
            prices.append(avg_price)
        ct = 0

        print(len(num_txns))
        print(len(times))
        print(times)
        for i in range(len(num_txns)):
            if final_regression_function(num_txns[i], FUNCTION_A, FUNCTION_B) >= times[i]:
                ct += 1
        print(float(ct) / len(num_txns))