import random

class Url:
    def __init__(self, db):
        self.db = db
        self.input_data = "qwertyuiopasdfghjklzxcvbnm1234567890" * 4

    def generate(self, length):
        return ''.join(random.sample(self.input_data, k=length))

    async def generateUrl(self):
        url = "{}-{}-{}-{}-{}".format(
            self.generate(8),
            self.generate(4),
            self.generate(4),
            self.generate(4),
            self.generate(8)
        )
        if await self.db.if_url_exists(url):
            return await self.generateUrl()
        return url
