from PIL import Image
import pytesseract
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
print(pytesseract.image_to_string(Image.open(sys.argv[1])))