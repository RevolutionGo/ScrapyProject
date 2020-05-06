path = r'C:\Users\SONY\Desktop\cloudtest.txt'
page=''
with open(path,'r', encoding="utf-8") as file:
    for line in file:
        page+=line.replace('\n', '\\n').replace('\r', '\\n')

with open(r'C:\Users\SONY\Desktop\cloudjson.txt', 'w', encoding="utf-8") as file1:
    file1.write(page)