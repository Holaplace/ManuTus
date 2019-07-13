import asyncio
from pyppeteer import launch
import time
from twilio.rest import Client
from aip import AipOcr
import os

launch_kwargs = {
        "headless": True,
        "args": [
            "--start-maximized",
            "--no-sandbox",
            "--disable-infobars",
            "--log-level=3",
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        ],
        "userDataDir": "/home/userDataDir"
    }


account_sid = 'AC42a0cd6e0266090f4d58340d9ebf6932'
auth_token = '2be41969718c99732244ed18f9c7aa0b'
myNumber = '+8618019156817'
twilioNumber = '+12055263797'


APP_ID = '16786457'
API_KEY = 'zQemGkiK2fRX0R7My4Nebqdu'
SECRET_KEY = 'XPNlEM20YNr3BmXt2yEFgLbhc7zSFing'


async def textmyself(message):
    client = Client(account_sid, auth_token)
    message = client.messages.create(to=myNumber, from_=twilioNumber, body=message)


async def main():
    time.sleep(5)
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

    await page.goto('https://ees.elsevier.com/neucom/default.asp?pg=login.asp')
    time.sleep(5)

    frame1 = page.frames
    b = 5
    await asyncio.sleep(1)
    username = await frame1[b].querySelector('#rightCol > form > div > fieldset > input:nth-child(3)')
    await username.type('xuzhencang@163.com')

    password = await frame1[b].querySelector('#rightCol > form > div > fieldset > input:nth-child(6)')
    await password.type('210071Xzc12145')

    coauther_role = await frame1[b].querySelector(
        '#rightCol > form > div > fieldset > div.buttonAlign > input:nth-child(2)')
    await coauther_role.click()
    time.sleep(5)
    await page.screenshot({'path': '/home/ocr.png'})

    currentTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    i = open(r'/home/ocr.png', 'rb')
    img = i.read()
    message = client.basicAccurate(img)

    totalMessage = ''

    for i in message.get('words_result'):
        totalMessage += i.get('words')

    if 'Submissions Being Processed(1)' in totalMessage:
        content1 = 'With Editor\n'
        content2 = currentTime
        f = open("/home/status.txt", 'a')
        f.write(content2)
        f.write(content1)
        f.close()
        # await textmyself('With Editor.')

    elif 'Submissions with a Decision(1)' in totalMessage:
        content3 = 'Please check status...'
        f = open("/home/status.txt", 'a')
        f.write(content3)
        f.close()
        await textmyself('Manuscript status has changed, please check your Elsevier account ASAP.')

    path = '/home/'

    for root, dirs, files in os.walk(path):
        for name in files:
            if name.endswith(".png"):
                os.remove(os.path.join(root, name))
                # print("Delete File: " + os.path.join(root, name))
        break


asyncio.get_event_loop().run_until_complete(main())
