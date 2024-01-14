# Copyright 2024, Dicky Herlambang "Nicklas373" <herlambangdicky5@gmail.com>
# Copyright 2016-2024, HANA-CI Build Project
# SPDX-License-Identifier: GPL-3.0-or-later
# This module based on https://github.com/Nicklas373/CGSS_ACB_Downloader that only
# have minimal function to track DB manifest version and report to user.

import telethon as tg
import requests
import json
from .. import command, module, util

class CgssModule(module.Module):
    name = "cgss"
    # disabled = True

    db: util.db.AsyncDB

    async def on_load(self) -> None:
        self.db = self.bot.get_db("cgss")

    async def on_message(self, event: tg.events.NewMessage.Event) -> None:
        pass

    @command.desc("Get information about latest manifest version from CGSS")
    @command.alias("get_manifest")
    async def cmd_cgss(self, ctx: command.Context) -> str:
        version=None
        verbose=True

        await ctx.respond("Loading...")\

        if not version:
            if verbose:
                try:
                    await ctx.respond("Getting game version ...")
                    url="https://starlight.kirara.ca/api/v1/info"
                    r=requests.get(url)
                    jsonData=json.loads(r.content)
                    version=jsonData['truth_version']
                except Exception as e:
                    await ctx.respond("No DB service was available!...")
                    version="NULL"
                else:
                    await ctx.respond("Getting game version from esterTion source...")
                    url="https://raw.githubusercontent.com/esterTion/cgss_master_db_diff/master/!TruthVersion.txt"
                    r=requests.get(url)
                    version=r.text.rstrip()

                await ctx.respond("Getting game version from local repository...")
                url="https://raw.githubusercontent.com/Nicklas373/CGSS_ACB_Downloader/master/Static_version"
                r=requests.get(url)
                old_version=r.text.rstrip()

                if (version > old_version):
                    reason="Local DB older than Dynamic DB!"
                elif (version == old_version):
                    reason="Local DB on latest version!"
                elif (version < old_version):
                    reason="Local DB higher than Dynamic DB, ERROR"

                result=(
                        f"**CGSS DB Manifest Ver.**\n"
                        f"\n"
                        f"**Local DB Ver.** : `{old_version}`\n"
                        f"**Online DB Ver.** : `{version}`\n"
                        f"**Status** : `{reason}`\n"
                        f"\n"
                        )
                await ctx.respond(result)

