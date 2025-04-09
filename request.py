import requests

def getLinks(loginSession, objectID):
    res = []
    formats = ["4KMP4", "HDMP4"]
    url = f"https://www.storyblocks.com/video/download-ajax/{objectID}/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest",
        "Referrer": "https://www.storyblocks.com/",
        "Accept-Language": "en-US,en;q=0.9",
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "ru,en;q=0.9",
        "cookie": f"login_session={loginSession}",
        "priority": "u=1, i",
        "referer": "https://www.storyblocks.com/video/stock/aerial-korea-seoul-april-2017-gangnam-night-hdlkf6b1zj27bfynq",
        "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132", "YaBrowser";v="25.2", "Yowser";v="2.5"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest"}

    for i in formats:
        response = requests.get(url+i, headers=headers)

        if response.status_code == 200:
            responseObj = response.json()['data']
            if 'downloadUrl' in responseObj:
                video_url = responseObj['downloadUrl']
                res.append(video_url)
        else:
            res.append("")
    
    return res