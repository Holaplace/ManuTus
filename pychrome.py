import asyncio
from pyppeteer import launch
import time
from twilio.rest import Client
from aip import AipOcr
import os

def screen_size():
    """使用tkinter获取屏幕大小"""
    import tkinter
    tk = tkinter.Tk()
    width = tk.winfo_screenwidth()
    height = tk.winfo_screenheight()
    tk.quit()
    return width, height

launch_kwargs = {
        "headless": False,
        "args": [
            "--start-maximized",
            "--no-sandbox",
            "--disable-infobars",
            "--log-level=3",
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        ],
        "userDataDir": "F:\\manutus\\userDataDir"
    }


account_sid = '**************'
auth_token = '**************'
myNumber = '**************'
twilioNumber = '**************'


APP_ID = '**************'
API_KEY = '**************'
SECRET_KEY = '**************'


async def textmyself(message):
    client = Client(account_sid, auth_token)
    message = client.messages.create(to=myNumber, from_=twilioNumber, body=message)


async def main():
    while True:
        time.sleep(10)
        browser = await launch(launch_kwargs)
        page = await browser.newPage()

        await page.evaluateOnNewDocument("""
                var _navigator = {};
                for (name in window.navigator) {
                    if (name != "webdriver") {
                        _navigator[name] = window.navigator[name]
                    }
                }
                Object.defineProperty(window, 'navigator', {
                    get: ()=> _navigator,
                })
            """)

        width, height = screen_size()
        await page.setViewport({"width": width, "height": height})


        await page.goto('https://ees.elsevier.com/neucom/default.asp?pg=login.asp')
        await page.waitFor('#mainFrameset > frameset:nth-child(1) > frame')

        frame1 = page.frames
        await asyncio.sleep(1)
        username = await frame1[5].querySelector('#rightCol > form > div > fieldset > input:nth-child(3)')
        await username.type('**************')

        password = await frame1[5].querySelector('#rightCol > form > div > fieldset > input:nth-child(6)')
        await password.type('**************')

        coauther_role = await frame1[5].querySelector(
            '#rightCol > form > div > fieldset > div.buttonAlign > input:nth-child(2)')
        await coauther_role.click()

        time.sleep(2)
        # await asyncio.sleep(1)

        await page.goto('https://ees.elsevier.com/neucom/coauthor/coauth_pendSubmissions.asp?currentpage=1')

        currentTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        await page.screenshot({'path': 'F:\manutus\ocr.png'})
        client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

        i = open(r'F:\manutus\ocr.png', 'rb')
        img = i.read()
        message = client.basicAccurate(img)

        totalMessage = ''
        for i in message.get('words_result'):
            totalMessage += i.get('words')

        if 'With' and 'Editor' in totalMessage:
            print(f"With Editor")
            print(currentTime)

        else:
            print(f"Please check status...")
            await textmyself('Manuscript status has changed, please check your Elsevier account ASAP.')
            print(currentTime)
            break

        await asyncio.sleep(1)
        await browser.close()

        path = "F:\\manutus\\"
        for root, dirs, files in os.walk(path):
            for name in files:
                if name.endswith(".png"):
                    os.remove(os.path.join(root, name))
                    print("Delete File: " + os.path.join(root, name))
            break
            
asyncio.get_event_loop().run_until_complete(main())
