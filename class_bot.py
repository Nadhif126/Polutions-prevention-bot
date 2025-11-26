# test-bot(bot class)
# This example requires the 'members' and 'message_content' privileged intents to function.

import discord
import random
from discord.ext import commands
from bot_logic import gen_pass
import os
import requests
from model import get_class
from collections import Counter
from detect_objects import detect
from transformers import pipeline
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
description = '''An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here.'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
# command prefix 
bot = commands.Bot(command_prefix='$', description=description, intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})') # type: ignore
    print('------')

# adding two numbers
@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)
# subtracting two numbers
@bot.command()
async def min(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left - right)
# multiplication two numbers
@bot.command()
async def times(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left*right)
# division two numbers
@bot.command()
async def divide(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left/right)
# exp two numbers
@bot.command()
async def exp(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left**right)

@bot.command()
async def mod(ctx, left: int, right: int):
    """find remainder of the 2 numbers."""
    await ctx.send(left%right)


# # give local meme see python folder Data Science drive
@bot.command()
async def meme(ctx):
    # try by your self 2 min
    img_name = random.choice(os.listdir('meme'))
    with open(f'meme/{img_name}', 'rb') as f:
        picture = discord.File(f)
 
    await ctx.send(file=picture)

# duck and dog API
def get_dog_image_url():
    url = 'https://random.dog/woof.json'
    res = requests.get(url)
    data = res.json()
    return data['url']
@bot.command('dog')
async def dog(ctx):
    '''Setiap kali permintaan dog (anjing) dipanggil, program memanggil fungsi get_dog_image_url'''
    image_url = get_dog_image_url()
    await ctx.send(image_url)

def get_duck_image_url():
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']
@bot.command('duck')
async def duck(ctx):
    '''Setiap kali permintaan duck (bebek) dipanggil, program memanggil fungsi get_duck_image_url'''
    image_url = get_duck_image_url()
    await ctx.send(image_url)

@bot.command()
async def tulis(ctx, *, my_string: str):
    with open('kalimat.txt', 'w', encoding='utf-8') as t:
        text = ""
        text += my_string
        t.write(text)

@bot.command()
async def tambahkan(ctx, *, my_string: str):
    with open('kalimat.txt', 'a', encoding='utf-8') as t:
        text = "\n"
        text += my_string
        t.write(text)

@bot.command()
async def baca(ctx):
    with open('kalimat.txt', 'r', encoding='utf-8') as t:
        document = t.read()
        await ctx.send(document)
        
# spamming word
@bot.command()
async def repeat(ctx, times: int, *,content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)
        # sentiment dev.
@bot.command() 
async def sentiment(ctx, *, kalimat3: str):
    # Initialize sentiment analysis pipeline with GPU support
    analyzer = pipeline('sentiment-analysis', model='nlptown/bert-base-multilingual-uncased-sentiment',device=1, batch_size=8, truncation=True)
    sentiment = analyzer(kalimat3)[0]
    await ctx.send(f"Sentiment: {sentiment['label']}")
    await ctx.send(f"Score: {sentiment['score']}")
# # sentiment dev.
@bot.command()
async def sentiment_vander(ctx, *, kalimat4: str):
    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(kalimat4)
    # Format the output for better readability
    formatted_scores = f"""
    Negative: {scores['neg']:.3f}
    Neutral: {scores['neu']:.3f}
    Positive: {scores['pos']:.3f}
    Compound: {scores['compound']:.3f}
    """
    await ctx.send(f"Score: {formatted_scores}")
#Computer Vision 

@bot.command()
async def klasifikasi(ctx):
    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            file_name = attachment.filename
            #file_url = attachment.url IF URL
            await attachment.save(f"./CV/{file_name}")
            await ctx.send(get_class(model_path="keras_model.h5", labels_path="labels.txt", image_path=f"./CV/{file_name}"))
    else:
        await ctx.send("Anda lupa mengunggah gambar burung :(")

@bot.command()
async def klasifikasi_sampah(ctx):
    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            file_name = attachment.filename
            #file_url = attachment.url IF URL
            await attachment.save(f"./CV/{file_name}")
            await ctx.send(get_class(model_path="keras_model4.h5", labels_path="labels4.txt", image_path=f"./CV/{file_name}"))
    else:
        await ctx.send("Anda lupa mengunggah gambar sampah :(")

@bot.command()
async def deteksi(ctx):
    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            file_name = attachment.filename
            await attachment.save(f"./CV/{file_name}")
            # call detect ONCE and reuse its result
            results = detect(input_image=f"./CV/{file_name}", output_image=f"./CV/{file_name}", model_path="yolov3.pt")
            # If detect returns a string (message/path), send it
            if isinstance(results, str):
                await ctx.send(results)
            # If detect returns a list of detections, count them
            if isinstance(results, list):
                counts = Counter(d['name'] for d in results)
                msg = '\n'.join(f"{k}: {v}" for k, v in counts.items())
                with open(f'CV/{file_name}', 'rb') as f:
                    picture = discord.File(f)
                await ctx.send(file=picture)
                await ctx.send(f"Object counts:\n{msg}")
    else:
        await ctx.send("Anda lupa mengunggah gambar :(")

# password generator        
@bot.command()
async def pw(ctx):
    await ctx.send(f'Kata sandi yang dihasilkan: {gen_pass(10)}')
@bot.command()
async def bye(ctx):
    await ctx.send('\U0001f642')
# coinflip
@bot.command()
async def coinflip(ctx):
    num = random.randint(1,2)
    if num == 1:
        await ctx.send('It is Head!')
    if num == 2:
        await ctx.send('It is Tail!')

# rolling dice
@bot.command()
async def dice(ctx):
    nums = random.randint(1,6)
    if nums == 1:
        await ctx.send('It is 1!')
    elif nums == 2:
        await ctx.send('It is 2!')
    elif nums == 3:
        await ctx.send('It is 3!')
    elif nums == 4:
        await ctx.send('It is 4!')
    elif nums == 5:
        await ctx.send('It is 5!')
    elif nums == 6:
        await ctx.send('It is 6!')

# welcome message
@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}') # type: ignore

#show local drive    
@bot.command()
async def local_drive(ctx):
    try:
      folder_path = "./files"  # Replace with the actual folder path
      files = os.listdir(folder_path)
      file_list = "\n".join(files)
      await ctx.send(f"Files in the files folder:\n{file_list}")
    except FileNotFoundError:
      await ctx.send("Folder not found.") 
#show local file
@bot.command()
async def showfile(ctx, filename):
  """Sends a file as an attachment."""
  folder_path = "./files/"
  file_path = os.path.join(folder_path, filename)

  try:
    await ctx.send(file=discord.File(file_path))
  except FileNotFoundError:
    await ctx.send(f"File '{filename}' not found.")
# upload file to local computer
@bot.command()
async def simpan(ctx):
    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            file_name = attachment.filename
            # file_url = attachment.url  IF URL
            await attachment.save(f"./files/{file_name}")
            await ctx.send(f"Menyimpan {file_name}")
    else:
        await ctx.send("Anda lupa mengunggah :(")
@bot.command()
async def pantau_udara(ctx):
    await ctx.send('Berikut adalah perkiraan kualitas udara: https://iklim.bmkg.go.id/id/kualitas-udara-indonesia/')
@bot.command()
async def tulis_tips(ctx, *, my_string: str):
    with open('polusi.txt', 'w', encoding='utf-8') as t:
        text = ""
        text += my_string
        t.write(text)

@bot.command()
async def tambahkan_tips(ctx, *, my_string: str):
    with open('polusi.txt', 'a', encoding='utf-8') as t:
        text = "\n"
        text += my_string
        t.write(text)

@bot.command()
async def tips(ctx):
    with open('kalimat.txt', 'r', encoding='utf-8') as t:
        document = t.read()
        await ctx.send(document)
@bot.command()
async def lama_penguraian(ctx):
    await ctx.send('Berikut adalah daftar lama penguraian sampah: https://dlh.lampungprov.go.id/detail-post/berapa-lama-sampah-terurai#:~:text=Ayo%20pelajari%20lebih%20jauh%20mengenai,waktu%206%20Bulan%20untuk%20terurai.')
@bot.command()
async def web(ctx):
    await ctx.send('Berikut adalah website databse: https://deaf661.pythonanywhere.com/')
bot.run(token=)

