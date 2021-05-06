from asyncio import sleep
from datetime import datetime
from glob import glob
from discord import Intents
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord import Embed
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import CommandNotFound
from ..db import db

PREFIX = "+"
OWNER_IDS = [137285426015764481]
COGS = [path.split("\\")[-1][:-3] for path in glob("./lib/cogs/*.py")]


class Ready(object):
    def __init__(self):
        for cog in COGS:
            setattr(self, cog, False)
    
    def ready_up(self, cog):
        setattr(self, cog, True)
        print(f"{cog} cog ready")

    def all_ready(self):
        return all([getattr(self, cog) for cog in COGS])

class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.cogs_ready = Ready()
        self.guild = None
        self.scheduler = AsyncIOScheduler()

        db.autosave(self.scheduler)

        super().__init__(
            command_prefix=PREFIX, 
            owner_ids=OWNER_IDS,
            intents = Intents.all()
        )

    def setup(self):
        for cog in COGS:
            self.load_extension(f"lib.cogs.{cog}")
            print(f"{cog} cog loaded.")

        print("setup complete")

    def run(self, version):
        self.VERSION = version

        print("running setup...")
        self.setup()

        with open("./lib/bot/token.0", "r", encoding="utf-8") as tf:
            self.TOKEN = tf.read()

            print("running bot...")
            super().run(self.TOKEN, reconnect=True)

    async def print_message(self): #Mesaj gonderen basit bit fonksiyon
        await self.stdout.send("I am a timed notification!")

    async def on_connect(self):
        print("bot connected")

    async def on_disconnect(self):
        print("bot disconnected")

    async def on_error(self, err, *args, **kwarg):
        if err == "on_command_error":
            await arsg[0].send("Something went wrong.")
        
        await self.stdout.send("An error occured.")
        raise

    async def on_command_error(self, ctx, exc):
        if isinstance(exc, CommandNotFound):
            pass

        elif hasattr(exc, "original"):
            raise exc.original
        
        else:
            raise exc

    async def on_ready(self):
        if not self.ready:
            self.guild = self.get_guild(838757067527421952) #sever id
            self.stdout = self.get_channel(838764006042894366)
            # self.scheduler.add_job(self.print_message, CronTrigger(second="0,15,30,45")) #her 15 saniyede mesaj gönderiyor.
            self.scheduler.start()
        
           
            
            """ # Bu kisimi su anlik artık on_ready de kullanmamiza gerek yok sonra baska bir yere alirim 
            embed = Embed(title="Now online!", description="YBKBOT is now online!",
                          colour=0x323373, timestamp=datetime.utcnow())

            fields = [("Name", "Value", True),
                      ("Another field", "This field is next to the other one", True),
                      ("A non-inline field", "this field ll appear on it's own", False)]
            
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            embed.set_author(name="FBU Yazılım ve Bilişim Kulübü", icon_url=self.guild.icon_url)
            embed.set_footer(text="This is a footer!")
            embed.set_thumbnail(url=self.guild.icon_url)
            embed.set_image(url=self.guild.icon_url)
            await channel.send(embed=embed)  """
            # await channel.send(file=File("{path}"))
            
            
            while not self.cogs_ready.all_ready():
                await sleep(0.5)

            await self.stdout.send("Now online!")
            self.ready = True
            print("bot ready")
            
        else:
            print("Bot reconnected")


    async def on_message(self, message):
        if not message.author.bot:
            await self.process_commands(message)

bot = Bot()