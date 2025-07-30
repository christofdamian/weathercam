#!/usr/bin/env python

from reolink_aio.api import Host
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

HUB_IP = os.environ.get("REOLINK_HUB_IP")
HUB_USER = os.environ.get("REOLINK_HUB_USER")
HUB_PASSWORD = os.environ.get("REOLINK_HUB_PASSWORD")
HUB_CAMERA_ID = int(os.environ.get("REOLINK_HUB_CAMERA_ID"))

async def snap():
    host = Host(HUB_IP, HUB_USER, HUB_PASSWORD)
    await host.get_host_data()

    with open("output/snap.jpg", "wb") as image:
        image.write(await host.get_snapshot(HUB_CAMERA_ID))

    await host.logout()

if __name__ == "__main__":
    asyncio.run(snap())
