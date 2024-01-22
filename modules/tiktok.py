import requests
import aiohttp
import re
import io
import discord

class Tiktok:
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "identity;q=1, *;q=0",
        "Accept-Language": "en-US,en;q=0.9",
        "Dnt": "1",
        "Origin": "https://www.tiktok.com",
        "Range": "bytes=0-",
        "Referer": "https://www.tiktok.com/",
        "Sec-Ch-Ua": '"Chromium";v="117", "Not;A=Brand";v="8"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "video",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    }

    @classmethod
    def isDirectUrl(cls, url):
        pattern = r'([^\/]+)\/video\/(\d+)'
        return re.search(pattern=pattern, string=url) is not None

    @classmethod
    def getDirectUrl(cls, url):
        if not cls.isDirectUrl(url):
            url_ = requests.get(
                url=url,
                headers=cls.headers
            ).url
        else:
            url_ = url.replace("vt.", "").strip()
        return url_

    @classmethod
    def updateCookies(cls, res):
        cookies = res.cookies.get_dict()
        cls.headers.update({
            "Cookie": f"ttwid={cookies['ttwid']};tt_csrf_token={cookies['tt_csrf_token']};tt_chain_token={cookies['tt_chain_token']}",
        })
        return cookies

    @classmethod
    def parseUrl(cls, raw_url):
        return raw_url.replace("\\u002F", "/")

    @classmethod
    def getDirectMedia(cls, html):
        media_pattern = r'"playAddr":"([^"]+)'
        url = re.search(pattern=media_pattern, string=html).group(1)
        return cls.parseUrl(url)

    @classmethod
    def get_content_media(cls, url):
        return io.BytesIO(requests.get(url, headers=cls.headers).content)

    @classmethod
    def tiktok(cls, url):
        url_ = cls.getDirectUrl(url)
        res = requests.get(
            url=url_,
            headers=cls.headers
        )
        cls.updateCookies(res)
        media_url = cls.getDirectMedia(res.text)
        content = cls.get_content_media(media_url)

        file = discord.File(content, f"abc.mp4")
        return file
