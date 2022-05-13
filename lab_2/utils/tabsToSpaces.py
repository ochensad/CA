file = open('./../tests/task_data.txt')
file2 = open('./../tests/task_data_spaces.txt', 'w')
for row in file.readlines():
    file2.write(row.replace("\t", " "))
file.close()
file2.close()