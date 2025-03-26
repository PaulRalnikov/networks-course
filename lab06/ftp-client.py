from ftplib import FTP

ftp = FTP('127.0.0.1')
ftp.login(user="user")

while (True):
    command = input().split()
    if (len(command) == 0):
        continue
    arg_0 = command[0]

    if (arg_0 == "ls"):
        ftp.dir()
    elif (arg_0 == "exit"):
        break
    elif (arg_0 == "load"):
        if len(command) < 2:
            print("Incorrect load: no file name")
            continue
        file_name = command[1]
        with open (file_name, "wb") as file:
            ftp.retrbinary(f"RETR {file_name}", file.write)
        print("File loaded!")
    elif arg_0 == "send":
        if len(command) < 2:
            print("Incorrect send: no file name")
            continue
        file_name = command[1]
        with open (file_name, "rb") as file:
            ftp.storbinary(f"STOR {file_name}", file)
        print("File sent!")
ftp.quit()
