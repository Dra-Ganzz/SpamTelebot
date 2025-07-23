# pakai async agar lancar jaya
import asyncio
import aiohttp
from rich.panel import Panel
from rich.console import Console
from rich.table import Table
from rich import box

console = Console()

# Masukan data
token = input("Masukan BOT TOKEN: ")
chat_id = input("Masukan CHAT ID: ")
pesan = input("Masukan Pesan: ")
jumlah = int(input("Masukan Jumlah: "))

url = f"https://api.telegram.org/bot{token}/sendMessage"
sem = asyncio.Semaphore(5)  # Batas maksimal concurrent task

async def spam(i):
    async with sem:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, data={"chat_id": chat_id, "text": pesan}) as resp:
                    if resp.status == 200:
                        console.print(Panel(f"[{i+1}] ✓ Terkirim", width=40, style="green"))
                    elif resp.status == 429:
                        console.print(Panel(f"[{i+1}] > Rate Limit (429)", width=40, style="red"))
                    else:
                        console.print(Panel(f"[{i+1}] > Gagal - Status {resp.status}", width=40, style="yellow"))
                await asyncio.sleep(0.5)
            except Exception as e:
                console.print(Panel(f"[{i+1}] Error: {str(e)}", width=40, style="bold red"))

async def main():
    tasks = [spam(i) for i in range(jumlah)]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    console.print(Panel("[bold cyan]Spam Token Telegram[/bold cyan]", subtitle="By Dra Vin", style="bold blue", width=40, box=box.ROUNDED))
    asyncio.run(main())
