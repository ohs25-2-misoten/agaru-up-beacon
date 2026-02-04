"""
Example for a BLE 4.0 Server
"""

import sys
import logging
import asyncio
import threading
import os

from typing import Any, Union
from dotenv import load_dotenv

from bless import (  # type: ignore
    BlessServer,
    BlessGATTCharacteristic,
    GATTCharacteristicProperties,
    GATTAttributePermissions,
)

load_dotenv()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(name=__name__)

# NOTE: Some systems require different synchronization methods.
trigger: Union[asyncio.Event, threading.Event]
if sys.platform in ["darwin", "win32"]:
    trigger = threading.Event()
else:
    trigger = asyncio.Event()


def read_request(characteristic: BlessGATTCharacteristic, **kwargs) -> bytearray:
    logger.debug(f"Reading {characteristic.value}")
    return characteristic.value


def write_request(characteristic: BlessGATTCharacteristic, value: Any, **kwargs):
    characteristic.value = value
    logger.debug(f"Char value set to {characteristic.value}")
    if characteristic.value == b"\x0f":
        logger.debug("NICE")
        trigger.set()


async def run(loop):
    trigger.clear()
    # Instantiate the server
    my_service_name = os.getenv("MY_SERVICE_NAME", "agaru-up-camera")
    server = BlessServer(name=my_service_name, loop=loop)
    server.read_request_func = read_request
    server.write_request_func = write_request

    # Add Service
    my_service_uuid = os.getenv("MY_SERVICE_UUID", "5c339364-c7be-4f23-b666-a8ff73a6a86a")
    await server.add_new_service(my_service_uuid)

    # Add a Characteristic to the service
    my_char_uuid = os.getenv("MY_CHAR_UUID", "ecf6c084-a579-42da-a7ff-f400fa4f4ae3")
    char_flags = (
        GATTCharacteristicProperties.read
    )
    my_char_data = bytearray(os.getenv("MY_CHAR_DATA"), "utf-8")

    permissions = GATTAttributePermissions.readable
    await server.add_new_characteristic(
        my_service_uuid, my_char_uuid, char_flags, my_char_data, permissions
    )

    logger.debug(server.get_characteristic(my_char_uuid))
    await server.start()
    logger.debug("Advertising")
    if trigger.__module__ == "threading":
        trigger.wait()
    else:
        await trigger.wait()

    await server.stop()


loop = asyncio.get_event_loop()
loop.run_until_complete(run(loop))
