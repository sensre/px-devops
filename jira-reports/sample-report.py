## 
# Description: Export more than 1000 jira issues
#   Originally taken from https://confluence.atlassian.com/jirakb/export-over-1000-results-to-excel-from-jira-cloud-779160833.html
# Author: GLiNTECH Pty Ltd - www.glintech.com
# How to run:
#   python3 export-issues.py email api_token 'url'
## 

import os
import sys
import requests
import glob
import csv
import time
from requests.auth import HTTPBasicAuth

def count_headers(headers):
    headercounts = []
    for header in headers:
        counted = False
        for headercount in headercounts:
            if headercount[0] == header:
                headercount[1] += 1
                counted = True
        if not counted:
            headercounts.append([header,1])
    return headercounts

def get_row_count(file):
    with open(file, 'r', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        return sum(1 for row in reader)

def get_headers(file):
    with open(file, 'r', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        for i, row in enumerate(reader):
            if i==0:
                return row

def insert_empty_column(file, header, index):
    with open(file, 'r', encoding='utf-8') as infile:
        with open('temp_' + file, 'w', newline='', encoding='utf-8') as outfile:
            reader = csv.reader(infile)
            writer = csv.writer(outfile, delimiter=',', quotechar='\"', quoting=csv.QUOTE_MINIMAL)
            for i, row in enumerate(reader):
                if i==0:
                    row.insert(index, header)
                    writer.writerow(row)
                else:
                    row.insert(index, '')
                    writer.writerow(row)
    os.remove(file)
    os.rename('temp_' + file, file)

def remove_columns(file, indices):
    indices.reverse()
    with open(file, 'r', encoding='utf-8') as infile:
        with open('temp_' + file, 'w', newline='', encoding='utf-8') as outfile:
            reader = csv.reader(infile)
            writer = csv.writer(outfile, delimiter=',', quotechar='\"', quoting=csv.QUOTE_MINIMAL)
            for i, row in enumerate(reader):
                for j in range(len(indices)):
                    row.pop(indices[j])
                writer.writerow(row)
    os.remove(file)
    os.rename('temp_' + file, file)

def find_empty_column_indices(file):
    column_count = len(get_headers(file))
    row_count = get_row_count(file)
    empty_column_indices = []
    for i in range(column_count):
        with open(file, 'r', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            for j, row in enumerate(reader):
                if j>0 and row[i] != '':
                    break
            if j == row_count - 1:
                empty_column_indices.append(i)
    return empty_column_indices

def dl_export():
    """_summary_
     args = sys.argv[1:]
    
    if len(args) != 3:
        print("Not enough arguments provided. Need email, API token and URL")
        print(f"Example:")
          sys.exit()
     """  
    page = 1000 # issue count per page, default 1000

    #email = args[0]
    #token = args[1]
    #url = args[2].replace("tempMax=1000",f"tempMax={page}")
    email='xxxxx'
    token='xxxxx'
    url= 'xxxxx'.replace("tempMax=1000",f"tempMax={page}")
    auth = HTTPBasicAuth(email,token)

    start = 0
    while True:
        response = requests.get(
            f"{url}&pager/start={start}",
            auth=auth
        )

        if response.ok:
            with open(f"file{start}.csv", 'wb') as f:
                f.write(response.content)
            if os.path.getsize(f"file{start}.csv") == 0:
                os.remove(f"file{start}.csv")
                break
            start = start + page

    files = glob.glob("file*.csv")

    #generate maximum header counts across all csv exports
    maxheadercounts = []
    for i, file in enumerate(files):
        headercounts = []
        with open(file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for j, row in enumerate(reader):
                if j==0:
                    headercounts = count_headers(row)
                else:
                    break
        if len(maxheadercounts) == 0:
            maxheadercounts = headercounts
        
        newheaders = []
        for headercount in headercounts:
            for k in range(len(maxheadercounts)):
                if headercount[0]==maxheadercounts[k][0]:
                    if headercount[1] > maxheadercounts[k][1]:
                        maxheadercounts[k][1] = headercount[1]
                    for newheader in reversed(newheaders):
                        maxheadercounts.insert(k, newheader)
                    newheaders=[]
                    break
                elif k == len(maxheadercounts) - 1:
                    newheaders.append(headercount)
        if len(newheaders) > 0:
            for newheader in newheaders:
                maxheadercounts.append(newheader)

    #generate the header for the merged csv exports
    finalheaders = []
    for header in maxheadercounts:
        for i in range(header[1]):
            finalheaders.append(header[0])


    #insert empty columns for multivalue fields
    for file in files:
        while True:
            headers = get_headers(file) 
            if len(finalheaders) == len(headers):
                break
            for i in range(len(headers)):
                if headers[i] != finalheaders[i]:
                    insert_empty_column(file, finalheaders[i], i)
                    break

	# Combining csv files
    output_csv = "full_export.csv"
    with open(output_csv, 'w', encoding='utf-8') as outfile:
        for i, file in enumerate(files):
            with open(file, 'r', encoding='utf-8') as f:
                if i == 0:
                    outfile.write(f.read())
                else :
                    for k, line in enumerate(f):
                        if k :
                            outfile.write(line)
            os.remove(file)

    # Remove empty columns from the combined csv
    empty_column_indices = find_empty_column_indices(output_csv)
    remove_columns(output_csv, empty_column_indices)        
    

    print("Export completed to file : " + output_csv)

if __name__ == "__main__":
    start = time.time()
    dl_export()
    end = time.time()


    print('took')
    print(end - start)
    print('seconds')