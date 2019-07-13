import asyncio
from pyppeteer import launch
import time
from twilio.rest import Client
from aip import AipOcr
import os
import random


def input_time_random():
    return random.randint(100, 151)


def saveFile(content):
    with open("/home/status.txt", 'a') as f:
        f.write(content)

launch_kwargs = {
        "headless": True,
        "args": [
            "--start-maximized",
            "--no-sandbox",
            "--disable-infobars",
            "--log-level=3",
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
            "--accept-language=zh-CN,zh;q=0.9,und;q=0.8,en;q=0.7"
        ],
        "userDataDir": "/home/userDataDir"
    }


async def stimulateClick(page, selector):
    box = await selector.boundingBox()

    x = box['x'] + (box['width'] / 2)
    y = box['y'] + (box['height'] / 2)

    await page.mouse.click(x, y)
    await page.waitFor(20)
    await page.waitForNavigation({'timeout': 1000*240})
    time.sleep(2)

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

    await page.goto('https://ees.elsevier.com/neucom/default.asp?pg=login.asp', {'timeout': 1000*240})
    time.sleep(5)

    frame1 = page.frames
    b = 5
    await asyncio.sleep(1)
    username = await frame1[b].querySelector('#rightCol > form > div > fieldset > input:nth-child(3)')
    await username.type('xuzhencang@163.com', {'delay': input_time_random() - 50})

    password = await frame1[b].querySelector('#rightCol > form > div > fieldset > input:nth-child(6)')
    await password.type('210071Xzc12145', {'delay': input_time_random()})

    coauther_role = await frame1[b].querySelector(
        '#rightCol > form > div > fieldset > div.buttonAlign > input:nth-child(2)')

    await stimulateClick(page, coauther_role)

    # await coauther_role.click()
    # time.sleep(5)
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
        saveFile('With Editor' + ' ' + currentTime + '\n')

    elif 'Submissions with a Decision(1)' in totalMessage:
        saveFile('Please check status...' + ' ' + currentTime + '\n')
        await textmyself('Manuscript status has changed, please check your Elsevier account ASAP.')

    path = '/home/'

    for root, dirs, files in os.walk(path):
        for name in files:
            if name.endswith(".png"):
                os.remove(os.path.join(root, name))
                # print("Delete File: " + os.path.join(root, name))
        break


asyncio.get_event_loop().run_until_complete(main())
