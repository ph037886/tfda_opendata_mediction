import asyncio
from googletrans import Translator

async def translate_text(txt):
    async with Translator() as translator:
        result = await translator.translate(str(txt), dest='zh')
        print(result)
    return result