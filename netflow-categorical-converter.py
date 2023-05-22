import csv
from datetime import datetime


# Open the CSV file
with open('urg16-raw.csv', 'r') as file:
    reader = csv.reader(file)
    rows = list(reader)

time_index = rows[0].index('ts')

count = 0

rows = rows[:14240] # just to test small size of dataset

for i, row in enumerate(rows):
    count += 1
    converted = ''
    if i == 0: 
        converted = 'date'
    else: 
        unix_timestamp = int(float(row[time_index]) / 1000000)
        converted = datetime.utcfromtimestamp(unix_timestamp).strftime('%Y-%m-%d %H:%M:%S')
        
    row.insert(0, converted)

print("count of items: ", count)

categoricalColumns = []
for name, values in df_data.dtypes.items():
    if values == 'object': 
        categoricalColumns.append(name)

# handling for categorical features
df_data = pd.get_dummies(data=df_data, columns=categoricalColumns, dtype=float) # Get one-hot encoding of variable
        

# Write the updated rows to a new CSV file
with open('datasets/updated_categorical_urg16.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(rows)