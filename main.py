#!/usr/bin/env python
import asyncio

async def main():

    print("test")


if __name__ == "__main__":
    loop=asyncio.get_event_loop()
    loop.run_until_complete(main())
