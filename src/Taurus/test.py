import asyncio

from Taurus.helper import build_taurus


async def main():
    taurus = build_taurus()
    
    command = input("Enter a command for Taurus: ")
    
    while command != "exit":
        handler = await taurus.handle_command(command)
        command = input("Enter a command for Taurus: ")
        print(handler)
    if command == "exit":
        print("Exiting...")

if __name__ == "__main__":
    asyncio.run(main())