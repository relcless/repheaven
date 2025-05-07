import discord
from discord.ext import commands
import aiohttp
from urllib.parse import quote
from bs4 import BeautifulSoup

intents = discord.Intents.default()
intents.message_content = True

CLARIFAI_API_KEY = "165782598e1b411abaee78cf150fafac"  # Wklej swój API key

class AcbuyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def detect_labels_from_image(self, image_url):
        """Wykryj etykiety na obrazie za pomocą Clarifai API."""
        api_url = "https://api.clarifai.com/v2/models/general-image-recognition/outputs"
        headers = {
            "Authorization": f"Key {CLARIFAI_API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "inputs": [
                {
                    "data": {
                        "image": {
                            "url": image_url
                        }
                    }
                }
            ]
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(api_url, headers=headers, json=data) as response:
                if response.status != 200:
                    text = await response.text()
                    raise Exception(f"Błąd API Clarifai: {response.status}, {text}")

                result = await response.json()
                concepts = result["outputs"][0]["data"].get("concepts", [])
                return [c["name"] for c in concepts[:5]]  # Zwraca do 5 etykiet

    async def search_product_on_cnfan(self, labels):
        """Wyszukaj produkt na Cnfans na podstawie wykrytych etykiet."""
        search_query = " ".join(labels[:3])  # Używamy pierwszych 3 etykiet
        search_url = f"https://www.cnfans.com/search?q={quote(search_query)}"
        
        return await self.search_on_page(search_url)

    async def search_product_on_kakoobuy(self, labels):
        """Wyszukaj produkt na Kakoobuy na podstawie wykrytych etykiet."""
        search_query = " ".join(labels[:3])  # Używamy pierwszych 3 etykiet
        search_url = f"https://www.kakoobuy.com/search?q={quote(search_query)}"
        
        return await self.search_on_page(search_url)

    async def search_product_on_acbuy(self, labels):
        """Wyszukaj produkt na Acbuy na podstawie wykrytych etykiet."""
        search_query = " ".join(labels[:3])  # Używamy pierwszych 3 etykiet
        search_url = f"https://www.acbuy.com/search/?q={quote(search_query)}"

        return await self.search_on_page(search_url)

    async def search_on_page(self, search_url):
        """Wyszukaj na danej stronie i zwróć wynik."""
        headers = {'User-Agent': 'Mozilla/5.0'}
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(search_url, headers=headers, timeout=10) as res:
                    if res.status == 200:
                        soup = BeautifulSoup(await res.text(), 'html.parser')
                        product_link = soup.find('a', class_='product-link')  # Dopasuj selektor, jeśli potrzeba
                        if product_link and 'href' in product_link.attrs:
                            return f"{product_link['href']}"
        except Exception as e:
            print(f"[BŁĄD] Nie udało się wyszukać na stronie: {e}")
        return None

    async def find_image_on_product_page(self, product_url):
        """Find the product image from the given product page."""
        headers = {'User-Agent': 'Mozilla/5.0'}
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(product_url, headers=headers) as res:
                    if res.status == 200:
                        soup = BeautifulSoup(await res.text(), 'html.parser')
                        product_image = soup.find('img', class_='product-image')  # Zmienna klasa, może się zmieniać
                        if product_image and 'src' in product_image.attrs:
                            return product_image['src']
        except Exception as e:
            print(f"[BŁĄD] Nie udało się znaleźć obrazu na stronie produktu: {e}")
        return None

    @commands.command()
    async def acbuy(self, ctx, image_url: str):
        """Szukaj produktu na różnych stronach na podstawie obrazu (linku do obrazu)."""
        await ctx.send("🔍 Wyszukiwanie produktu na stronach Cnfans, Kakoobuy, i Acbuy...")

        try:
            labels = await self.detect_labels_from_image(image_url)
            if not labels:
                return await ctx.send("❌ Nie udało się wykryć żadnych etykiet na podstawie obrazu.")

            # Wyszukiwanie na różnych stronach
            acbuy_link = await self.search_product_on_acbuy(labels)
            cnfan_link = await self.search_product_on_cnfan(labels)
            kakoobuy_link = await self.search_product_on_kakoobuy(labels)

            if acbuy_link:
                await self.handle_product_link(ctx, acbuy_link)
            elif cnfan_link:
                await self.handle_product_link(ctx, cnfan_link)
            elif kakoobuy_link:
                await self.handle_product_link(ctx, kakoobuy_link)
            else:
                await ctx.send("❌ Nie udało się znaleźć pasującego produktu na żadnej z stron.")

        except Exception as e:
            await ctx.send(f"❌ Wystąpił błąd podczas przetwarzania obrazu: {e}")

    async def handle_product_link(self, ctx, product_link):
        """Obsługuje znaleziony link produktu i wysyła informacje do bota."""
        product_image_url = await self.find_image_on_product_page(product_link)
        if product_image_url:
            await ctx.send(f"✅ Znaleziono produkt: {product_link}")
            await ctx.send(f"Obraz produktu: {product_image_url}")
        else:
            await ctx.send(f"✅ Znaleziono produkt: {product_link}, ale nie udało się znaleźć obrazu produktu.")

# Dodaj coga do bota
async def setup(bot):
    await bot.add_cog(AcbuyCog(bot))
