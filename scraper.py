import requests
from bs4 import BeautifulSoup
import re

url = 'https://cs.illinois.edu/about/people/all-faculty/zaher'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

html = requests.get(url,headers=headers)
bs_html = BeautifulSoup(html.text,'html.parser')
content = re.findall(r'\w+', bs_html.text) #remove punctuation
#filter numbers
def int_filter(list_i):
    for v in list_i:
        try:
            int(v)
            continue # Skip these
        except ValueError:
            yield v # Keep these

number_filter = (list(int_filter(content)))

data = {}
#store in dictionary and word count
for i in range(len(number_filter)):
    if number_filter[i] not in data:
        data[number_filter[i].lower()] = 1 #lowercase only
    else:
        data[number_filter[i].lower()] += 1

#sort in descending order
sort_orders = sorted(data.items(), key=lambda x: x[1], reverse=True)
sort_dict = {}
for i  in sort_orders:
    sort_dict[i[0]] = i[1]

print(sort_dict)

## write in a txt file
# def write_lst(lst,file_):
#     with open(file_,'w') as f:
#         for l in lst:
            
#             f.write(l)
#             f.write('\n')
# bio_urls_file = 'file.txt'
# write_lst(sort_dict,bio_urls_file)