
print ("hello word")
import random
password =""
def   generate_password(length):
    letters ="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    letters_upper ="ABCDEFGHIKLMNOPQRSTUVWXYZ"
    digits = "0123456789"
    symbols = "!@#$%^&*"
    all_chars = letters + letters_upper + digits + symbols
    password = ""
    for i in range(length):
         
        
        password += random.choice(all_chars)

    return password
print("password sederhana:", generate_password(10))

    

