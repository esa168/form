import streamlit as st
import cv2 as cv
import pytesseract
import numpy as np


# https://medium.com/analytics-vidhya/streamline-your-images-into-text-with-python-and-ocr-6c32c0f79d1e
#https://stackoverflow.com/questions/71532407/what-is-the-best-way-to-get-text-from-image-with-python


picture = st.camera_input("Camera Input", key = 'pic')

if picture:
    st.image(picture)


    pytesseract.pytesseract.terreract_cmd = {
        r'/usr/bin/tesseract'
    }

    #src = cv2.imread(picture)
    #cv2_imshow(src)
    img = cv.imread(picture)

    output_txt = pytesseract.image_to_string(img)
    print(type(output_txt))
    print(output_txt)