with open("DFile.txt", 'r') as file:
    lines = file.readlines()

# delete matching content
content = "BS-4444-TEMP.mp4"
flag =0
with open("DFile.txt", 'w') as file:
    for line in lines:
        # readlines() includes a newline character
        #if line.strip("\n") != content:
        print("find:", line.find(content))
        if line.find(content) == 0:
            line = content + '#432' + '\n'
            flag = 1             
        file.write(line)
        
    if flag == 0 :
        line = content + '$777'
        file.write(line)