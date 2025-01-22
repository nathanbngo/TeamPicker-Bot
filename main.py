import discord
from discord.ext import commands
from discord.ext.commands import DefaultHelpCommand
import random
import math
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# Bot setup
intents = discord.Intents.all()
intents.messages = True
intents.message_content = True  # Enable message content for attachment handling
bot = commands.Bot(command_prefix=">", intents=intents)

# Persistent list of names and skills
name_list = []
skill_levels = {}  # Dictionary to store skill levels for each name
default_skill = 3
teams = []

def validate_groups(groups, name_list):
    """
    Ensure groups contain only valid names.
    """
    for group in groups:
        for name in group:
            if name not in name_list:
                raise ValueError(f"Invalid group member: {name}")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    
@bot.command()
async def shuffle(ctx, *, args=None):
    """
    Shuffle names into teams.
    Usage:
    >shuffle team_size=<size> names=<name_list>
    >shuffle num_teams=<number> names=<name_list>
    If no arguments are provided, reshuffle existing teams.
    """
    global name_list, skill_levels, teams

    # Parse arguments if provided
    if args:
        params = {k: v for k, v in (arg.split('=') for arg in args.split())}
        if 'names' in params:
            raw_names = params.get('names', '').split(',')
            name_count = {}
            name_list = []
            for name in raw_names:
                if name in name_count:
                    name_count[name] += 1
                    name_list.append(f"{name}({name_count[name]})")
                else:
                    name_count[name] = 1
                    name_list.append(name)

                # Ensure every name has a default skill level
                if name not in skill_levels:
                    skill_levels[name] = default_skill
        raw_groups = params.get('group', '').split(';') if 'group' in params else []
        groups = [g.split(',') for g in raw_groups]

        try:
            validate_groups(groups, name_list)
        except ValueError as e:
            await ctx.send(str(e))
            return

        team_size = int(params.get('team_size', 0))
        num_teams = int(params.get('num_teams', 0))
    else:
        if not name_list:
            await ctx.send("No existing data to reshuffle. Please provide parameters.")
            return
        team_size = 0
        num_teams = len(teams)
        groups = []

    # Calculate the number of teams or adjust based on team size
    total_names = len(name_list) + sum(len(group) for group in groups)

    if team_size > 0:
        num_teams = math.ceil(total_names / team_size)
    elif num_teams > 0:
        num_teams = num_teams
    else:
        await ctx.send("Please specify either team_size or num_teams.")
        return

    # Ensure no more teams than necessary
    num_teams = min(num_teams, total_names)

    # Shuffle and divide names into balanced teams based on skill levels
    teams = [[] for _ in range(num_teams)]
    team_skills = [0] * num_teams

    for group in groups:
        # Add entire groups to the least skilled team
        best_team_index = min(range(num_teams), key=lambda i: team_skills[i])
        teams[best_team_index].extend(group)
        team_skills[best_team_index] += sum(skill_levels.get(name, default_skill) for name in group)
        for name in group:
            if name in name_list:
                name_list.remove(name)

    for name in name_list:
        # Assign remaining names to the team with the lowest total skill level
        best_team_index = min(range(num_teams), key=lambda i: team_skills[i])
        teams[best_team_index].append(name)
        team_skills[best_team_index] += skill_levels.get(name, default_skill)

    # Generate response
    response = "Teams:\n"
    for i, team in enumerate(teams, start=1):
        avg_skill = team_skills[i - 1] / len(team) if team else 0
        response += f"Team {i} (Avg Skill: {avg_skill:.2f}): {', '.join(team)}\n"

    await ctx.send(response)

@bot.command()
async def addSkill(ctx, *, args):
    """
    Add a person to the list with a specific skill level (1-5).
    Usage: >addSkill name=<name> skill=<level>
    """
    global name_list, skill_levels

    params = {k: v for k, v in (arg.split('=') for arg in args.split())}
    name = params.get('name')
    skill = int(params.get('skill', default_skill))

    if not name:
        await ctx.send("Please provide a name.")
        return

    if skill < 1 or skill > 5:
        await ctx.send("Skill level must be between 1 and 5.")
        return

    if name in name_list:
        await ctx.send(f"{name} is already in the list with skill level {skill_levels[name]}.")
        return

    name_list.append(name)
    skill_levels[name] = skill
    await ctx.send(f"Added {name} with skill level {skill} to the list.")

@bot.command()
async def changeSkill(ctx, *, args):
    """
    Change the skill level of an existing person (1-5).
    Usage: >changeSkill name=<name> skill=<level>
    """
    global skill_levels

    params = {k: v for k, v in (arg.split('=') for arg in args.split())}
    name = params.get('name')
    skill = int(params.get('skill', default_skill))

    if not name:
        await ctx.send("Please provide a name.")
        return

    if name not in skill_levels:
        await ctx.send(f"{name} is not in the list.")
        return

    if skill < 1 or skill > 5:
        await ctx.send("Skill level must be between 1 and 5.")
        return

    skill_levels[name] = skill
    await ctx.send(f"Updated {name}'s skill level to {skill}.")

    # Reshuffle and show updated teams
    await shuffle(ctx)

@bot.command()
async def viewSkill(ctx):
    """
    View the skill levels of all people in the list.
    Usage: >viewSkill
    """
    global skill_levels

    if not skill_levels:
        await ctx.send("No skill data available.")
        return

    response = "Skill Levels:\n"
    for name, skill in skill_levels.items():
        response += f"{name}: {skill}\n"

    await ctx.send(response)

@bot.command()
async def example(ctx):
    """
    Provide examples of how to use the commands.
    """
    examples = (
        "**Examples:**\n"
        ">shuffle team_size=3 names=Alice,Bob,Charlie,David\n"
        ">shuffle num_teams=2 names=Alice,Bob,Charlie,David group=Alice,Bob\n"
        ">shuffle team_size=2 names=Alice,Bob,Charlie,Nathan group=Alice,Bob;Charlie,Nathan\n"
        ">addSkill name=Alice skill=4\n"
        ">changeSkill name=Bob skill=5\n"
        ">viewSkill\n"
        ">save teams.txt\n"
        ">load teams.txt"
    )
    await ctx.send(examples)

@bot.command()
async def add(ctx, *, name):
    """
    Add a person to the global list of names and readjust teams.
    Usage: >add <name>
    """
    global name_list
    if name in name_list:
        await ctx.send(f"{name} is already in the list.")
        return
    count = sum(1 for n in name_list if n.startswith(name))
    if count > 0:
        name = f"{name}({count + 1})"
    name_list.append(name)
    skill_levels[name] = default_skill  # Assign default skill level
    await ctx.send(f"Added {name} to the list.")

    # Reshuffle and show updated teams
    await shuffle(ctx)


@bot.command()
async def remove(ctx, *, name):
    """
    Remove a person from the global list of names and readjust teams.
    Usage: >remove <name>
    """
    global name_list
    for n in name_list:
        if n == name or n.startswith(name):
            name_list.remove(n)
            del skill_levels[name]  # Remove skill level entry
            await ctx.send(f"Removed {n} from the list.")

            # Reshuffle and show updated teams
            await shuffle(ctx)
            return
    await ctx.send(f"{name} is not in the list.")

@bot.command()
async def list(ctx):
    """
    Display the current list of names.
    Usage: >list
    """
    global name_list
    if name_list:
        await ctx.send(f"Current list: {', '.join(name_list)}")
    else:
        await ctx.send("The list is currently empty.")

@bot.command()
async def teams(ctx):
    """
    Show the current teams.
    Usage: >teams
    """
    global teams

    if not teams:
        await ctx.send("Teams are currently empty.")
        return

    response = "Current Teams:\n"
    for i, team in enumerate(teams, start=1):
        response += f"Team {i}: {', '.join(team)}\n"
    await ctx.send(response)

@bot.command()
async def switch(ctx, name1: str, name2: str):
    """
    Switch two people between teams.
    Usage: >switch <name1> <name2>
    """
    global teams
    found_name1 = found_name2 = False
    team1_index = team2_index = None

    for i, team in enumerate(teams):
        if name1 in team:
            team1_index = i
            found_name1 = True
        if name2 in team:
            team2_index = i
            found_name2 = True

    if found_name1 and found_name2:
        teams[team1_index].remove(name1)
        teams[team2_index].remove(name2)
        teams[team1_index].append(name2)
        teams[team2_index].append(name1)
        response = "Teams after switch:\n"
        for i, team in enumerate(teams, start=1):
            response += f"Team {i}: {', '.join(team)}\n"
        await ctx.send(response)
    else:
        await ctx.send(f"One or both names not found in teams: {name1}, {name2}")

@bot.command()
async def load(ctx):
    """
    Load names and optional skill levels from a .txt file attached to the message.
    Usage: >load (with a .txt file attachment)
    Each line in the file should be formatted as:
      Name [Skill Level]
    Example:
      Alice 4
      Bob
      Charlie 2
    """
    global name_list, skill_levels

    if not ctx.message.attachments:
        await ctx.send("Please attach a .txt file with the command.")
        return

    attachment = ctx.message.attachments[0]
    if not attachment.filename.endswith(".txt"):
        await ctx.send("Only .txt files are supported.")
        return

    try:
        file_content = await attachment.read()
        lines = file_content.decode("utf-8").strip().split("\n")

        for line in lines:
            parts = line.rsplit(" ", 1)
            name = parts[0].strip()
            skill = default_skill

            if len(parts) > 1 and parts[1].isdigit():
                skill = int(parts[1])
                skill = max(1, min(skill, 5))  # Ensure skill level is between 1 and 5

            name_list.append(name)
            skill_levels[name] = skill

        await ctx.send(f"Loaded names and skill levels from {attachment.filename}.")

    except Exception as e:
        await ctx.send(f"An error occurred while loading the file: {e}")

@bot.command()
async def clear(ctx):
    """
    Clear all names and skill levels.
    Usage: >clear
    """
    global name_list, skill_levels, teams
    name_list.clear()
    skill_levels.clear()
    teams = []  # Reinitialize teams as an empty list
    await ctx.send("All names, skill levels, and teams have been cleared.")

# Custom Help Command Class
class CustomHelpCommand(DefaultHelpCommand):
    def __init__(self):
        super().__init__()
        self.indent = 4
        self.sort_commands = True
        self.no_category = 'Bot Commands'

    async def send_bot_help(self, mapping):
        """
        Customize the bot-wide help command output.
        """
        ctx = self.context
        help_message = "**Team Picker Bot Commands:**\n"

        help_message += (
            "\n__File Commands__\n"
            ">load <file_name>: Load names from a .txt file. Format: Each name on a new line. 'Nathan' or 'Nathan 5'\n"
            ">example: Show examples of how to use the commands.\n"
            "\n__Skill Commands__\n"
            ">addSkill name=<name> skill=<level>: Add a person with a specific skill level (1-5).\n"
            ">changeSkill name=<name> skill=<level>: Change the skill level of an existing person.\n"
            ">viewSkill: View the skill levels of all people in the list.\n"
            "\n__Team Commands__\n"
            ">teams: Show the current teams.\n"
        )

        for cog, commands in mapping.items():
            commands = await self.filter_commands(commands, sort=True)
            if not commands:
                continue

            cog_name = cog.qualified_name if cog else self.no_category
            help_message += f"\n__{cog_name}__\n"
            for command in commands:
                help_message += f"`{self.context.prefix}{command}`: {command.short_doc}\n"

        await ctx.send(help_message)

    async def send_command_help(self, command):
        """
        Customize help output for a specific command.
        """
        help_message = f"**Command:** `{self.context.prefix}{command}`\n"
        help_message += f"{command.help}\n"
        await self.context.send(help_message)


# Assign the custom help command to the bot
bot.help_command = CustomHelpCommand()

# Run the bot with token from .env file
if BOT_TOKEN:
    bot.run(BOT_TOKEN)
else:
    print("Error: DISCORD_BOT_TOKEN not found in .env file.")