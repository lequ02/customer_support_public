import json
import pandas as pd
import requests

file = open('ruby_hackathon_data.json', 'r')
json_data = file.read()

# Load JSON data
complaints = json.loads(json_data)


# Convert JSON data to DataFrame
df = pd.DataFrame([complaint['_source'] for complaint in complaints])

# Print the DataFrame
print(df)
print(df.columns)
print(df['complaint_what_happened'].head())
print(df.sub_issue.unique())
print(len(df.sub_issue.unique()))

print(df['product'].unique())

print(df['company_response'].unique())
print(df['company_public_response'].unique())

print(df['issue'].unique())
print(df['sub_issue'].unique())
# count =0 
# for i in df.sub_issue.unique():
#     print(i)
#     # print(df[df['sub_issue'] == i]['complaint_what_happened'].head())
#     count+=1

# print(count)


# print(len(df))
# for complaint in complaints:
#     # print(complaint,"\n\n")
#     # for key in complaint:
#     #     print(key, ":", complaint[key])

#     # print(complaint['_source'], "\n\n")
#     for key in complaint['_source']:
#         print("\t", key, ":", complaint['_source'][key])
#     i+=1
#     if i==7:
#         break

# print(len(complaints))

