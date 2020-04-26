import re
import cv2 
import numpy as np
import pytesseract
from pytesseract import Output
from matplotlib import pyplot as plt

IMG_DIR = 'images/'

# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# noise removal
def remove_noise(image):
    return cv2.medianBlur(image,5)
 
#thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

#dilation
def dilate(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.dilate(image, kernel, iterations = 1)
    
#erosion
def erode(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.erode(image, kernel, iterations = 1)

#opening - erosion followed by dilation
def opening(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

#canny edge detection
def canny(image):
    return cv2.Canny(image, 100, 200)

#skew correction
def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

#template matching
def match_template(image, template):
    return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)


def image_to_text(image_name):
    image = cv2.imread(image_name)
    custom_config = r'--oem 3 --psm 6'
    print(pytesseract.image_to_string(image, config=custom_config))
    text = pytesseract.image_to_string(image, config=custom_config)
    json_element = {}
    split_text = text.split('Contact Info')
    print('split')
    print(split_text)
    is_address = False
    print('splitted')
    is_phone = False
    print(split_text[1])
    is_website = False
    is_email = False
    website = []
    others = []
    previous_line = ''
    for line in text.splitlines():
        restr = re.sub(r"[^a-zA-Z0-9./()]+", ' ', line.strip())
        print(restr)
        if(line.__contains__('linkedin.com/in')):
            json_element.update({'profile': line.strip()})
        elif((line.__contains__('Websites')) or is_website):
            web = re.sub(r"[^a-zA-Z0-9]+", ' ', line.strip())
            print('web')
            print(is_website)
            if(web.strip().__eq__('Websites')):
                is_website = True
                continue
            elif(line.__contains__('Phone') or line.__contains__('Address') or line.__contains__('Email') or line.__contains__('Twitter')):
                res = re.sub(r"[^a-zA-Z0-9]+", ' ', line.strip())
                if(res.strip().__eq__('Phone')):
                    is_phone = True
                    is_website = False
                    continue
                elif(res.strip().__eq__('Address')):
                    is_address = True
                    is_website = False
                    continue
                else:
                    is_website = False
            else:
                website.append(line.strip())
        elif((line.__contains__('Phone')) or is_phone):
            pho = re.sub(r"[^a-zA-Z0-9]+", ' ', line.strip())
            print('pho')
            print(is_phone)
            if(pho.strip() == 'Phone'):
                is_phone = True
                print(is_phone)
                continue
            elif(line.__contains__('Address') or line.__contains__('Email') or line.__contains__('Twitter')):
                rep = re.sub(r"[^a-zA-Z0-9]+", ' ', line.strip())
                if(res.strip().__eq__('Websites')):
                    is_website = True
                    continue
                elif(res.strip().__eq__('Address')):
                    is_address = True
                    continue
                else:
                    is_phone = False
            else:
                print('addinng')
                json_element.update({'Phone': line.strip()})
                is_phone = False
        elif((line.__contains__('Address')) or is_address):
            addr = re.sub(r"[^a-zA-Z0-9]+", ' ', line.strip())
            print('addr')
            print(is_address)
            if(addr.strip() == 'Address'):
                is_address = True
                print(is_address)
                continue
            elif(line.__contains__('Email') or line.__contains__('Twitter')):
                is_email = True
                continue
            else:
                json_element.update({'Address': line.strip()})
                previous_line = line.strip()
                is_address = False
        elif(line.__contains__('Email') or is_email):
            ema = re.sub(r"[^a-zA-Z0-9]+", ' ', line.strip())
            print('email')
            print(is_email)
            if(ema.strip().__contains__('Email')):
                is_email = True
                print(is_email)
                continue
            elif( line.__contains__('Twitter')):
                is_email = False
                continue
            else:
                json_element.update({'Email': line.strip()})
                is_email = False
        else:
            print('others')
            others.append(line.strip())
    json_element.update({'Websites': website})
    if(len(others)>0):
        json_element.update({'others': others})
    print(json_element)

