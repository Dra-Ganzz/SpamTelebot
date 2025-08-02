import asyncio
import aiohttp
from rich.panel import Panel
from rich.console import Console
from rich.table import Table
from rich import box
import os

console = Console()

# Input data
token = input("BOT TOKEN: ")
chat_id = input("CHAT ID: ")
pesan = input("Pesan: ")
print("cintoh : /sdcard/namafile/gambar.jpg bebas pokonya gambar")
foto_path = input("masukan Foto (kosongkan jika tidak ada): ")
jumlah = int(input("Jumlah: "))

sem = asyncio.Semaphore(5)  # Batas maksimal concurrent task

async def spam(i):
    async with sem:
        async with aiohttp.ClientSession() as session:
            try:
                if foto_path and os.path.isfile(foto_path):
                    url = f"https://api.telegram.org/bot{token}/sendPhoto"
                    with open(foto_path, 'rb') as f:
                        data = aiohttp.FormData()
                        data.add_field('chat_id', chat_id)
                        data.add_field('caption', pesan)
                        data.add_field('photo', f, filename=os.path.basename(foto_path), content_type='image/jpeg')

                        async with session.post(url, data=data) as resp:
                            if resp.status == 200:
                                console.print(Panel(f"[{i+1}] ✓ Foto terkirim", width=50, style="green"))
                            else:
                                console.print(Panel(f"[{i+1}] ✗ Gagal kirim foto - Status {resp.status}", width=50, style="red"))
                else:
                    url = f"https://api.telegram.org/bot{token}/sendMessage"
                    async with session.post(url, data={"chat_id": chat_id, "text": pesan}) as resp:
                        if resp.status == 200:
                            console.print(Panel(f"[{i+1}] ✓ Pesan terkirim", width=50, style="green"))
                        elif resp.status == 429:
                            console.print(Panel(f"[{i+1}] > Rate Limit (429)", width=50, style="red"))
                        else:
                            console.print(Panel(f"[{i+1}] ✗ Gagal - Status {resp.status}", width=50, style="yellow"))
                await asyncio.sleep(0.5)
            except Exception as e:
                console.print(Panel(f"[{i+1}] Error: {str(e)}", width=50, style="bold red"))

async def main():
    tasks = [spam(i) for i in range(jumlah)]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    console.print(Panel("[bold cyan]Spam Telegram dengan Foto[/bold cyan]", subtitle="By Dra Vin", style="bold blue", width=50, box=box.ROUNDED))
    asyncio.run(main())
