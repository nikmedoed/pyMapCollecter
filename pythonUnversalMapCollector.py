from selenium import webdriver
from time import sleep
from PIL import Image
from io import BytesIO
from tqdm import tqdm
from selenium.webdriver.chrome.options import Options

INIT_LINK = "https://yandex.ru/maps/213/moscow/?ll=37.624027%2C55.753747&z=15.68"

SCREENSHOOT_WIDTH = 30000
SCREENSHOOT_HEIGHT = 45000

SCREENSHOOT_self_boundSize = 500  # Different services have different safe zones

SIDEBAR = {
    "yandex": ["sidebar-toggle-button__icon"]
}

SIDEBAR = next((x[1] for x in SIDEBAR.items() if x[0] in INIT_LINK), None)


class MapCollector:
    def __init__(self, initLink, width, height, boundSize=500, pointIsCenter=True, sidebar=[]):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.browser = webdriver.Chrome(options=chrome_options)
        self.browser.set_window_size(2000, 2000)
        self.browser.get(initLink)
        self.width = width
        self.height = height
        self.boundSize = boundSize
        self.boundSizeHalf = boundSize // 2
        self.body = self.getbody()
        for i in sidebar:
            try:
                self.browser.find_element_by_class_name(i).click()
            except:
                pass
        if pointIsCenter:
            self.goToStartPoint()
        else:
            self.slideToOffset(self.boundSizeHalf, self.boundSizeHalf)

    def __del__(self):
        self.browser.close()

    def goToStartPoint(self):
        size = self.browser.get_window_size()
        toMoveX, toMoveY = [int(size[x] * 0.9 // 2) for x in ['width', 'height']]
        distanceToStartX = self.width // 2 - self.boundSizeHalf
        distanceToStartY = self.height // 2 - self.boundSizeHalf

        pbar = tqdm(desc="MoveToStart", total=distanceToStartX + distanceToStartY)
        while 1:
            toMoveX = min(distanceToStartX, toMoveX)
            toMoveY = min(distanceToStartY, toMoveY)
            self.slideToOffset(toMoveX, toMoveY)
            distanceToStartX -= toMoveX
            distanceToStartY -= toMoveY
            pbar.update(toMoveX + toMoveY)
            if distanceToStartX == 0 and distanceToStartY == 0:
                break
        print("At the start position")

    def slideToOffset(self, x, y):
        webdriver.ActionChains(self.browser).click_and_hold(self.getbody()).move_by_offset(x, y).release().perform()
        sleep(0.5)
        return self

    def getbody(self):
        return self.browser.find_element_by_tag_name("body")

    def smallScreenShoot(self, img):
        return img.crop([x // 2 + s for s in [-self.boundSizeHalf, self.boundSizeHalf] for x in img.size])

    def finalShoot(self):
        width = self.width
        height = self.height
        boundSize = self.boundSize
        smallScreenShoot = self.smallScreenShoot
        browser = self.browser

        finalScreenShoot = Image.new('RGB', (width, height))
        sign = 1
        reverse = width - width % boundSize - boundSize
        pbar = tqdm(desc="CollectingMap", total=((height // boundSize + (1 if height % boundSize > 0 else 0)) * (
                width // boundSize + (1 if width % boundSize > 0 else 0))))
        widminusbs = width - boundSize
        for y in range(0, height, boundSize):
            for x in range(0, width, boundSize):
                png = browser.get_screenshot_as_png()
                im = Image.open(BytesIO(png))
                finalScreenShoot.paste(smallScreenShoot(im), (x if sign > 0 else reverse - x, y))
                if widminusbs - x > 0:
                    self.slideToOffset(-boundSize * sign, 0)
                pbar.update(1)
            sign *= -1
            self.slideToOffset(0, -boundSize)
        return finalScreenShoot


collector = MapCollector(INIT_LINK, SCREENSHOOT_WIDTH, SCREENSHOOT_HEIGHT, SCREENSHOOT_self_boundSize,
                         pointIsCenter=True, sidebar=SIDEBAR)
shoot = collector.finalShoot()
shoot.save("resultmap.png")
# shoot.show()
