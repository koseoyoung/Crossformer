import csv
from datetime import datetime


# Open the CSV file
with open('caida-raw.csv', 'r') as file:
    reader = csv.reader(file)
    rows = list(reader)

time_index = rows[0].index('time')
proto_index = rows[0].index('proto')
offset_index = rows[0].index('off')
ihl_index = rows[0].index('ihl')
version_index = rows[0].index('version')

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
            
    del row[offset_index+1] # delete all same values coloumn or string instead of integer values 
    del row[ihl_index+1]
    del row[version_index+1]
    del row[proto_index+1]
    
print("count of items: ", count)

# Write the updated rows to a new CSV file
with open('datasets/updated_pcap.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(rows)