# Author: github.com/nthonybruno
# Description: Converts a specific unstructured HTML property tax dataset into a structured CSV file for future analysis and manipulation.

# Dependencies below
import requests
from bs4 import BeautifulSoup
import csv

# URL contains loosely formatted data on every NJ town's property tax data, over 500 entries that I needed formatted.
URL = "https://patch.com/new-jersey/across-nj/every-nj-towns-average-property-tax-bill-new-2021-list"
page = requests.get(URL)
content = BeautifulSoup(page.text, features="lxml")

# Fiilter down the page content to just the HTML parent <div> tag containing the target <li> tags
target_content_parent_element = content.find_all("div", class_="styles_HTMLContent__LDG2k")

# Loop through the parent <div> tag, and append each <li> tag as a new element in the list.
list_builder = []
for tag in target_content_parent_element:
    list_elements = tag.find_all("li")
    for tagg in list_elements:
        list_builder.append(tagg.text)

# This list now contains unwanted additional entries. There are 565 total towns in the list, so I chop off all entries after. This leaves #1 - #565 in refined_list
refined_list = list_builder[:565]


filename = 'NJ County Property Tax Averages.csv' # Will output to cwd in terminal
fields = ["Town", "County", "Average Annual Tax Bill ($)"] #Column header information for csv file

# Write headers to file
with open(filename,'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(fields)

# At this point, each list element is in the format: ['Tavistock Borough, Camden $30,328']
# Goal now is to seperate into 3 distinct elements, so that the output CSV fiile can have 3 columns: Town, County and Average Annual Tax Bill for the respective county
# Loop over unformatted list, split each index, and then output the new row to the output file.
for entry in refined_list:
    temp = entry.split(" $") 
    temp2 = temp[0].split(",") 
    
    with open(filename,'a', newline='',) as f:
        writer = csv.writer(f)
        row = [temp2[0], temp2[1], temp[1]]
        writer.writerow(row)