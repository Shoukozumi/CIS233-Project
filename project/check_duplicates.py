import csv


def delete_formatting_mistakes(csv_url, csv_url2):
    data = []
    with open(csv_url, mode='r') as data_file:
        csv_file_reader = csv.reader(data_file, delimiter=',')
        for row in csv_file_reader:
            if row[8] == 'Ethereum':
                data.append(row)

    with open(csv_url2, mode='w') as data_file:
        writer = csv.writer(data_file)
        writer.writerows(data)


def delete_duplicates(csv_url, csv_url2, dupe_rows):
    data = []
    with open(csv_url, mode='r') as data_file:
        csv_file_reader = csv.reader(data_file, delimiter=',')
        counter = 0
        for row in csv_file_reader:
            if counter not in dupe_rows:
                data.append(row)
            counter += 1

    with open(csv_url2, mode='w') as data_file:
        writer = csv.writer(data_file)
        writer.writerows(data)


def check_duplicates(csv_url):
    names = []
    token_ids = []
    urls = []
    res = []

    with open(csv_url, mode="r") as data_file:
        csv_file_reader = csv.reader(data_file, delimiter=',')
        for row in csv_file_reader:
            urls.append(row[0])
            names.append(row[1])
            token_ids.append(row[6])

    counter = 0
    for i in range(len(names) - 1):
        for j in range(i + 1, len(names)):
            if names[i] == names[j] and token_ids[i] == token_ids[j]:
                res.append(i)
                counter += 1

    return counter, res


if __name__ == "__main__":
    old_url = "../data/test_data.csv"
    # new_url = "../data/new_data2.csv"

    num, rows = check_duplicates(old_url)
    print(num)
    print(rows)
