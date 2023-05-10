import csv
from datetime import datetime


# Open the CSV file
with open('caida-raw.csv', 'r') as file:
    reader = csv.reader(file)
    rows = list(reader)

time_index = rows[0].index('time')
proto_index = rows[0].index('proto') # categorical data ("TCP" or "UDP")
offset_index = rows[0].index('off') # variance is 0
ihl_index = rows[0].index('ihl') # variance is 0
version_index = rows[0].index('version') # variance is 0

count = 0

rows = rows[:14240]

for i, row in enumerate(rows):
    count += 1
    converted = ''
    if i == 0: 
        converted = 'date'
    else: 
        unix_timestamp = int(row[time_index]) / 1000000
        converted = datetime.utcfromtimestamp(unix_timestamp).strftime('%Y-%m-%d %H:%M:%S')
        
    row.insert(0, converted)
            
    del row[offset_index+1] # delete the offset column since variance is 0
    del row[ihl_index+1] # delete the ihl column since variance is 0
    del row[version_index+1] # delete the version column since variance is 0
    del row[proto_index+1] # delete proto column since it is categorical data
    
print("count of items: ", count)

# Write the updated rows to a new CSV file
with open('datasets/updated_pcap.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(rows)