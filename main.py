import asyncio
import os
import json
from functools import partial

import requests
from interactions import *
from googleapiclient.discovery import build

# =====================================#
#               BOT SET UP            #
# =====================================#

# make sure to work in the correct directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# initialize variables
global guilds, guild_keys_values, reseaux
TOKEN = ""
YOUTUBE_API_KEY = ""
guilds = []
guild_keys_values = {}
reseaux = {}


# read config file
def load_config():
    with open("assets/config.json", "r") as input_config:
        loaded_config = json.load(input_config)
    return loaded_config


# save the config to a json file
def save_config():
    with open("assets/config.json", "w") as output_config:
        json.dump({"token": TOKEN, "youtube": YOUTUBE_API_KEY, "guilds": guild_keys_values, "social": reseaux},
                  output_config)


# load saved config
config = load_config()

# apply it
TOKEN: str = config["token"]
YOUTUBE_API_KEY: str = config["youtube"]
guilds: list[int] = [int(guild_id) for guild_id in config["guilds"].keys()]
guild_keys_values = config["guilds"]
reseaux: dict = config["social"]

# delete unnecessary heavy variables to free some memory
del config

# create a bot/client instance
bot = Client(TOKEN)


# =====================================#
#               BOT EVENTS            #
# =====================================#

# know when the bot is online
@bot.event
async def on_ready():
    print("ready !")


# =====================================#
#             Administration           #
# =====================================#

@bot.command(
    name="rules",
    description="update the server's rules",
    scope=guilds,
    options=[
        Option(
            name="new_rules",
            description="new rules statement",
            required=True,
            type=OptionType.ATTACHMENT
        ),
        Option(
            name="role_to_add",
            description="role to add when the rules are accepted",
            required=True,
            type=OptionType.ROLE
        )
    ]
)
async def rules(ctx: CommandContext, new_rules: Attachment, role_to_add: Role):
    if not guild_keys_values[ctx.guild.id][1] in ctx.author.roles:
        await ctx.send("You don't have the authorization to do this.")

    else:
        """if ctx.channel.id == guild_keys_values[ctx.guild.id][0]:
            await ctx.send("Please use this command in another channel.", ephemeral=True)
            return None
        
        message = await ctx.send("Fetching rules channel")
        print('server rules modification requested')
        channels = ctx.guild.channels
        for c in channels:
            if c.id == guild_keys_values[ctx.guild.id][0]:
                print(c, c.id, c.id == guild_keys_values[ctx.guild.id][0])
                rules_channel = c
                break
        await message.edit("Cleaning channel before sending")
        await asyncio.sleep(1)
        await rules_channel.purge(100)
        await message.edit("Updating rules")
        validate = Button(
            style=ButtonStyle.SUCCESS,
            label="☑️I have read and I accept the rules",
            custom_id="rules")
        rules_text = requests.get(new_rules.url).text
        await rules_channel.send(rules_text, components=validate)
        await asyncio.sleep(1)
        await message.delete()
        await ctx.send("All done!", ephemeral=True)
        """
        validate = Button(
            style=ButtonStyle.SUCCESS,
            label="☑️I have read and I accept the rules",
            custom_id="rules")
        await ctx.send("Click the button below to agree the rules and get an access to the whole server.", components=validate)


@bot.component("rules")
async def accept_the_rules(ctx: ComponentContext):
    await ctx.author.add_role(guild_keys_values[ctx.guild.id][3], ctx.guild.id)
    await ctx.author.send(f"You know have full access to **{ctx.guild.name}**.")
    await ctx.send("Noted!", ephemeral=True)


@bot.command(
    name="clear",
    description="delete an amount of messages",
    options=[
        Option(
            name="messages",
            description="amount of messages to delete",
            type=OptionType.INTEGER,
            required=False
        )
    ]
)
async def clear(ctx: CommandContext, messages: int =None):
    if not guild_keys_values[ctx.guild.id][1] in ctx.author.roles:
        await ctx.send("You don't have the authorization to do this.")

    else:
        await ctx.channel.purge(messages)
        await ctx.send("All done!", ephemeral=True)

def make_buttons(guild:CommandContext.guild, roles):
    buttons = []
    emojis = guild.emojis
    print(emojis)
    icon = None
    for r in roles:
        for emo in emojis:
            if emo.name == r:
                icon = emo
                break
        buttons.append(Button(style=ButtonStyle.PRIMARY, label=f" {r}", custom_id=r, emoji=icon))
    return buttons


@bot.command(
    name="rolereact",
    description="initialize the rolereact"
)
async def rolereact(ctx: CommandContext, messages: int = 100):
    if not guild_keys_values[ctx.guild.id][1] in ctx.author.roles:
        await ctx.send("You don't have the authorization to do this.")

    else:
        jailbreaks = ["unc0ver", "taurine", "odyssey", "checkra1n","chimera"]
        devices = ["iphone", "ipad","appletv", "mac"]
        gender = ["man", "woman", "other"]
        platforms = ["apple", "android", "windows", "linux"]

        jailbreaks_buttons = make_buttons(ctx.guild, jailbreaks)
        devices_buttons = make_buttons(ctx.guild, devices)
        gender_buttons = make_buttons(ctx.guild, gender)
        platforms_buttons = make_buttons(ctx.guild, platforms)


        await ctx.send("**choose your jailbreak tool(s) below**", components=jailbreaks_buttons)
        await ctx.send("**choose your device(s) below**", components=devices_buttons)
        await ctx.send("**choose your platform(s) below**", components=platforms_buttons)
        await ctx.send("**choose your gender below**", components=gender_buttons)


@bot.component("windows")
async def windows(ctx: ComponentContext):
    role_to_add = 1017446247533125632
    if role_to_add in ctx.author.roles:
        await ctx.author.remove_role(role_to_add, ctx.guild.id)
        await ctx.send("Role removed successfully", ephemeral=True)
    else:
        await ctx.author.add_role(role_to_add, ctx.guild.id)
        await ctx.send("Role added successfully", ephemeral=True)


@bot.component("unc0ver")
async def unc0ver(ctx: ComponentContext):
    role_to_add = 1017446813680275549
    if role_to_add in ctx.author.roles:
        await ctx.author.remove_role(role_to_add, ctx.guild.id)
        await ctx.send("Role removed successfully", ephemeral=True)
    else:
        await ctx.author.add_role(role_to_add, ctx.guild.id)
        await ctx.send("Role added successfully", ephemeral=True)


@bot.component("taurine")
async def taurine(ctx: ComponentContext):
    role_to_add = 1017446895532114012
    if role_to_add in ctx.author.roles:
        await ctx.author.remove_role(role_to_add, ctx.guild.id)
        await ctx.send("Role removed successfully", ephemeral=True)
    else:
        await ctx.author.add_role(role_to_add, ctx.guild.id)
        await ctx.send("Role added successfully", ephemeral=True)


@bot.component("odyssey")
async def odyssey(ctx: ComponentContext):
    role_to_add = 1017446874011152474
    if role_to_add in ctx.author.roles:
        await ctx.author.remove_role(role_to_add, ctx.guild.id)
        await ctx.send("Role removed successfully", ephemeral=True)
    else:
        await ctx.author.add_role(role_to_add, ctx.guild.id)
        await ctx.send("Role added successfully", ephemeral=True)


@bot.component("mac")
async def mac(ctx: ComponentContext):
    role_to_add = 1017446181011456040
    if role_to_add in ctx.author.roles:
        await ctx.author.remove_role(role_to_add, ctx.guild.id)
        await ctx.send("Role removed successfully", ephemeral=True)
    else:
        await ctx.author.add_role(role_to_add, ctx.guild.id)
        await ctx.send("Role added successfully", ephemeral=True)


@bot.component("linux")
async def linux(ctx: ComponentContext):
    role_to_add = 1017446279162363986
    if role_to_add in ctx.author.roles:
        await ctx.author.remove_role(role_to_add, ctx.guild.id)
        await ctx.send("Role removed successfully", ephemeral=True)
    else:
        await ctx.author.add_role(role_to_add, ctx.guild.id)
        await ctx.send("Role added successfully", ephemeral=True)


@bot.component("iphone")
async def iphone(ctx: ComponentContext):
    role_to_add = 953374203644633128
    if role_to_add in ctx.author.roles:
        await ctx.author.remove_role(role_to_add, ctx.guild.id)
        await ctx.send("Role removed successfully", ephemeral=True)
    else:
        await ctx.author.add_role(role_to_add, ctx.guild.id)
        await ctx.send("Role added successfully", ephemeral=True)


@bot.component("ipad")
async def ipad(ctx: ComponentContext):
    role_to_add = 1017446140741951509
    if role_to_add in ctx.author.roles:
        await ctx.author.remove_role(role_to_add, ctx.guild.id)
        await ctx.send("Role removed successfully", ephemeral=True)
    else:
        await ctx.author.add_role(role_to_add, ctx.guild.id)
        await ctx.send("Role added successfully", ephemeral=True)


@bot.component("chimera")
async def chimera(ctx: ComponentContext):
    role_to_add = 1017446851882008606
    if role_to_add in ctx.author.roles:
        await ctx.author.remove_role(role_to_add, ctx.guild.id)
        await ctx.send("Role removed successfully", ephemeral=True)
    else:
        await ctx.author.add_role(role_to_add, ctx.guild.id)
        await ctx.send("Role added successfully", ephemeral=True)


@bot.component("checkra1n")
async def checkra1n(ctx: ComponentContext):
    role_to_add = 1017446916549783582
    if role_to_add in ctx.author.roles:
        await ctx.author.remove_role(role_to_add, ctx.guild.id)
        await ctx.send("Role removed successfully", ephemeral=True)
    else:
        await ctx.author.add_role(role_to_add, ctx.guild.id)
        await ctx.send("Role added successfully", ephemeral=True)


@bot.component("appletv")
async def appletv(ctx: ComponentContext):
    role_to_add = 1017446193783115799
    if role_to_add in ctx.author.roles:
        await ctx.author.remove_role(role_to_add, ctx.guild.id)
        await ctx.send("Role removed successfully", ephemeral=True)
    else:
        await ctx.author.add_role(role_to_add, ctx.guild.id)
        await ctx.send("Role added successfully", ephemeral=True)


@bot.component("apple")
async def apple(ctx: ComponentContext):
    role_to_add = 1017447678373793862
    if role_to_add in ctx.author.roles:
        await ctx.author.remove_role(role_to_add, ctx.guild.id)
        await ctx.send("Role removed successfully", ephemeral=True)
    else:
        await ctx.author.add_role(role_to_add, ctx.guild.id)
        await ctx.send("Role added successfully", ephemeral=True)


@bot.component("android")
async def android(ctx: ComponentContext):
    role_to_add = 953374436747247616
    if role_to_add in ctx.author.roles:
        await ctx.author.remove_role(role_to_add, ctx.guild.id)
        await ctx.send("Role removed successfully", ephemeral=True)
    else:
        await ctx.author.add_role(role_to_add, ctx.guild.id)
        await ctx.send("Role added successfully", ephemeral=True)


@bot.component("man")
async def man(ctx: ComponentContext):
    role_to_add = 984074817370214401
    if role_to_add in ctx.author.roles:
        await ctx.author.remove_role(role_to_add, ctx.guild.id)
        await ctx.send("Role removed successfully", ephemeral=True)
    else:
        await ctx.author.add_role(role_to_add, ctx.guild.id)
        await ctx.send("Role added successfully", ephemeral=True)


@bot.component("woman")
async def woman(ctx: ComponentContext):
    role_to_add = 984074790858022964
    if role_to_add in ctx.author.roles:
        await ctx.author.remove_role(role_to_add, ctx.guild.id)
        await ctx.send("Role removed successfully", ephemeral=True)
    else:
        await ctx.author.add_role(role_to_add, ctx.guild.id)
        await ctx.send("Role added successfully", ephemeral=True)


@bot.component("other")
async def other(ctx: ComponentContext):
    role_to_add = 984074842733170728
    if role_to_add in ctx.author.roles:
        await ctx.author.remove_role(role_to_add, ctx.guild.id)
        await ctx.send("Role removed successfully", ephemeral=True)
    else:
        await ctx.author.add_role(role_to_add, ctx.guild.id)
        await ctx.send("Role added successfully", ephemeral=True)


if __name__ == '__main__':
    bot.start()
    # client.run(TOKEN)
