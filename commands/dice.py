import random
import re
import asyncio
import discord
from discord.ext import commands

def setup_dice_commands(bot):
    @bot.command(name='r', aliases=['roll', 'dice', 'd'])
    async def roll_dice(ctx, *, command: str):
        try:
            command = re.sub(r'\s+', ' ', command.strip().lower())

            command_for_parse = re.sub(r'\s*([+\-*/])\s*', r'\1', command)

            pattern = re.compile(r'^(?:(\d+)[d ]\s*)?(\d+)([+\-*/]\d+)?$')
            match = pattern.fullmatch(command_for_parse)
            if not match:
                await ctx.send("Try `.r d20`, `.roll 2d6+3`, `.r 2 6 -3`, `.r 20`, `.r 3 20 + 2`, etc.")
                return

            num_dice = int(match.group(1)) if match.group(1) else 1
            dice_type = int(match.group(2))
            modifier_str = match.group(3)
            modifier = int(modifier_str[1:]) if modifier_str else 0
            operator = modifier_str[0] if modifier_str else '+'

            if num_dice > 50:
                await ctx.send("Too many dice! Max is 50.")
                return

            if dice_type < 1:
                await ctx.send("Dice must have at least 1 side.")
                return

            results = [random.randint(1, dice_type) for _ in range(num_dice)]

            # Apply modifier to each roll
            modified_results = []
            for roll in results:
                if operator == '+':
                    modified = roll + modifier
                elif operator == '-':
                    modified = roll - modifier
                elif operator == '*':
                    modified = roll * modifier
                elif operator == '/':
                    if modifier == 0:
                        await ctx.send("Division by zero is not allowed.")
                        return
                    modified = roll // modifier
                else:
                    modified = roll
                modified_results.append(modified)

            results_str = ', '.join(map(str, modified_results))
            max_possible = num_dice * dice_type
            percentage = (sum(modified_results) / max_possible) * 100 if max_possible else 0

            nickname = ctx.author.nick or ctx.author.name

            embed = discord.Embed(title="🎲 Roll Stats", color=discord.Color.blue())
            embed.add_field(name="User", value=nickname, inline=True)
            embed.add_field(name="Dice Roll", value=command, inline=True)
            embed.add_field(name="Results", value=results_str, inline=False)
            if num_dice > 1:
                embed.add_field(name="Total", value=sum(modified_results), inline=True)

            awesome_dice = [
                "https://tenor.com/view/vergil-grin-devil-may-cry5-thumbs-up-smile-gif-26758676",
                "https://tenor.com/view/dante-dmc-mog-dante-sparda-devil-may-cry-gif-633545941459700262",
                "FILL 🧨🧨🧨✨ POW POW POW 🎇🎆🎆🎇💥💥🎆✨🎇BOOM BOOM✨🎆🎆🎉🎉🎆TRATRATRA🎆🎇💥💥🎆POW FIIIIIIU 🎆🎉🎇✨🎆🎆🧨🎆✨",
                "https://tenor.com/view/robert-downey-jr-explaining-speech-bubble-transparent-gif-25987307",
                "https://tenor.com/view/starman-superman-super-man-theres-a-starman-there-gif-11906140510431067153"
            ]
            
            nice_dice = [
                "https://tenor.com/view/vegeta-method-do-you-want-the-method-speech-bubble-the-method-gif-6979719801801243503",
                "https://tenor.com/view/yungviral-gif-865009269088736323",
                "https://tenor.com/view/oh-great-ok-the-rock-gif-18017054636487826799",
            ]

            medium_dice = [
                "https://tenor.com/view/tamm-cat-gif-1067625986375071026",
                "https://tenor.com/view/reimu-hakurei-retro-live-reaction-live-reimu-reaction-gif-25108998",
                "https://tenor.com/view/vergil-reaction-to-this-information-gif-15147410473022148700",
            ]

            terrible_dice = [
                "https://tenor.com/view/eggman-speech-bubble-gif-25564771",
                "https://tenor.com/view/speechbubble-speech-bubble-please-meme-gif-25693113",
                "https://tenor.com/view/touhou-reimu-reimu-hakurei-live-reaction-goku-stare-gif-17843086582445113317",
                "https://tenor.com/view/owl-standing-gif-4614094214811740127",
                "https://tenor.com/view/bubble-text-owl-text-bubble-bubble-text-owl-bubble-text-speech-bubble-owl-gif-25466686",
                "https://tenor.com/view/cahara-fear-and-hunger-crowmauler-terrifying-presence-gif-11660160882700055465",
                "https://tenor.com/view/ohno-meme-monkey-ohno-ohno-monkey-ohno-emote-ohno-twitch-emote-gif-119989999548046247",
                "https://tenor.com/view/astolfo-speech-bubble-discord-monster-gif-26662120",
                "https://tenor.com/view/dmc5-gif-14000810",
                "https://tenor.com/view/vergil-dmc5-dmc-5-my-honest-my-honest-reaction-gif-15208154529352500531",
                "https://tenor.com/view/aaah-gif-10038493696838146297",
                "https://tenor.com/view/bocchi-bocchi-the-rock-hitori-gotoh-gif-27259628",
                "https://tenor.com/view/peter-griffin-fly-meme-gif-22525004",
                "https://tenor.com/view/saul-goodman-meme-speech-bubble-saul-goodman-gif-25296783",
                "https://tenor.com/view/you-deer-deer-dark-souls-nokotan-my-deer-friend-nokotan-gif-15144319581244726751"
            ]

            if num_dice == 1 and dice_type == 4 and total == 1:
                deathMessages = [
                    "My name's Mei and your fate has been sealed",
                    "it was nice to have you here",
                    "your time has come",
                    "さよなら",
                    "Rest in peace",
                    "roses are red like your blood...",
                    "Is this the end you wished for?"
                ]

                deathMessage = random.choice(deathMessages)

                await ctx.send(f"{nickname} you see a glimpse of your whole life passing through your eyes...")
                await asyncio.sleep(0.5)
                await ctx.send(deathMessage)
                await asyncio.sleep(0.7)
                await ctx.send("https://tenor.com/view/he-gone-dead-hella-dead-gif-20116498")
                return
            
            if num_dice  == 1 and dice_type == 2 and total == 2:
                await asyncio.sleep(0.2)
                await ctx.send(f"{nickname}, flipped a coin...")
                await asyncio.sleep(0.6)
                await ctx.send("https://tenor.com/view/fear-and-hunger-coin-flip-heads-gif-1404393224500712989")
                return
            
            if num_dice == 1 and dice_type == 2 and total == 1:
                await asyncio.sleep(0.2)
                await ctx.send(f"{nickname}, flipped a coin...")
                await asyncio.sleep(0.6)
                await ctx.send("https://tenor.com/view/fear-and-hunger-coin-flip-tails-gif-2938111952525768260")
                return
            
            if num_dice == 2 and dice_type == 2 and total == 3:
                await asyncio.sleep(0.2)
                await ctx.send(f"{nickname}, flipped two coins...")
                await asyncio.sleep(0.6)
                await ctx.send("https://tenor.com/view/fear-and-hunger-coin-flip-lucky-coin-heads-tails-gif-6370455690319299531")
                return

            if num_dice == 2 and dice_type == 2 and total == 2:
                await asyncio.sleep(0.2)
                await ctx.send(f"{nickname}, flipped two coins...")
                await asyncio.sleep(0.6)
                await ctx.send("https://tenor.com/view/fear-and-hunger-coin-flip-lucky-coin-tails-tails-gif-586030300076156221")
                return

            if num_dice == 2 and dice_type == 2 and total == 4:
                await asyncio.sleep(0.2)
                await ctx.send(f"{nickname}, flipped two coins...")
                await asyncio.sleep(0.6)
                await ctx.send("https://tenor.com/view/fear-and-hunger-coin-flip-lucky-coin-heads-heads-gif-11655328672403159466")
                return

            if percentage == 100:
                image = random.choice(awesome_dice)
            elif percentage >= 85:
                image = random.choice(nice_dice)
            elif percentage >= 60:
                image = random.choice(medium_dice)
            else:
                image = random.choice(terrible_dice)

            await ctx.send(embed=embed)
            await asyncio.sleep(0.2)
            await ctx.send("my honest reaction...")
            await asyncio.sleep(0.6)
            await ctx.send(image)

        except Exception as e:
            await ctx.send(f"Oopsie: {e}")

def setup(bot):
    setup_dice_commands(bot)