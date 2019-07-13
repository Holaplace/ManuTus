import time
import random
import asyncio
from pyppeteer import launch
from twilio.rest import Client


def input_time_random():
    return random.randint(100, 151)


def saveFile(content):
    with open(r"C:\Users\*****\Desktop\RSC.txt", 'a') as f:
        f.write(content)


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
            "--accept-language=zh-CN,zh;q=0.9,und;q=0.8,en;q=0.7"
        ],
        "userDataDir": "F:\\manutus\\rscUserDataDir"
    }


async def stimulateClick(page, selector):
    box = await selector.boundingBox()

    x = box['x'] + (box['width'] / 2)
    y = box['y'] + (box['height'] / 2)

    await page.mouse.click(x, y)
    await page.waitFor(20)
    await page.waitForNavigation({'timeout': 1000*240})
    time.sleep(2)


account_sid = '*****************'
auth_token = '*****************'
myNumber = '*****************'
twilioNumber = '*****************'


async def textmyself(message):
    client = Client(account_sid, auth_token)
    message = client.messages.create(to=myNumber, from_=twilioNumber, body=message)


async def main():
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

    await page.goto('************************')
    await page.waitFor('#logInButton')

    await page.type('#USERID', '*************', {'delay': input_time_random() - 50})
    await page.type('#PASSWORD', '**************', {'delay': input_time_random()})

    clickButton = await page.querySelector("#logInButton")
    await stimulateClick(page, clickButton)

    auther_ui = await page.querySelector('#header > div > div.nav-collapse.toplvlnav > div > ul > li:nth-child(2) > a')
    await stimulateClick(page, auther_ui)

    await page.waitForSelector('#default_form > div.container > div')
    currentTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    try:
        status = await page.querySelector('#queue_0 > td:nth-child(1)')
        true_status = await status.querySelector(
            '#queue_0 > td:nth-child(1) > table > tbody > tr > td:nth-child(2) > span')
        title_str = await (await true_status.getProperty('textContent')).jsonValue()
        saveFile(title_str + ' ' + currentTime + '\n')

        print(title_str)
        print(currentTime)

    except AttributeError:
        status = await page.querySelector('#queue_0 > td:nth-child(2)')
        true_status = await status.querySelector(
            '#queue_0 > td:nth-child(2) > table > tbody > tr > td:nth-child(2) > span')
        title_str = await (await true_status.getProperty('textContent')).jsonValue()
        print(title_str)
        print(currentTime)
        await textmyself(title_str)

    await asyncio.sleep(1)
    await browser.close()


asyncio.get_event_loop().run_until_complete(main())
