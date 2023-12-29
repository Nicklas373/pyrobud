import json
import telethon as tg
import psutil
import subprocess
from .. import command, module, util

class vpsinfo(module.Module):
    name = "VPS Info"

    db: util.db.AsyncDB

    async def on_load(self) -> None:
        self.db = self.bot.get_db("vpsinfo")

    async def on_message(self, event: tg.events.NewMessage.Event) -> None:
        pass

    @command.desc("Docker Bot Container Ping")
    @command.alias("dockeralive")
    async def cmd_dockerping(self, ctx: command.Context) -> None:
        await ctx.respond("Bot Container is alive")

    @command.desc("Docker Bot Container Info")
    @command.alias("dockerinfo")
    async def cmd_dockerstats(self, ctx: command.Context) -> None:
        cpuName = "Docker Container Common CPU"
        cpuCoreCount = psutil.cpu_count(logical=True)
        cpuUsage = psutil.cpu_percent(interval=1)
        diskTotal = int(psutil.disk_usage('/').total/(1024*1024*1024))
        diskUsed = int(psutil.disk_usage('/').used/(1024*1024*1024))
        diskAvail = int(psutil.disk_usage('/').free/(1024*1024*1024))
        diskPercent = psutil.disk_usage('/').percent
        ramTotal = int(psutil.virtual_memory().total/(1024*1024))
        ramUsage = int(psutil.virtual_memory().used/(1024*1024))
        ramFree = int(psutil.virtual_memory().free/(1024*1024))
        ramUsagePercent = psutil.virtual_memory().percent
        upTime = subprocess.check_output(['uptime','-p']).decode('UTF-8')
        msg = '''
            HANA-CI VPS Info
--------------------------------

CPU Info
CPU Name                          = {}
CPU Core Count               = {} Cores
CPU Usage                          = {} %
CPU Uptime                       = {}
RAM Info
RAM Total Capacity         = {} MB
RAM Total Usage              = {} MB | {} %
RAM Total Free                 = {} MB

Storage Info
Storage Total Capacity    = {} GB
Storage Total Usage         = {} GB | {} %
Storage Total Free            = {} GB\n'''.format(cpuName,cpuCoreCount,cpuUsage,upTime,ramTotal,ramUsage,ramUsagePercent,ramFree,diskTotal,diskUsed,diskPercent,diskAvail)
        await ctx.respond(msg)

    @command.desc("Docker Container Application Logs")
    @command.alias("dockerlog")
    async def cmd_dockerlogs(self, ctx: command.Context) -> None:
        await ctx.respond("Sending logs...")
        try:
             print(subprocess.run(["/app/pyrobud/sendLaravelLog.sh", ""],capture_output=True))
        except subprocess.CalledProcessError as e:
             if e.output.startswith('error: {'):
                error = json.loads(e.output[7:])
                await ctx.respond("Error: "+error['message'])
             else:
                await ctx.respond("Error: "+e.output)
