import random
import re
import asyncio
import discord
from discord.ext import commands

def setup_dice_commands(bot):
    @bot.command(name='r', aliases=['roll', 'dice', 'd'])
    async def roll_dice(ctx, *, command: str):
        try:
            command = command.strip().lower().replace(' ', '')
            # Accepts formats like 1d20+2, d6-1, 2d8, 20, etc.
            pattern = re.compile(r'^(?:(\d*)d)?(\d+)([+\-*/]\d+)?$')
            match = pattern.fullmatch(command)
            if not match:
                await ctx.send("Try `.r d20`, `.roll 2d6+3`, `.r 20`, etc.")
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

            rolls = [random.randint(1, dice_type) for _ in range(num_dice)]
            rolls_str = ', '.join(map(str, rolls))
            total = sum(rolls)

            # Apply modifier to the total
            if operator == '+':
                final_total = total + modifier
            elif operator == '-':
                final_total = total - modifier
            elif operator == '*':
                final_total = total * modifier
            elif operator == '/':
                if modifier == 0:
                    await ctx.send("Division by zero is not allowed.")
                    return
                final_total = total // modifier
            else:
                final_total = total

            nickname = ctx.author.nick or ctx.author.name

            embed = discord.Embed(title="🎲 Dice Roll", color=discord.Color.blue())
            embed.add_field(name="User", value=nickname, inline=True)
            embed.add_field(name="Dice", value=f"{num_dice}d{dice_type}", inline=True)
            if modifier_str:
                embed.add_field(name="Modifier", value=modifier_str, inline=True)
            embed.add_field(name="Rolls", value=rolls_str, inline=False)
            embed.add_field(name="Total", value=str(final_total), inline=True)

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"Oopsie: {e}")

def setup(bot):
    setup_dice_commands(bot)