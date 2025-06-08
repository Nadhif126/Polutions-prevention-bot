import random

def gen_pass(pass_length):
    elements = "+-/*!&$#?=@<>"
    password = ""

    for i in range(pass_length):
        password += random.choice(elements)

    return(password)

def coinflip():
    num = random.randint(1,2)
    if num == 1:
        return "Heads"
    else:
        return "Tails"
    
def roll_dice():
    return "the dice is", random.randint(1,6)
def meme():
    emojis = ["^^", "0_o", ":)", "¯\_(ツ)_/¯", "(￢_￢)"]
    return(random.choice(emojis))