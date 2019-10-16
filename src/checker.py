import properties

file_name = properties.SCRIPT_LOG_FILE_NAME

print("file_name : {}".format(file_name))

with open(file_name, "r") as f:
    line = f.read()
    print(line)
