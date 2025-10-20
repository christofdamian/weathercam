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
    host = Host(HUB_IP, HUB_USER, HUB_PASSWORD, timeout=10)
    try:
        await asyncio.wait_for(host.get_host_data(), timeout=15)

        with open("output/snap.jpg", "wb") as image:
            snapshot = await asyncio.wait_for(host.get_snapshot(HUB_CAMERA_ID), timeout=10)
            image.write(snapshot)
    finally:
        try:
            await asyncio.wait_for(host.logout(), timeout=5)
            await asyncio.wait_for(host.unsubscribe(), timeout=5)
        except asyncio.TimeoutError:
            pass

if __name__ == "__main__":
    asyncio.run(snap())
