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

    @command.desc("Check Pyrobud Ping")
    @command.alias("vps_alive")
    async def cmd_dockerping(self, ctx: command.Context) -> None:
        await ctx.respond("Pyrobud Container is alive")

    @command.desc("Check OS Host System Info")
    @command.alias("vps_info")
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
            HANA-CI Host VPS Info
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

    @command.desc("Send Application Logs")
    @command.alias("vps_logs")
    async def cmd_dockerlogs(self, ctx: command.Context) -> None:
        await ctx.respond("Sending logs...")
        try:
             subprocess.run(["/app/pyrobud/sendLaravelLog.sh", ""],capture_output=True)
             await ctx.respond("Logs has been sent!")
        except subprocess.CalledProcessError as e:
             if e.output.startswith('error: {'):
                error = json.loads(e.output[7:])
                await ctx.respond("Error: "+error['message'])
             else:
                await ctx.respond("Error: "+e.output)
