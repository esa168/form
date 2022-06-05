import cv2 as cv
import pytesseract as tes

tes.pytesseract.tesseract_cmd = '/Users/mp/opt/anaconda3/envs/heroku/lib/python3.9/site-packages/pytesseract'

#r'C:\Users\USER\AppData\Local\Tesseract-OCR\tesseract.exe'

fn = 'img.png'
img = cv.imread (fn)

height,width,_ = img.shape
roi = img[50:500, 200:600]

print(tes.image_to_string(roi))
cv.imshow ('name', roi)
cv.waitKey(0)
cv.destroyAllWindows()
