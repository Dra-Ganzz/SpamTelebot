import asyncio
import aiohttp
import random
from rich.panel import Panel
from rich.console import Console
from rich import box
import os

console = Console()

# token bisa di tambahkan lagi
tokens = [
    "7224304462:AAFUoaFbB7njkEyaH0EAoTovYpDJRjTifW8",
    "7465534118:AAHfWtdkkcsSb65oP2ELL_djpKJsqe1h2cg",
    "7386271666:AAH7Fm_388SADza6CHTZh82CZB6jXMSq3UY"
]

# Chat ID tujuan
chat_id = "5034446293"

# Daftar pesan random
pesan_list = [
    "ISI TEXT APA SAJA",
    "ISI TEXT APA SAJA",
    "ISI TEXT APA SAJA",
    "ISI TEXT APA SAJA",
    "ISI TEXT APA SAJA",
    "ISI TEXT APA SAJA",
    "ISI TEXT APA SAJA",
    "ISI TEXT APA SAJA",
    "ISI TEXT APA SAJA", # Bisa di tambahkan lagi text random nya 
]

# Daftar foto random (isi path lengkap fotonya)
poto = [
    "/sdcard/IMG-20250802-WA0015.jpg",
    "/sdcard/IMG-20250710-WA0106.jpg",
    "/sdcard/IMG-20241225-WA0040.jpg",
    None  # kadang hanya teks saja
]

# Input jumlah spam
jumlah = int(input("Jumlah: "))

# Batas maksimal concurrent task
sem = asyncio.Semaphore(5)

async def spam(i):
    async with sem:
        async with aiohttp.ClientSession() as session:
            try:
                # Pilih token random
                token = random.choice(tokens)
                # Pilih pesan random
                pesan = random.choice(pesan_list)
                # Pilih foto random (atau None)
                foto_path = random.choice(poto)

                if foto_path and os.path.isfile(foto_path):
                    # Kirim foto + caption
                    url = f"https://api.telegram.org/bot{token}/sendPhoto"
                    with open(foto_path, 'rb') as f:
                        data = aiohttp.FormData()
                        data.add_field('chat_id', chat_id)
                        data.add_field('caption', pesan)
                        data.add_field('photo', f, filename=os.path.basename(foto_path), content_type='image/jpeg')

                        async with session.post(url, data=data) as resp:
                            if resp.status == 200:
                                console.print(Panel(f"[{i+1}] ✓ Foto terkirim (token {token}) | Pesan: {pesan}", width=75, style="green"))
                            else:
                                console.print(Panel(f"[{i+1}] ✗ Gagal kirim foto - Status {resp.status} (token {token})", width=75, style="red"))
                else:
                    # Kirim teks biasa
                    url = f"https://api.telegram.org/bot{token}/sendMessage"
                    async with session.post(url, data={"chat_id": chat_id, "text": pesan}) as resp:
                        if resp.status == 200:
                            console.print(Panel(f"[{i+1}] ✓ Pesan terkirim (token {token}) | Pesan: {pesan}", width=75, style="green"))
                        elif resp.status == 429:
                            console.print(Panel(f"[{i+1}] > Rate Limit (429) (token {token})", width=75, style="red"))
                        else:
                            console.print(Panel(f"[{i+1}] ✗ Gagal - Status {resp.status} (token {token})", width=75, style="yellow"))
                await asyncio.sleep(0.5)
            except Exception as e:
                console.print(Panel(f"[{i+1}] Error: {str(e)}", width=75, style="bold red"))

async def main():
    tasks = [spam(i) for i in range(jumlah)]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    console.print(Panel("[bold cyan]Spam Telegram (Multi Token + Random Pesan + Random Foto)[/bold cyan]", subtitle="By Dra Vin", style="bold blue", width=75, box=box.ROUNDED))
    asyncio.run(main())
