#!/usr/bin/env python

from reolink_aio.api import Host
import asyncio
import os
from dotenv import load_dotenv
from PIL import Image

load_dotenv()

HUB_IP = os.environ.get("REOLINK_HUB_IP")
HUB_USER = os.environ.get("REOLINK_HUB_USER")
HUB_PASSWORD = os.environ.get("REOLINK_HUB_PASSWORD")
HUB_CAMERA_ID = int(os.environ.get("REOLINK_HUB_CAMERA_ID"))

async def snap():
    host = Host(HUB_IP, HUB_USER, HUB_PASSWORD, timeout=10)
    temp_file = "output/snap.jpg.tmp"
    final_file = "output/snap.jpg"
    thumbnail_file = "output/snap_thumb.jpg"
    temp_thumbnail = "output/snap_thumb.jpg.tmp"

    try:
        await asyncio.wait_for(host.get_host_data(), timeout=15)

        # Write to temporary file first
        with open(temp_file, "wb") as image:
            snapshot = await asyncio.wait_for(host.get_snapshot(HUB_CAMERA_ID), timeout=10)
            image.write(snapshot)

        # Only replace the old file if we successfully got a new snapshot
        if os.path.exists(temp_file) and os.path.getsize(temp_file) > 0:
            # Create thumbnail version for faster loading
            try:
                img = Image.open(temp_file)
                # Calculate thumbnail size (max width 1200px, maintaining aspect ratio)
                max_width = 1200
                if img.width > max_width:
                    ratio = max_width / img.width
                    new_height = int(img.height * ratio)
                    img_resized = img.resize((max_width, new_height), Image.LANCZOS)
                    img_resized.save(temp_thumbnail, "JPEG", quality=85, optimize=True)
                    print(f"Created thumbnail: {img.width}x{img.height} -> {max_width}x{new_height}")
                else:
                    # If image is already small, just copy it
                    img.save(temp_thumbnail, "JPEG", quality=85, optimize=True)
                    print(f"Image is already small ({img.width}x{img.height}), optimized without resizing")

                # Replace both files atomically
                os.replace(temp_file, final_file)
                os.replace(temp_thumbnail, thumbnail_file)
                print(f"Successfully saved snapshot to {final_file} and {thumbnail_file}")
            except Exception as e:
                print(f"Error creating thumbnail: {e}")
                # Still save the full image even if thumbnail creation fails
                os.replace(temp_file, final_file)
                print(f"Saved full image only")
                if os.path.exists(temp_thumbnail):
                    os.remove(temp_thumbnail)
        else:
            print(f"Error: Temporary snapshot file is empty or doesn't exist")
            if os.path.exists(temp_file):
                os.remove(temp_file)
    except Exception as e:
        print(f"Error getting snapshot: {e}")
        # Clean up temporary files if they exist
        if os.path.exists(temp_file):
            os.remove(temp_file)
        if os.path.exists(temp_thumbnail):
            os.remove(temp_thumbnail)
        print(f"Keeping existing snapshot (if any)")
    finally:
        try:
            await asyncio.wait_for(host.logout(), timeout=5)
            await asyncio.wait_for(host.unsubscribe(), timeout=5)
        except asyncio.TimeoutError:
            pass

if __name__ == "__main__":
    asyncio.run(snap())
