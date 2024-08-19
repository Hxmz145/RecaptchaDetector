import requests
from bs4 import BeautifulSoup

import cv2
from inferenceModel import split_image

import os
import subprocess


def download_image(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print("Image downloaded")
    else:
        print("Failed to load image")


r = requests.get(
    'https://www.google.com/recaptcha/api/fallback?k=6LdAvUIUAAAAAHjrjmjtNTcXyKm0WKwefLp-dQv9')


# Parse the HTML content
soup = BeautifulSoup(r.content, 'html.parser')

# Finding the Payload
payload_div = soup.find('img', class_='fbc-imageselect-payload')


items = soup.find("div", class_="rc-imageselect-desc-no-canonical")

src = payload_div['src']
item_name = items.find('strong')
print(item_name.text)
new_url = f"https://www.google.com/{src}"
download_image(new_url, f"{item_name.text}.png")


path = f'{item_name.text}.png'
sections = split_image(path)


for n, section in enumerate(sections):
    target_width = 640
    target_height = 640
    resized_image = cv2.resize(section, (target_width, target_height))
    G = cv2.GaussianBlur(resized_image, (5, 5), 0)
    b = cv2.blur(G, (5, 5))
    cv2.imwrite(f"{item_name.text}--{n}.png", b)

length = len(sections)

os.chdir('/Users/hamza1/yolov5')
# For loop for running YoloV5
for i in range(length):
    result = subprocess.run(["python", "detect.py", "--weights", "yolov5s.pt",
                             "--source", f"/Users/hamza1/Desktop/CaptchaSolver/{item_name.text}--{i}.png"], capture_output=True, text=True)
