import os
import discord
from discord.ext import commands, tasks
from discord.ext.commands import Context, bot

intents = discord.Intents.default()
intents.typing | intents.presences

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)
        self.commands = {}

    async def setup_hook(self):
        await self.wait_until_ready()
        print("Bot is ready")

        # load commands from folder
        command_files = [f for f in os.listdir("./commands") if f.endswith(".py")]

        for file in command_files:
            module = __import__(f"commands.{file.split('.')[0]}", fromlist=["Command"])
            self.add_command(module.Command)

    async def event_command_interaction(self, interaction):
        if not interaction or not interaction.is_command():
            return

        command = self.get_command(interaction.name)
        if not command:
            return

        await command.invoke(context=Context(interaction))

class Command:
    async def invoke(self, context: Context):
        pass

async def main():
    bot = Bot()
    token = os.environ['TOKEN']
    await bot.start(token)

@tasks.loop(seconds=30.0)
async def autostart():
    if not bot.is_closed:
        await bot.wait_until_ready()

if __name__ == "__main__":
    main()