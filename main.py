import pandas as pd
from tabula import read_pdf
import tabula as tb
import urllib3
from bs4 import BeautifulSoup
import urllib.request
import json



filePDF = "Final_test.pdf"
reader = read_pdf(filePDF ,stream=True, multiple_tables=True,encoding="UTF-8" )
# print(reader)
ss = pd.concat(reader)
print(ss)
# ss.to_json("im_json.json")
ss.to_html("main.html")
# Specify the path to your HTML file
html_file_path = 'main.html'

# Open the HTML file in read mode
with open(html_file_path, 'r') as html_file:
    # Read the contents of the file
    html_content = html_file.read()

# Print the content of the HTML file
soup = BeautifulSoup(html_content, 'html.parser')

# Find and print all the paragraph tags in the HTML
paragraphs = soup.find_all('td')
head_html = soup.find_all('th')
table = soup.find('table')
rows = table.find_all('tr')
fineNan = soup.find_all(text="NaN")
html = BeautifulSoup("<html><body></body></html>", "html.parser")
table = html.new_tag("table")
html.body.append(table)
string_no_want = ["NaN", "Lec.","Rec." , "Course Code" , "Course Name" , "Prerequisites" , "Credit" ,"Lec." , "Lab." ,"Rec.", "Notes", "Hours" ,"Total", "TBA","Available:","CS xxx:" , "C" , "Cr","Course","Title", "#", "Title", "##"]
code = []
subjects = []
time = []
for row in rows:
    cells = row.find_all('td')
    if cells:
        for cell in cells:
            text = cell.get_text().strip()
            if text not in string_no_want:
                if not text.isdigit():
                    if len(text) <= 8:
                        code.append(text)
                    elif len(text) > 8:
                        subjects.append(text)
                else:
                    number = int(text)
                    if 1 <= number <= 5:
                        time.append(number)


print(f"code : {len(code)}\n sub : {len(subjects)} \n time : {len(time)}")


# for i in code:
#     print(i)
# print("\n")
# for i in subjects:
#     print(i)
# print("\n")
# for i in time:
#     print(i)



for i in range(len(subjects)):
    # Create a new row
    row_tag = html.new_tag("tr")
    # Create td tags for code, subject, and time
    code_tag = html.new_tag("td", attrs={"class": "code"})
    sub_tag = html.new_tag("td", attrs={"class": "subject"})
    time_tag = html.new_tag("td", attrs={"class": "time"})
        
        # Set the content of the td tags
    code_tag.string = f"code : {code[i]}"
    sub_tag.string = f"subject : {subjects[i]}"
    time_tag.string = f"time : {time[i]}"
        
    # Append td tags to the row
    row_tag.append(code_tag)
    row_tag.append(sub_tag)
    row_tag.append(time_tag)
    
    # Append the row to the table
    table.append(row_tag)
my_content = html.prettify()

with open("test.html", "w") as file:
    file.write(my_content)
print("done")


html_file_path = 'test.html'
with open(html_file_path, 'r') as html_file:
    html_content = html_file.read()

soup = BeautifulSoup(html_content, 'html.parser')
table = soup.find('table')
rows = table.find_all('tr')

# Create a list to store data in sets of four subjects, codes, and times
grouped_data = []
current_group = {'subject': [], 'code': [], 'time': []}

# Loop through the rows and process the cells
for row in rows:
    cells = row.find_all('td')
    if cells:
        entry = {}
        for index, cell in enumerate(cells):
            if index == 0:
                code = cell.get_text().strip().replace("code :", "")
                entry['code'] = code
            elif index == 1:
                subject = cell.get_text().strip().replace("subject :", "")
                entry['subject'] = subject
            elif index == 2:
                time = cell.get_text().strip().replace("time :", "")
                entry['time'] = time

        # Append the entry to the current group
        current_group['subject'].append(entry['subject'])
        current_group['code'].append(entry['code'])
        current_group['time'].append(entry['time'])
        
        # Check if the current group has four entries, then start a new group
        if len(current_group['subject']) == 4:
            grouped_data.append(current_group)
            current_group = {'subject': [], 'code': [], 'time': []}

# If there are remaining entries in the last group, add it to the grouped data
if current_group['subject']:
    grouped_data.append(current_group)

# Convert the grouped data to JSON
json_data = json.dumps(grouped_data, indent=4)

# Write the JSON data to a file
with open('grouped_output.json', 'w') as json_file:
    json_file.write(json_data)

print("Conversion to JSON completed.")