#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ==== Java imports ====

from com.zolbit import Walker
import java.lang.RuntimeException
import org.sikuli.script.FindFailed

# ==== Python imports ====

import datetime
import time
import os
import traceback
import calendar
import sys
import types
import zipfile
from zipfile import ZipFile


# ==== Anti-captcha Python imports ====
ABSOLUTE_PATH_MODULES = "/usr/lib/python2.7/dist-packages"
sys.path.append(ABSOLUTE_PATH_MODULES) # agregar ABSOLUTE_PATH para poder importar modulos
from python_anticaptcha import AnticaptchaClient, NoCaptchaTaskProxylessTask

# ==== Program exceptions ====

class ImageNotFoundException(Exception):
    pass
class ImageNotPresentException(Exception):
    pass
class CantConnectException(Exception):
    pass
class TooFewArgumentsException(Exception):
    pass
class AbortedException(Exception):
    pass
class ManualFinishException(Exception):
    pass

# ==== Private constants ====

_VERSION = "1.0.6"
_DOWNLOAD_TRACKER = False
_EXPLORER_OPENED = False

# ==== Java Walker instance setup ====

_walker = Walker()
_walker.init_screen()

# ==== Program Constants setup ====

SECONDS = 1000
MINUTES = 60 * SECONDS
HOURS = 60 * MINUTES
UP = _walker.UP
DOWN = _walker.DOWN
LEFT = _walker.LEFT
RIGHT = _walker.RIGHT
TAB = _walker.TAB
ENTER = _walker.ENTER
PAGE_DOWN = _walker.PAGE_DOWN
PAGE_UP = _walker.PAGE_UP
ESC = _walker.ESC
DELETE = _walker.DELETE
CTRL = _walker.CTRL
SHIFT = _walker.SHIFT
ALT = _walker.ALT
SPACE = _walker.SPACE
MOUSE_LEFT = _walker.MOUSE_LEFT
MOUSE_MIDDLE = _walker.MOUSE_MIDDLE
MOUSE_RIGHT = _walker.MOUSE_RIGHT

# ==== Configuration file setup ====

exec(open(ABSOLUTE_PATH + "program_config.py").read())
if 'WEBDRIVER_DIRECTORY' in locals():
    _walker.set_webdriver_directory(WEBDRIVER_DIRECTORY)
if 'STARTUP_FILE' not in locals():
    raise Exception("No se ha provisto un archivo de startup.")

# ==== Image based decorator exception handler ====

def image_based_function(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except java.lang.RuntimeException:
            raise ImageNotFoundException(args[0])
        except org.sikuli.script.FindFailed:
            raise ImageNotPresentException(args[0])
    return inner

# ==== Logging functions ====

def log(code, message):
    message = "[{}][{}]{} ".format(datetime.datetime.now().strftime("%H:%M:%S"), code, message)
    _walker.log(code, message)

# === HELPER FUNCTIONS ===

_keystring = {
    UP : "UP",
    DOWN : "DOWN",
    LEFT : "LEFT",
    RIGHT : "RIGHT",
    TAB : "TAB",
    ENTER : "ENTER",
    PAGE_DOWN : "PAGE_DOWN",
    PAGE_UP : "PAGE_UP",
    ESC : "ESC",
    DELETE : "DELETE",
    CTRL : "CTRL",
    SHIFT : "SHIFT",
    ALT : "ALT",
    SPACE : "SPACE",
    MOUSE_LEFT : "MOUSE_LEFT",
    MOUSE_MIDDLE : "MOUSE_MIDDLE",
    MOUSE_RIGHT : "MOUSE_RIGHT",
}

# === SETUP FUNCTIONS ===

def set_min_similarity(value):
    _walker.set_min_similarity(value)

def set_imagepath(directory):
    _walker.set_imagepath(directory)

def set_download_directory(directory):
    _walker.set_download_directory(directory)

def set_screenshot_directory(directory):
    _walker.set_screenshot_directory(directory)

def enable_flash(enable):
    _walker.enable_flash(enable)

def use_firefox(enable):
    _walker.use_firefox(enable)

# === EXPLORER FUNCTIONS ===

def open_explorer(url):
    log("INFO", "open_explorer " + url)
    global _EXPLORER_OPENED
    _EXPLORER_OPENED = True
    _walker.launch_explorer(url)

def new_tab():
    if not _EXPLORER_OPENED:
        raise Exception("El explorador no está abierto.")
    key_hold(CTRL)
    press("T")
    key_release(CTRL)

def close_tab():
    if not _EXPLORER_OPENED:
        raise Exception("El explorador no está abierto.")
    key_hold(CTRL)
    press("W")
    key_release(CTRL)

def close_explorer():
    log("INFO", "close_explorer")
    global _EXPLORER_OPENED
    _EXPLORER_OPENED = False
    _walker.close_explorer()

# === KEYBOARD FUNCTIONS ===

def _log_key(templatestr, key):
    if key in _keystring:
        log("INFO", templatestr % _keystring[key])
    else:
        log("WARNING", "cant log key (unregistered in keystring)")

def press(key):
    _walker.press(key)
    _log_key("pressed %s", key)

def type(text):
    _walker.type(text)
    log("INFO", "typed {}".format(text.encode('utf-8')))

def key_hold(key):
    _walker.key_down(key)
    _log_key("key hold %s", key)

def key_release(key):
    _walker.key_up(key)
    _log_key("key released %s", key)

# -keyboard shortcuts-

def press_with_ctr(key):
    key_hold(CTRL)
    press(key)
    key_release(CTRL)

def copy():
    press_with_ctr("c")

def paste():
    press_with_ctr("v")

# === TCP FUNCTIONS ===

def tcp_connect(host):
    log("INFO", "tcp_connect " + host)
    try:
        log("INFO", "Conectando " + host + "...")
        _walker.tcp_connect(host)
        log("INFO", "Conectado con " + host)
    except Exception as e:
        CANT_CONNECT_MESSAGE = "Imposible conectar con " + host
        log("ERROR", CANT_CONNECT_MESSAGE + "\n" + e)
        raise CantConnectException(CANT_CONNECT_MESSAGE)

def tcp_send(message):
    log("INFO", "tcp_send " + message)
    _walker.tcp_send(message)

def tcp_close():
    log("INFO", "tcp_close ")
    _walker.tcp_close()

def tcp_send_recieve(message):
    log("INFO", "tcp_send " + message)
    returned_message = _walker.tcp_send_recieve(message)
    log("INFO", "In Python, the returned string is: " + returned_message)
    return returned_message
    
# === SCREENSHOT FUNCTIONS ===

def screenshot_save(filename):
    #Toma una captura de pantalla completa
    log("INFO", "screenshot_save " + filename)
    _walker.screenshot_save(filename)

def screenshot_save_crop(filename, x, y, w, h):
    #Take a screenshot using a top-left coordinate (x, y) and a rectangle size (w, h)
    log("INFO", "screenshot_save_crop " + filename +" "+ str(x) +" "+ str(y) +" "+ str(w) +" "+ str(h))
    _walker.screenshot_save_crop(filename, x, y, w, h)

def screenshot_save_crop_with_points(filename, x1, y1, x2, y2):
    #Take a screenshot using a top-left point and a bottom-right point (x1, y1), (x2, y2)
    screenshot_save_crop(filename, x1, y1, x2 - x1, y2 - y1)

def pass_text(id):
    #Changes password box attribute to text to make it visible. Requires id of text box.
    _walker.pass_text(id)

# ==== CAPTCHAS  ===
def captcha_sb():
        #resuelve el captcha para los portales SB(Preunic,Salcobrand)
        log("INFO", "Resolviendo captcha SB")
        _walker.captcha_sb()

def captcha_google(SITE_KEY):
        #Resuelve recaptcha google
        url = _walker.get_url()
        log("INFO", "Resolviendo recaptcha google")
        ANTICAPTCHA_KEY = "b73dc4d2e885dd3f834fc1c766d97a7b"
        recaptcha_xpath = '//*[@id="g-recaptcha-response"]'
        client = AnticaptchaClient(ANTICAPTCHA_KEY)
        task = NoCaptchaTaskProxylessTask(website_url=url, website_key=SITE_KEY)
        job = client.createTask(task)
        job.join()
        log("INFO", "Respuesta desde anti-captcha: " + job.get_solution_response())
        _walker.recaptchaGoogle(job.get_solution_response(),recaptcha_xpath)

# ==== DATA RETRIEVAL ====

def get_download_directory():
    return _walker.DEFAULT_DOWNLOAD_DIRECTORY

def get_screenshot_directory():
    return _walker.SCREENSHOT_DIRECTORY

def get_files_count(dir):
    #Returns the number of files in the directory dir
    return len(os.listdir(dir))

def get_downloads_count():
    #Returns the number of files currently in the downloads directory
    result = get_files_count(get_download_directory())
    log("INFO", "get_downloads count = " + str(result))
    return result

def get_screenshots_count():
    #Return the number of files in screenshot directory
    result = get_files_count(get_screenshot_directory())
    log("INFO", "get_screenshots count = " + str(result))
    return result

def get_clipboard():
    return _walker.get_clipboard()

def get_parameters():
    return _walker.get_parameters()

# ==== PYTHON CODE PREPROCESSING ====

def _preprocess(code):
    funcs = {
    "load_template(": "exec open_read(", 
    "repeat(": "for repeat_index in range(",
    }
    for key, value in funcs.items():
        code = code.replace(key, value)
    return code

# ==== DYNAMIC EXECUTION FUNCTIONS ====

def execute(filename):
    exec(open(filename).read())

# ==== DATE AND TIME MANIPULATION ====

def today():
    return datetime.datetime.today()

def get_weekday_as_int():
    #Returns the current weekday as integer, starting from monday as 0 to sunday as 6
    return datetime.datetime.today().weekday() 

def get_first_day_of_month(date):
    #Returns the date corresponding to the first day of the month of the given date.
    return date.replace(day=1)

def subtract_days(date, days):
    #Retorna la fecha con days dias atras.
    return date - datetime.timedelta(days)

def previous_day(date):
    #Returns the date corresponding to the previous day of the given date.
    return date - datetime.timedelta(1)

def date_to_string(date, template="%d-%m-%Y"):
    #Returns the date as string using the given template.
    return date.strftime(template)

def string_to_date(date, template="%d-%m-%Y"):
    #Returns the date as string using the given template.
    return date.strptime(template)

def get_previous_month(d):
    #Retorna la fecha correspondiente al mes anterior. Se pierde la informacion del dia.
    newd = d.replace(
        year=d.year if d.month > 1 else d.year - 1,
        month=d.month - 1 if d.month > 1 else 12,
        day=1
        )
    return newd

def get_last_day_of_month(d):
    return calendar.monthrange(d.year, d.month)[1]

# ==== DATA TYPE EXTENSIONS ====

def string_keep_digits(s):
    return ''.join(i for i in s if i.isdigit())

# ==== SHORTCUT FUNCTIONS ====

def open_read(filename):
    return open(filename).read()

def run_script(filename):
    exec(_preprocess(open(filename).read()))

def createBoundMethod(func, obj):
    return types.MethodType(func, obj, obj.__class__)

# ==== DATA RETRIEVAL ====
tcp_connect(OPTION_ARGS[1].encode("utf-8"))
OPTION_FILENAME = OPTION_ARGS[0]
OPTION_ARGS = get_parameters()

# ==== PARAMETER SET ====
for x in range (len(OPTION_ARGS)):
    if x == 0:
        print("Parameter {} --> {}".format(x,OPTION_ARGS[x][2:]))
    else:
        print("Parameter {} --> {}".format(x,OPTION_ARGS[x].encode('utf-8')))
RUT_EMPRESA = OPTION_ARGS[0][2:]
USERNAME = OPTION_ARGS[1]
PASSWORD = OPTION_ARGS[2]
NOMBRE_EMPRESA = OPTION_ARGS[3]
URL_PORTAL = OPTION_ARGS[4]
OPTION_LOG_ID = OPTION_ARGS[5]
OPTION_RETRIES = int(OPTION_ARGS[6])
TIMEOUT = OPTION_ARGS[7]
NUM_LOCALES = OPTION_ARGS[8]
AVANZAR = OPTION_ARGS[9]
OPTION_TRACE_EVERY  = OPTION_ARGS[10]
EXTRA = OPTION_ARGS[11]
NUM_SSHOTS = OPTION_ARGS[12]
##### Zolbit conversion required parameters #####
FILE_TYPE = OPTION_ARGS[13]
SALES_FILE_FORMAT = OPTION_ARGS[14]
SALES_ORDER = OPTION_ARGS[15]
SALES_DELIMITATOR = OPTION_ARGS[16]
SALES_HEADER = OPTION_ARGS[17]
SALES_DATE_FORMAT = OPTION_ARGS[18]
SALES_UNITS_CONVERSION = OPTION_ARGS[19]
SALES_UNITS_DECIMAL = OPTION_ARGS[20]
SALES_AMOUNT_CONVERSION = OPTION_ARGS[21]
SALES_AMOUNT_DECIMAL = OPTION_ARGS[22]
STOCK_FILE_FORMAT = OPTION_ARGS[23]
STOCK_ORDER = OPTION_ARGS[24]
STOCK_DELIMITATOR = OPTION_ARGS[25]
STOCK_HEADER = OPTION_ARGS[26]
STOCK_DATE_FORMAT = OPTION_ARGS[27]
STOCK_UNITS_CONVERSION = OPTION_ARGS[28]
STOCK_UNITS_DECIMAL = OPTION_ARGS[29]
STOCK_AMOUNT_CONVERSION = OPTION_ARGS[30]
STOCK_AMOUNT_DECIMAL = OPTION_ARGS[31]
ENCODING = OPTION_ARGS[32]
DATE = OPTION_ARGS[33]
SSHOT_CXY = OPTION_ARGS[34]
SSHOT_TXT = OPTION_ARGS[35]
MATRIX = [str(char) for char in OPTION_ARGS[36]]

IMAGE_BASED_FUNCTIONS_TIMEOUT = int(TIMEOUT) #In seconds
if len(DATE) > 3:
    IMAGE_WAIT_TIMEOUT = int(TIMEOUT)*3 #In seconds
else:
    IMAGE_WAIT_TIMEOUT = int(TIMEOUT)
IMAGE_GONE_WAIT_TIMEOUT = int(TIMEOUT) #In seconds
IMAGE_APPEARED_TIMEOUT = int(TIMEOUT)/6 #In seconds


# ==== EXTERNAL-POWERED FUNCTIONS ====

def get_string_from_image(img):
    import subprocess
    output = subprocess.check_output(["python", ABSOLUTE_PATH + "tesseract.py", img])
    return output

def get_zolbit_format(encoding, file_type, file_format, order, delimitator, header, date_format, file_path, units_conversion, units_decimal, amount_conversion, amount_decimal, file_name):
    import subprocess
    output = subprocess.check_output(["python3", ABSOLUTE_PATH + "convertZolbit.py", encoding, file_type, file_format, order, delimitator, header, date_format, file_path, units_conversion, 
        units_decimal, amount_conversion, amount_decimal, file_name])
    return output

def get_zolbit_format_trio(file_path):
    import subprocess
    output = subprocess.check_output(["python3", ABSOLUTE_PATH + "unify.py", file_path])
    return output

# === MOUSE FUNCTIONS ===

@image_based_function
def image_hover(img, timeout=IMAGE_BASED_FUNCTIONS_TIMEOUT):
    score = _walker.hover(img, timeout)
    log("INFO", "hovered {}. score: {}".format(img, str(score)))

@image_based_function
def image_click(img, timeout=IMAGE_BASED_FUNCTIONS_TIMEOUT):
    score = _walker.image_click(img, timeout)
    log("INFO", "clicked {}. score: {}".format(img, str(score)))

@image_based_function
def image_double_click(img, timeout=IMAGE_BASED_FUNCTIONS_TIMEOUT):
    score = _walker.double_click(img, timeout)
    log("INFO", "double clicked {}. score: {}".format(img, str(score)))

@image_based_function
def image_right_click(img, timeout=IMAGE_BASED_FUNCTIONS_TIMEOUT):
    score = _walker.right_click(img, timeout)
    log("INFO", "right clicked {}. score: {}".format(img, str(score)))

def mouse_move(x, y):
    _walker.mouse_move(x, y)
    log("INFO", "mouse moved " + str(x) + " " + str(y))

def click():
    _walker.click()
    log("INFO", "clicked (positional)")

def mouse_get_x():
    result = _walker.mouse_get_x()
    log("INFO", "got mouse x = " + str(result))
    return result
def mouse_get_y():
    result = _walker.mouse_get_y()
    log("INFO", "got mouse y = " + str(result))
    return result

def mouse_hold():
    _walker.mouse_down(MOUSE_LEFT)
    log("INFO", "mouse_hold")
def mouse_release():
    _walker.mouse_up(MOUSE_LEFT)
    log("INFO", "mouse_release")
def mouse_right_hold():
    _walker.mouse_down(MOUSE_RIGHT)
    log("INFO", "mouse_right_hold")
def mouse_right_release():
    _walker.mouse_up(MOUSE_RIGHT)
    log("INFO", "mouse_right_release")

# -mouse shortcuts-

def mouse_select(x, y):
    #Selecciona una region relativa a la posicion del mouse, moviendose (x, y) pixeles.
    mouse_hold()
    mouse_move(x, y)
    mouse_release()

# === WAITING FUNCTIONS ===

def time_wait(millis):
    secs = millis / 1000.0
    log("INFO", "sleeping for " + str(secs) + "s")
    time.sleep(secs)
    log("INFO", "waited time " + str(secs) + "s")

@image_based_function
def image_wait(img, timeout=IMAGE_WAIT_TIMEOUT):
    
    log("INFO", "waiting for " + img)
    #Espera hasta que aparezca la imagen img en pantalla. Si no aparece antes del timeout, arroja ImageNotPresent Exception.
    _walker.image_wait(img, timeout)
    log("INFO", "waiting success")

@image_based_function
def image_wait_multiple(*args, **kwargs):
    #Espera hasta que alguna de las imagenes aparezca, y retorna el string que contiene la imagen que aparecio.
    #Si ninguna aparece antes del timeout, arroja un string vacio.

    # Example: image_wait_multiple("badlogin.png", "screenloaded.png", "unavailable.png")
    
    log("INFO", "waiting for " + str(args))
    kwargs.setdefault("timeout", IMAGE_WAIT_TIMEOUT)
    result = _walker.image_wait_multiple(args, kwargs["timeout"])
    log("INFO", "waiting success, found {}".format(result))
    return result

@image_based_function
def image_gone_wait(img, timeout=IMAGE_GONE_WAIT_TIMEOUT):
    #Espera hasta que la imagen img se haya ido de la pantalla. Si esto no ocurre antes del timeout,
    #arroja ImageNotGone Exception (implemented in Java).
    
    log("INFO", "waiting for gone " + img)
    _walker.image_gone_wait(img, timeout)
    log("INFO", "gone success " + img)

# === BOOLEAN FUNCTIONS ===

@image_based_function
def image_appeared(img, timeout=IMAGE_APPEARED_TIMEOUT):
    #Retorna true si la imagen img aparecio en pantalla. Si no ocurre antes del timeout, arroja false.
    #El timeout debe ser corto
    result = _walker.image_appeared(img, timeout)
    if result:
        log("INFO", "image appeared " + img)
    else:
        log("INFO", "image not appeared " + img)
    return result

# === ZIP FUNCTIONS === 
def unzip(file,extension):
    zf = ZipFile(get_download_directory()+file+'.zip','r')
    name_in_zip = (zf.namelist())
    print("Nombre del archivo dentro del zip --> {}".format(name_in_zip))
    zf.extractall(get_download_directory())
    zf.close()
    os.rename(get_download_directory()+name_in_zip[0],get_download_directory()+file+extension)

def zipper(name,file,filelist=[]):
    try:
        print("Zip name-->{}".format(name))
        zf = zipfile.ZipFile(get_download_directory()+name+'.zip','w',zipfile.ZIP_DEFLATED)
        if len(filelist)==0:
            print("File to zip-->{}".format(get_download_directory()+file))
            zf.write(get_download_directory()+file,file)
        else:
            for x in range(len(filelist)):
                print("File to zip-->{}".format(get_download_directory()+filelist[x]))
                zf.write(get_download_directory()+filelist[x],filelist[x])
        print(zf.namelist())
        zf.close()
    except Exception as e:
        traceback.print_exc()

# ==== CUSTOM FUNCTIONS LOADING ====

#exec open_read(ABSOLUTE_PATH + "custom_functions.py")

# ==== STARTUP ====
try:
    exec open_read(ABSOLUTE_PATH + STARTUP_FILE)
except Exception as e:
    print("Excepcion en {}: {}".format(STARTUP_FILE, str(e)))
