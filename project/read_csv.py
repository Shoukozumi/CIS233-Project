import os
import time

from scrape_transactions import extract_from_link
import csv


if __name__ == "__main__":
	urls_file = open("../data/nft_urls.csv", mode="r")
	reader = list(csv.reader(urls_file))
	if os.path.isfile("../data/old_data.csv"):
		start = len(list(csv.reader(open("../data/old_data.csv", mode="r"))))
		mode = "a"
	else:
		start = 0
		mode = "w"
		exit()
	with open("../data/old_data.csv", mode=mode) as data_file:
		for i in range(start, len(reader) - 1):
			link = reader[i][0]
			print(f'link #{i}', link)
			c = 0
			while c < 10:
				try:
					s = extract_from_link(link)
					break
				except Exception as e:
					print(e)
					time.sleep(2)
					c += 1

			if c == 10:
				print("ERROR")
				data_file.write(s + '\n')
			if s == '':
				data_file.write("Skipped\n")
			else:
				data_file.write(s + '\n')
