import argparse
import asyncio
import json
from nats.aio.client import Client as NATS # type: ignore
from nats.aio.errors import ErrConnectionClosed, ErrTimeout, ErrNoServers # type: ignore
from utils import *

async def pump_fun_subscriber(catch=None, catch_all=None, notify=False):
    nats_server = "wss://prod-v2.nats.realtime.pump.fun"
    user = "subscriber"
    password = "lW5a9y20NceF6AE9"
    subject = "newCoinCreated.prod"

    notifiers = load_notifiers()

    nc = NATS()

    async def reconnect_handler():
        print("Reconnected to NATS!")

    async def disconnect_handler():
        print("Disconnected from NATS.")

    try:
        print("✅ Attempting to connect to NATS...")

        await nc.connect(
            servers=[nats_server],
            user=user,
            password=password,
            reconnect_time_wait=2,
            max_reconnect_attempts=10,
            allow_reconnect=True
        )

        print(f"✅ Connected to NATS")

        async def message_handler(msg):
            data = json.loads(msg.data.decode())
            creator = data.get("creator")

            token_info = f"🚨 Token discovered!\n" \
                         f"Mint: {data['mint']}, Name: {data['name']}, Symbol: ${data['symbol']}, " \
                         f"Description: {data['description']}, Creator: {data['creator']}, " \
                         f"UsdMarketCap: {data['usd_market_cap']}\n"

            if catch and catch == creator:
                print(token_info)
                if notify:
                    notify_new_token(token_info, notifiers)

            if catch_all and creator in catch_all:
                print(token_info)
                if notify:
                    notify_new_token(token_info, notifiers)

            if not catch and not catch_all:
                print(token_info)
                if notify:
                    notify_new_token(token_info, notifiers)

        print(f"✅ Starting to monitor pump.fun\n")
        await nc.subscribe(subject, cb=message_handler)

        while True:
            await asyncio.sleep(1)

    except ErrConnectionClosed:
        print("Connection closed unexpectedly.")
    except ErrTimeout:
        print("Timeout occurred while connecting.")
    except ErrNoServers:
        print("No NATS servers available.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        await nc.close()
        print("Disconnected from NATS.")

def parse_args():
    parser = argparse.ArgumentParser(description="Pump Fun Subscriber")
    parser.add_argument("-catch", type=str, help="Specify a creator to catch")
    parser.add_argument("-catchAll", type=str, help="Specify a file location to read creators")
    parser.add_argument("-notify", action="store_true", help="Enable notifications (Not implemented yet)")

    return parser.parse_args()

def load_creators_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            creators = [line.strip() for line in file.readlines()]
        return creators
    except Exception as e:
        print(f"Failed to load creators from file: {e}")
        return []

if __name__ == "__main__":
    args = parse_args()
    catch = args.catch
    catch_all = None
    if args.catchAll:
        catch_all = load_creators_from_file(args.catchAll)
    notify = args.notify

    print(banner)
    asyncio.run(pump_fun_subscriber(catch, catch_all, notify))
