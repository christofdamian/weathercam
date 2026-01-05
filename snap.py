#!/usr/bin/env python

from reolink_aio.api import Host
import asyncio
import os
from dotenv import load_dotenv
from PIL import Image
import logging
import argparse

load_dotenv()

HUB_IP = os.environ.get("REOLINK_HUB_IP")
HUB_USER = os.environ.get("REOLINK_HUB_USER")
HUB_PASSWORD = os.environ.get("REOLINK_HUB_PASSWORD")
HUB_CAMERA_ID = int(os.environ.get("REOLINK_HUB_CAMERA_ID"))

logger = logging.getLogger(__name__)

async def snap():
    host = Host(HUB_IP, HUB_USER, HUB_PASSWORD, timeout=10)
    temp_file = "output/snap.jpg.tmp"
    final_file = "output/snap.jpg"
    thumbnail_file = "output/snap_thumb.jpg"
    temp_thumbnail = "output/snap_thumb.jpg.tmp"

    try:
        logger.info(f"Connecting to camera hub at {HUB_IP}...")
        await asyncio.wait_for(host.get_host_data(), timeout=15)
        logger.info("Successfully connected to hub")

        # Write to temporary file first
        logger.info(f"Requesting snapshot from camera {HUB_CAMERA_ID}...")
        with open(temp_file, "wb") as image:
            snapshot = await asyncio.wait_for(host.get_snapshot(HUB_CAMERA_ID), timeout=10)
            image.write(snapshot)
        logger.info(f"Snapshot data received ({os.path.getsize(temp_file)} bytes)")

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
                    logger.info(f"Created thumbnail: {img.width}x{img.height} -> {max_width}x{new_height}")
                else:
                    # If image is already small, just copy it
                    img.save(temp_thumbnail, "JPEG", quality=85, optimize=True)
                    logger.info(f"Image is already small ({img.width}x{img.height}), optimized without resizing")

                # Replace both files atomically
                os.replace(temp_file, final_file)
                os.replace(temp_thumbnail, thumbnail_file)
                logger.info(f"Successfully saved snapshot to {final_file} and {thumbnail_file}")
            except Exception as e:
                logger.error(f"Error during thumbnail creation: {e}", exc_info=True)
                # Still save the full image even if thumbnail creation fails
                os.replace(temp_file, final_file)
                logger.info("Saved full image only (thumbnail creation failed)")
                if os.path.exists(temp_thumbnail):
                    os.remove(temp_thumbnail)
        else:
            file_size = os.path.getsize(temp_file) if os.path.exists(temp_file) else 0
            logger.error(f"Temporary snapshot file is empty or doesn't exist (size: {file_size} bytes)")
            if os.path.exists(temp_file):
                os.remove(temp_file)
    except asyncio.TimeoutError as e:
        logger.error(f"Timeout waiting for camera response", exc_info=True)
        logger.info(f"Check: 1) Camera is powered on, 2) Network connection, 3) Camera hub is accessible at {HUB_IP}")
        # Clean up temporary files if they exist
        if os.path.exists(temp_file):
            os.remove(temp_file)
        if os.path.exists(temp_thumbnail):
            os.remove(temp_thumbnail)
        logger.info("Keeping existing snapshot (if any)")
    except ConnectionError as e:
        logger.error(f"Cannot connect to camera hub at {HUB_IP}", exc_info=True)
        logger.info("Check network connectivity and hub IP address")
        # Clean up temporary files if they exist
        if os.path.exists(temp_file):
            os.remove(temp_file)
        if os.path.exists(temp_thumbnail):
            os.remove(temp_thumbnail)
        logger.info("Keeping existing snapshot (if any)")
    except OSError as e:
        logger.error(f"File system error - check disk space and permissions", exc_info=True)
        # Clean up temporary files if they exist
        if os.path.exists(temp_file):
            os.remove(temp_file)
        if os.path.exists(temp_thumbnail):
            os.remove(temp_thumbnail)
        logger.info("Keeping existing snapshot (if any)")
    except Exception as e:
        logger.error(f"Unexpected error during snapshot capture", exc_info=True)
        # Clean up temporary files if they exist
        if os.path.exists(temp_file):
            os.remove(temp_file)
        if os.path.exists(temp_thumbnail):
            os.remove(temp_thumbnail)
        logger.info("Keeping existing snapshot (if any)")
    finally:
        try:
            await asyncio.wait_for(host.logout(), timeout=5)
            await asyncio.wait_for(host.unsubscribe(), timeout=5)
        except asyncio.TimeoutError as e:
            logger.warning("Timeout during cleanup (logout/unsubscribe)")
        except Exception as e:
            logger.error("Error during cleanup (logout/unsubscribe)", exc_info=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Capture snapshot from Reolink camera")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging")
    args = parser.parse_args()

    # Configure logging
    # Priority: 1) LOG_LEVEL env var, 2) --verbose flag, 3) default to ERROR
    log_level_str = os.environ.get("LOG_LEVEL", "").upper()
    if log_level_str in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
        log_level = getattr(logging, log_level_str)
    elif args.verbose:
        log_level = logging.INFO
    else:
        log_level = logging.ERROR

    logging.basicConfig(
        level=log_level,
        format='[%(asctime)s] %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    asyncio.run(snap())
