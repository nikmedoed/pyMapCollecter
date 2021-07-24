from selenium import * webdriver 
from time import sleep
from PIL import Image
from io import BytesIO
from tqdm import tqdm

initLink = "https://yandex.ru/maps/213/moscow/?ll=37.620853%2C55.752200&mode=whatshere&whatshere%5Bpoint%5D=37.616644%2C55.750826&whatshere%5Bzoom%5D=15.44&z=15.44"

width = 3000
height = 5000

boundSize = 500
boundSizeHalf = boundSize//2

sidebar = {
    "yandex": "sidebar-toggle-button__icon"
}

def slide (browser, x,y):
    action = webdriver.ActionChains(browser)
    action.move_to_element(mapElement).perform()    
    action.click_and_hold(mapElement).move_by_offset(x,y).perform()
    sleep(1) # change sleepTime for your internet connection
    action.release().perform() 
    sleep(1)          
    
# you should set path to chromedriver https://chromedriver.chromium.org/downloads
browser = webdriver.Chrome()

browser.set_window_size(2000,2000)
browser.get(initLink)

distanceToStartX = width //2 - boundSizeHalf
distanceToStartY = height //2 - boundSizeHalf 

sidebar = next((x[1] for x in sidebar.items() if x[0] in initLink), None)

browser.find_element_by_class_name(sidebar).click()

mapElement = browser.find_element_by_tag_name("body")

selectShift = lambda x: x if x < boundSize else boundSize
while 1:
    toMoveX = selectShift(distanceToStartX)
    toMoveY = selectShift(distanceToStartY)
#     mapElement = browser.find_element_by_tag_name("body")
    slide(browser, toMoveX,toMoveY)
    distanceToStartX -=toMoveX
    distanceToStartY -=toMoveY
    if distanceToStartX == 0 and distanceToStartY==0:
        break
    print(toMoveX, toMoveY, distanceToStartX, distanceToStartY)