import os
from discord.ext import commands
import mysql.connector

bot = commands.Bot(command_prefix='$')

@bot.command()
async def foo(ctx):
    await ctx.send("Hi there ctx command")

@bot.command()
async def ind(ctx):
    await individuation(ctx)

@bot.command()
async def individuation(ctx):
    if ctx.message.author == bot.user:
        return

    msg = ctx.message

    if len(msg.channel_mentions) > 0:
        ch = msg.channel_mentions[0] #TODO support multiple channel posting?
    else:
        ch = msg.channel

        if len(msg.mentions) > 0:
            tgt = msg.mentions[0] #TODO support multiple users?
        else:
            tgt = msg.author.mention

        await send_prompt(tgt, ch)

async def send_prompt(tgt, channel):
  await channel.send("Here's an individuation prompt for {0}".format(tgt))

@bot.command()
async def add(ctx, *args):
    prompt = ""
    for arg in args:
        prompt = prompt + " " + arg
    pw = os.getenv('DBPASSWORD')
    conn = mysql.connector.connect(user='discord', password=pw, host='127.0.0.1', database='challenge_prompts')
    cursor = conn.cursor()
    sql = "INSERT INTO individuation(prompt, author) VALUES('{0}','{1}')".format(prompt.lstrip(), ctx.message.author.id)
    try:
        cursor.execute(sql)
        conn.commit()
        conn.close()
        await ctx.channel.send("I added a thing and it probably worked")
    except:
        conn.rollback()
    conn.close()
    
@bot.event
async def on_ready():
  print("I'm alive. I am {0.user}".format(bot))

bot.run(os.getenv('TOKEN'))