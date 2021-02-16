set_imagepath("/Sikulix/Imgs/PCFactory/")
set_download_directory("/home/seluser/Downloads/")
set_screenshot_directory("/home/seluser/Screenshots/")

def make_filename(*args, **kwargs):
    kwargs.setdefault("separator", "_")
    result = ""
    for arg in args:
        result += arg + kwargs["separator"]
    return result[:-1]


def pcfactory_generic_login(**kwargs):
    def internal_dec(func):
        def inner(*inargs, **inkwargs):
            res = func(*inargs, **inkwargs)
            result = image_wait_multiple(kwargs["incorrect"], kwargs["correct"])
            if result == kwargs["incorrect"]:
                #Caso de bad login
                send_action_simple(1, 1)
                sname = make_filename("ERROR", "LOGIN", kwargs["portal"])
                screenshot_save(sname)
                tcp_send("SNDPIC1 /home/seluser/Screenshots/" + sname + ".png")
                tcp_send("FINISH1")
                abort("Credenciales de login erroneas.")
            elif result == kwargs["correct"]:
                #Caso de login OK
                send_action_simple(1, 0)
            else:
                #Caso de timeout
                send_action_simple(9, 3)
                raise ImageNotPresentException("({},{})".format(kwargs["correct"], kwargs["incorrect"]))
            return res
        return inner
    return internal_dec

portal = "PCFACTORY"
hoy = today()
ayer = previous_day(hoy)
ayer_s = date_to_string(ayer, "%Y%m%d")

@pcfactory_generic_login(incorrect="badlogin.png", correct="ventas.png", portal=portal)
def login():
    image_click("loguser.png")
    time_wait(5000)
    type(USERNAME)
    press(TAB)
    time_wait(5000)
    type(PASSWORD)
    press(ENTER)

def pre_login_screenshot():
    log_sshot = "{}_{}".format("PRELOGIN", portal)
    pass_text("ARREGLAR")
    screenshot_save(name)

def set_date(date):
    if hoy.day == 1:
        #Caso dia 1 del mes
        image_click("calendario_left.png")
    image_wait("calendario_lu.png")
    image_click("calendario_lu.png")
    repeat(date.day):
        time_wait(100)
        press(TAB)
    press(ENTER)

def get_file():
    image_click("ventas.png")
    send_action_simple(9, 0)
    send_action_simple(3, 0)
    image_wait("porempresa.png")
    image_wait("hoy.png")
    image_click("porempresa.png")
    press(DOWN)
    press(ENTER)
    image_click("hoy.png")
    image_click("dd_rangodefechas.png")
    press(TAB)
    set_date(ayer)
    image_click("porsucursal.png")
    repeat(4):
        press(TAB)
    set_date(ayer)
    image_click("consultar.png")
    image_wait("consulta_panel.png")
    time_wait(1000)
    image_click("excel.png")
    image_wait("dlprompt.png")
    filename = make_filename(RUT_EMPRESA, ayer_s, ayer_s, NOMBRE_EMPRESA, portal, "B2B", "DIA")
    type(get_download_directory() + filename)
    press(ENTER)
    time_wait(1000)
    data=get_zolbit_format(ENCODING, FILE_TYPE[:2], SALES_FILE_FORMAT, SALES_ORDER, SALES_DELIMITATOR, SALES_HEADER, SALES_DATE_FORMAT, get_download_directory(), 
                SALES_UNITS_CONVERSION, SALES_UNITS_DECIMAL, SALES_AMOUNT_CONVERSION, SALES_AMOUNT_DECIMAL, filename+SALES_FILE_FORMAT)
    print(data)
    temp=data.split(';')
    print(temp[1][:2])
    time_wait(5000)
    zipper(filename,filename+SALES_FILE_FORMAT)
    zipper('Z'+filename,'Z'+filename+'.csv')
    tcp_send("SNDFIL" + str(matrix_get("DOWNLOAD_COUNT")+1) + "   '" + filename + ".zip' " + temp[1][:2])
    # tcp_send("SNDFIL1   '" + filename + ".xlsx'")
    send_action_simple(4, 0, num_files=1)

def get_inventario(first=False):
    image_click("inventario")
    if first == True:
        send_action_simple(9, 0)
        send_action_simple(3, 0)
    image_wait("porempresa.png")
    image_click("porempresa.png")
    press(DOWN)
    press(ENTER)
    image_click("consultar.png")
    image_wait("consulta_panel.png")
    time_wait(1000)
    image_click("excel.png")
    image_wait("dlprompt.png")
    filename = make_filename(RUT_EMPRESA, ayer_s, ayer_s, NOMBRE_EMPRESA, portal, "B2B", "DIA", "INV")
    type(get_download_directory() + filename)
    press(ENTER)
    time_wait(1000)
    data=get_zolbit_format(ENCODING, FILE_TYPE[2:], STOCK_FILE_FORMAT, STOCK_ORDER, STOCK_DELIMITATOR, STOCK_HEADER, STOCK_DATE_FORMAT, get_download_directory(), 
                STOCK_UNITS_CONVERSION, STOCK_UNITS_DECIMAL, STOCK_AMOUNT_CONVERSION, STOCK_AMOUNT_DECIMAL, filename+STOCK_FILE_FORMAT)
    print(data)
    temp=data.split(';')
    print(temp[1][:2])
    time_wait(5000)
    zipper(filename,filename+SALES_FILE_FORMAT)
    zipper('Z'+filename,'Z'+filename+'.csv')
    tcp_send("SNDFIL" + str(matrix_get("DOWNLOAD_COUNT")+1) + "   '" + filename + ".zip' " + temp[1][:2])
    # tcp_send("SNDFIL2   '" + filename + ".xlsx'")
    send_action_simple(4, 0, num_files=2)
    time_wait(5000)
    tcp_send("FINISH0")

open_explorer(URL_PORTAL)
login()
first = False
if get_downloads_count() == 0:
    get_file()
else:
    first = True
get_inventario(first)
close_explorer()
