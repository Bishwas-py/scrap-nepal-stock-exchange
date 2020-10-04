import requests as reqs
from bs4 import BeautifulSoup
import html5lib
import csv
import os

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}
url_preffix = "http://www.nepalstock.com/main/todays_price/index/"

result = []
for pagination in range(10):
    request_ = reqs.get(f'{url_preffix}{pagination+1}')
    print(f'{url_preffix}{pagination+1}')
    souped_data = BeautifulSoup(request_.text, 'html5lib')
    for tr_tags in range(20):
        print(tr_tags, pagination)
        try:
            tr_count = souped_data.findAll('tr')[2+tr_tags]
            traded_comp = tr_count.findAll('td')[1].text
            transaction_num = tr_count.findAll('td')[2].text
            max_price = tr_count.findAll('td')[3].text
            min_price = tr_count.findAll('td')[4].text
            closing_price = tr_count.findAll('td')[5].text
            traded_shares = tr_count.findAll('td')[6].text
            traded_amount = tr_count.findAll('td')[7].text
            pre_closing = tr_count.findAll('td')[8].text
            diff_rs = tr_count.findAll('td')[9].text.split(u"\xa0")[0]

            passed_dict = {
                'traded_comp' : traded_comp,
                'transaction_num': transaction_num,
                'max_price' : max_price,
                'min_price' : min_price,
                'closing_price' : closing_price,
                'traded_shares' : traded_shares,
                'traded_amount' : traded_amount,
                'pre_closing' : pre_closing,
                'diff_rs' : diff_rs
            }
        except:
            break
        result.append(passed_dict)

new_csv = open('final.csv', 'a', newline='')
not_file_created = os.stat('final.csv').st_size == 0
csv_writer = csv.DictWriter(new_csv, fieldnames= [
        'traded_comp', 
        'transaction_num', 
        'max_price', 
        'min_price', 
        'closing_price', 
        'traded_shares', 
        'traded_amount', 
        'pre_closing', 
        'diff_rs'
        ]
    )
if not_file_created:
    csv_writer.writeheader()

csv_writer.writerows(
    result
)

print('Done!!!')