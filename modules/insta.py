import requests
import re
import json
import io
import discord

class Instagram():
    headers = {
        "Cookie": 'mid=ZNeIEgABAAFMV1WbMcmazA31jgWS; ig_nrcb=1; ig_did=AEAE504B-0AFB-42DB-B873-DDB69E6B357D; datr=EojXZL6xkIwLR3S7KsTns3xZ; fbm_124024574287414=base_domain=.instagram.com; csrftoken=sDMbW7JbH5EznlKIEBIVJA9CAFHIlilU; ds_user_id=18388851825; sessionid=18388851825%3AqAK5x79X04NRZ9%3A26%3AAYeVjuG8kUKdS9-R6Lgbun-TXOaOqFDoQLg5DXUcjPQ; shbid="276\05418388851825\0541727628198:01f7825aaefc63d01efa7f4bdd8ff6a86281d85a386bf0e04de148049dff26279931f988"; shbts="1696092198\05418388851825\0541727628198:01f77d4879348a84b9403727311b29d4ee06e0e6be9d5a87397b9ffa0f7e70ee4dc8df6d"; fbsr_124024574287414=o1MDgtURCbdao46AS4AbHCdWvveLO81Rbzbb23L6AgQ.eyJ1c2VyX2lkIjoiMTAwMDExMzQzNDc4ODkwIiwiY29kZSI6IkFRRHBWZkxTaFpNMlEzMU1WcmJXSWJSdy1Ib0djRDJuQ3RPRkFhT3Juc2p2dm1qY1NWQ1M2aEVValJ1djNxVklocGhSTEc1NXhRR1lNY0s5Qm5NOWQ3NlRTLUdFNkNfSlYyRzJYTjFGamNrbVFaTFRsSXBfODVkMkdPN3gwVlBpd09yU1ZMZkY0czVUd2NPWU9oQTNKXzJ6dWlWbnIySGI1ZHR2c2ozeXUyUU9zOTJsUDN1NzhBdWVmRVVxbklSWTF0RTR4aFFFaE5PSmFGTEJCaGhOeHdVV3Vpb1FJZ1BVVkZ1STFyVEJwQkRvV2dpLTZsMl9DazZDcjMtSVlhSWZPX3g1QkxOdm1xckVwVFlWMjRjaFNwaHhrWndEZVJOVks5X3Jia2FUWjRpNjlkMWJvelJheHFMRDFSYXhBcjRWdHU4dC1YRUtMd2xRQk5SSnBqV2R4U3h1Iiwib2F1dGhfdG9rZW4iOiJFQUFCd3pMaXhuallCT3dUOURpTE0yd3NzRWY0U3RHVG5MenhoekRBeDBqQkk4YTNaQkc4SU5ZcTNzSnJlZzJTQ0JvU3VWd0xUbklLdkhQYXk1NEh5azBaQXNhNmVScmk3WkJjWXdSbWJzSEY4WEN4QTRKZkdOYk9vQ042TVZQWXhUbHVGUWRjVTdLWU5ZS0NtWkFoZWI2RVdhRklBbU5QZHdpbnNFU2JYQWR1a0VOcGFvaERIc2lxd0E5dk0xdDZ0NW5NWkQiLCJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImlzc3VlZF9hdCI6MTY5NjA5MjgyMH0; fbsr_124024574287414=o1MDgtURCbdao46AS4AbHCdWvveLO81Rbzbb23L6AgQ.eyJ1c2VyX2lkIjoiMTAwMDExMzQzNDc4ODkwIiwiY29kZSI6IkFRRHBWZkxTaFpNMlEzMU1WcmJXSWJSdy1Ib0djRDJuQ3RPRkFhT3Juc2p2dm1qY1NWQ1M2aEVValJ1djNxVklocGhSTEc1NXhRR1lNY0s5Qm5NOWQ3NlRTLUdFNkNfSlYyRzJYTjFGamNrbVFaTFRsSXBfODVkMkdPN3gwVlBpd09yU1ZMZkY0czVUd2NPWU9oQTNKXzJ6dWlWbnIySGI1ZHR2c2ozeXUyUU9zOTJsUDN1NzhBdWVmRVVxbklSWTF0RTR4aFFFaE5PSmFGTEJCaGhOeHdVV3Vpb1FJZ1BVVkZ1STFyVEJwQkRvV2dpLTZsMl9DazZDcjMtSVlhSWZPX3g1QkxOdm1xckVwVFlWMjRjaFNwaHhrWndEZVJOVks5X3Jia2FUWjRpNjlkMWJvelJheHFMRDFSYXhBcjRWdHU4dC1YRUtMd2xRQk5SSnBqV2R4U3h1Iiwib2F1dGhfdG9rZW4iOiJFQUFCd3pMaXhuallCT3dUOURpTE0yd3NzRWY0U3RHVG5MenhoekRBeDBqQkk4YTNaQkc4SU5ZcTNzSnJlZzJTQ0JvU3VWd0xUbklLdkhQYXk1NEh5azBaQXNhNmVScmk3WkJjWXdSbWJzSEY4WEN4QTRKZkdOYk9vQ042TVZQWXhUbHVGUWRjVTdLWU5ZS0NtWkFoZWI2RVdhRklBbU5QZHdpbnNFU2JYQWR1a0VOcGFvaERIc2lxd0E5dk0xdDZ0NW5NWkQiLCJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImlzc3VlZF9hdCI6MTY5NjA5MjgyMH0; rur="NHA\05418388851825\0541727628859:01f728afea5585a3c4e867bebb8f59ca82a3f6e2a8633accf46d00273582381dc06474ca"',
        "Dpr": "1",
        "Pragma": "no-cache",
        "Referer": "https://www.instagram.com/reel/CxqNmORI-EQ",
        "Sec-Ch-Prefers-Color-Scheme": "dark",
        "Sec-Ch-Ua": '"Chromium";v="118", "Microsoft Edge";v="118", '
        '"Not=A?Brand";v="99"',
        "Sec-Ch-Ua-Full-Version-List": '"Chromium";v="118.0.5993.21", "Microsoft '
        'Edge";v="118.0.2088.17", '
        '"Not=A?Brand";v="99.0.0.0"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Model": '""',
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Ch-Ua-Platform-Version": '"15.0.0"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 "
        "Edg/118.0.2088.17",
        "Viewport-Width": "673",
    }
    params = {
        "query_hash": "b3055c01b4b222b8a47dc12b090e4e64",
        "variables":{
            "shortcode": "",
        }
    }
    @classmethod
    def getCode(cls, url) -> str|None:
        p1 = r"instagram\.com\/p\/([^\/]+)"
        p2 = r"www\.instagram\.com\/reels?\/([A-Za-z0-9_-]+)\/\??"

        r1 = re.search(p1, url)
        r2 = re.search(p2, url)

        return r1.group(1) if r1 else r2.group(1) if r2 else None
    
    @classmethod
    def getUrl(cls, code) -> str:
        graphqlApi = "https://www.instagram.com/graphql/query/"
        cls.params.update({
            "variables": json.dumps({
                "shortcode": code,
            })
        })
        rs = requests.get(
            url = graphqlApi,
            params = cls.params,
            headers = cls.headers
        ).json()
        raw_url = str(rs["data"]["shortcode_media"]["video_url"])

        # idk why i make this and how it works
        try:
            result2 = re.search(r"https:\/\/([A-Za-z0-9_\-\.]+)\/v\/", raw_url)
            target = result2.group(1)
            main_url = raw_url.replace(target, "scontent.cdninstagram.com", 1)
        except:
            main_url = rs["data"]["shortcode_media"]["video_url"]

        return main_url

    @classmethod
    def insta(cls, url) -> discord.File:
        code = cls.getCode(url)
        url = cls.getUrl(code)
        file = [discord.File(io.BytesIO(requests.get(url).content), f"abc.mp4")]

        return file
    
# Instagram.insta("https://www.instagram.com/reel/C1_-du5vOv3/?igsh=MXh3ZWJqa3R6bWFmdw==")
