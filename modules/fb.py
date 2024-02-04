import urllib.parse
import discord
import io
import requests
import re
import json
from threading import Thread

class Facebook:
    # Get cookies from connfig.json
    cookies = json.loads(open('config.json', 'r+', encoding='utf-8').read())["fbCookies"]
    session_ : requests.Session = requests.Session()
    baseHeaders : dict = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br', 
        'Accept-Language': 'en-US,en;q=0.9', 
        'Cache-Control': 'no-cache', 
        'Cookie': cookies, 
        'Dpr': '1', 
        'Pragma': 'no-cache', 
        'Sec-Ch-Prefers-Color-Scheme': 'dark', 
        'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Microsoft Edge";v="120"', 
        'Sec-Ch-Ua-Full-Version-List': '"Not_A Brand";v="8.0.0.0", "Chromium";v="120.0.6099.35", "Microsoft Edge";v="120.0.2210.39"', 
        'Sec-Ch-Ua-Mobile': '?0', 
        'Sec-Ch-Ua-Model': '""', 
        'Sec-Ch-Ua-Platform': '"Windows"', 
        'Sec-Ch-Ua-Platform-Version': '"15.0.0"', 
        'Sec-Fetch-Dest': 'document', 
        'Sec-Fetch-Mode': 'navigate', 
        'Sec-Fetch-Site': 'none', 
        'Sec-Fetch-User': '?1', 
        'Upgrade-Insecure-Requests': '1', 
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0', 
        'Viewport-Width': '628'
    }

    def returnUrl(cls, url):
        session = cls.session_
        result = session.get(
            url, headers=cls.baseHeaders
        ).url
        return result
            
    def parseVidUrl(html):
        # Find HD/SD content direct url using regex (stored in page html)
        # Skip if either HD/SD url is "null"
        urlHD = ""
        urlSD = ""
        urlPattern = r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&\/\/=]*)'

        HD = [json.loads('"' + item[0].replace("\\/","/") + '"') for item in re.findall(r'"browser_native_hd_url":"?(([^\\"]|\\.)*)|null"', html)]
        SD = [json.loads('"' + item[0].replace("\\/","/") + '"') for item in re.findall(r'"browser_native_sd_url":"?(([^\\"]|\\.)*)|null"', html)]

        for item in HD:
            if "null" in item:
                urlHD = ""
                break
            else:
                _ = re.search(urlPattern, item)
                if _ :
                    urlHD = _.group(0)
                    break

        for item in SD:
            if "null" in item:
                urlSD = ""
                break
            else:
                _ = re.search(urlPattern, item)
                if _ :
                    urlSD = _.group(0)
                    break

        for i in [urlHD, urlSD]:
            if i != "":
                return i
        
    @classmethod
    def parseAttachments(cls, html):
        attList = []
        a=[]
        z=[]
        url = ""
        attL_ = ""
        urlPattern = r'^https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&\/\/=]*)'

        idPost = re.search(r'"post_id":"(\d+)"', html)

        att1 = re.search(r'\\"photo_attachments_list\\":\[([^\]]+)', html)
        att2 = re.search(r'\\"photo_attachments_list\\":\\([^\]^,]+)', html)
        att3 = re.search(r'"photo_image":{"uri":"([^\"]+)', html)

        vid1 = re.search(r'\\"video_id\\":\[([^\]]+)', html)
        vid2 = re.search(r'\\"video_id\\":\\([^\]^,]+)', html)
        vid3 = re.search(r'"video_id":"(\d+)"', html)
        
        for i in [att1, att2]:
            if i:
                a = i.group(1)
                attL_ += a
        
        # if att3 found, and not any att1 or att2 found
        if att3 and not any([att1, att2]):
            attL_ += att3.group(1).replace("\\/","/")
        
        if not any([vid1, vid2]):
            attList.append(cls.parseVidUrl(html))
            z = re.findall(r'(\d+)', vid3.group(1))
        else:
            for i in [vid1, vid2]:
                if i:
                    attList.append(cls.parseVidUrl(html))
                    z = re.findall(r'(\d+)', i.group(1))

        b = [elem for elem in re.findall(r'(\d+)', attL_) if elem not in z]
        
        # only 1 attachment?
        if re.search(urlPattern, attL_):
            attList.append(attL_)
            pass
        else:
            threads = [None] * len(b)
            results = [None] * len(b)
            for j, i in enumerate(b):
                if i is None:
                    continue
                if re.search(urlPattern, i):
                    attList.append(i)
                else:
                    url = f'https://www.facebook.com/photo/?fbid={i}&set=pcb.{idPost.group(1)}'
                    threads[j] = Thread(target=cls.work, args=(url, results, j))
                    threads[j].start()
                    
            for i in range(len(b)):
                threads[i].join()

            attList += results
        return attList
    
    @classmethod
    def work(cls, url, result, index):
        # This function created for threading
        content =cls.session_.get(url = url, headers = cls.baseHeaders)
        url_ = json.loads('"' + re.search(r'"image":{"uri":"(([^\\"]|\\.)*)"', content.text).group(1).replace("\\/","/") + '"')
        result[index] = url_

    @classmethod
    def work2(cls, url, extension, result, index):
        # This function created for threading
        # Get content from url, convert to binary stream (will be kept in memory buffer) then convert to discord file.
        file=discord.File(io.BytesIO(requests.get(url).content), f"abc{extension}")
        result[index] = file

    @classmethod
    def getDirectUrl(cls, url):

        if re.search(r"m\.facebook.+", url):
            url = url.replace("m.facebook", "www.facebook")
        
        url_ = requests.get(url = url, headers = cls.baseHeaders).url

        if "login" in url_:
            url_ = urllib.parse.unquote(re.search(r'next=(.+)', url_).group(1))
            url = url_
            if "login" in url:
                url = None
        else:
            url = url_

        return url if url else None

    @classmethod
    def cleanMSG(cls, msg : str):
        # lol
        replacements = {
            "*": r"\*",
            "_": r"\_",
            "**": r"\*\*",
            "~~": r"\~\~",
            "||": r"\|\|"
        }
        for key, value in replacements.items():
            msg = msg.replace(key, value)
        return msg

    @classmethod
    def facebook(cls, url):
        
        session = cls.session_
        result = session.get(
            cls.getDirectUrl(url), headers = cls.baseHeaders
        )
        # get html
        attList = cls.parseAttachments(result.text)
        hasMsg = re.search(r'"message":{"text":"(([^\\"]|\\.)*)"', result.text)
        msg = json.loads('"' + hasMsg.group(1) + '"') if hasMsg and hasMsg.group(1) != "Explore more in Video" else ""
        msg = cls.cleanMSG(msg)

        # Discord message length limit = 2000
        msg = msg[:1800] + f"... [View more]({url})" if len(msg) > 1950 else msg

        attList = [item for item in attList if item is not None]
        threads = [None] * len(attList)
        files = [None] * len(attList)
        for i, item in enumerate(attList):
            if item is None:
                continue
            extension = re.search(r'(.+)(\.png|\.webp|\.jpg|\.gif)', item)
            extension_vid = re.search(r'(.+)(\.mp4|\.mov)', item)
            if extension:
                threads[i] = Thread(target=cls.work2, args=(item, extension.group(2), files, i))
                threads[i].start()

            if extension_vid:
                threads[i] = Thread(target=cls.work2, args=(item, extension_vid.group(2), files, i))
                threads[i].start()

        for i in range(len(threads)):
            threads[i].join()
        
        #files: list of Discord file
        #msg: text in post, return "" if message is none
        # print(files, msg)
        return files, msg
    
    
# Facebook.facebook("https://www.facebook.com/share/p/aRr2nU3RmgDTzR37/?mibextid=WC7FNe")
