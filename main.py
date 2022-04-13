import os
from discord.ext import commands
import mysql.connector
import markdown

bot = commands.Bot(command_prefix='$')

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

# @bot.command()
# async def add(ctx, *args):
#     prompt = ""
#     for arg in args:
#         prompt = prompt + " " + arg#.replace('"', '\"').replace("'", "\\'")
#     #prompt = json.dumps(prompt)
#     prompt = markdown.markdown(prompt)
#     dbpw = os.getenv('DBPASSWORD')
#     dbhost = os.getenv('DBHOST')
#     dbuser = os.getenv('DBUSERNAME')
#     conn = mysql.connector.connect(user=dbuser, password=dbpw, host=dbhost, database='challenge_prompts')
#     cursor = conn.cursor()
#     sql = "INSERT INTO individuation(prompt, author) VALUES('{0}','{1}')".format(prompt, ctx.message.author.id)
#     print("Going to send the following to SQL: ", sql)
#     try:
#         cursor.execute(sql)
#         conn.commit()
#         if cursor.rowcount > 0:
#             id = cursor.lastrowid
#             sql_check = "SELECT * FROM individuation WHERE id={0}".format(id)
#             cursor.execute(sql_check)
#             new_prompt = cursor.fetchall()
#         conn.close()
#         await ctx.channel.send("<@{0}> added the following prompt: \n {1}".format(new_prompt[0][2], new_prompt[0][1]))
#     except Exception as e:
#         print("Oops", e)
#         conn.rollback()
#         conn.close()
    
@bot.event
async def on_ready():
  print("I'm alive. I am {0.user}".format(bot))

bot.run(os.getenv('TOKEN'))