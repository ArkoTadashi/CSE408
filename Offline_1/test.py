filePath = 'server/pic.png'
with open(filePath, 'rb') as file:
    fileData = bytearray(file.read())

print(fileData)