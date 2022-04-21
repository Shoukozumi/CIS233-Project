import os
import time

from scrape_transactions import extract_from_link
import csv


if __name__ == "__main__":
	urls_file = open("nft_urls.csv", mode="r")
	reader = list(csv.reader(urls_file))
	if os.path.isfile("data.csv"):
		start = len(list(csv.reader(open("data.csv", mode="r"))))
		mode = "a"
	else:
		start = 0
		mode = "w"
		exit()
	with open("data.csv", mode=mode) as data_file:
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
				break
			if s == '':
				data_file.write("Skipped\n")
			else:
				data_file.write(s + '\n')
			# print(s)
