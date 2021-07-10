set_imagepath("/Sikulix/Imgs/Farmaciasahumada/")
set_download_directory("/home/seluser/Downloads/")
set_screenshot_directory("/home/seluser/Screenshots/")

PORTAL="FASA"

def make_filename(*args, **kwargs):
    kwargs.setdefault("separator", "_")
    result = ""
    for arg in args:
        result += arg + kwargs["separator"]
    return result[:-1]


def login():
    log_sshot = "{}_{}".format("PRELOGIN", PORTAL) 
    image_wait("loguser.png")
    time_wait(5000)
    type(USERNAME)
    press(TAB)
    time_wait(5000)
    type(PASSWORD)
    pre_login_screenshot(log_sshot)
    image_click("ingresar.png")
    time_wait(2000)
    result = image_wait_multiple("badlogin.png", "comercial.png", "baduser.png")
    if result == "badlogin.png":
        #Caso de bad login
        send_action_simple(1, 1)
        sname = make_filename("ERROR", "LOGIN", PORTAL)
        screenshot_save(sname)
        tcp_send("SNDPIC1 /home/seluser/Screenshots/" + sname + ".png")
        tcp_send("SNDPIC1 /home/seluser/Screenshots/" + log_sshot + ".png")
        tcp_send("FINISH1")
        abort("Credenciales de login erroneas.")
    elif result == "comercial.png":
        #Caso de login OK
        send_action_simple(1, 0)
        matrix_set("LOGIN_CORRECT",True)
    elif result == "baduser.png":
        send_action_simple(1, 15)
        sname = make_filename("ERROR", "LOGIN", PORTAL)
        screenshot_save(sname)
        tcp_send("SNDPIC1 /home/seluser/Screenshots/" + sname + ".png")
        tcp_send("SNDPIC1 /home/seluser/Screenshots/" + log_sshot + ".png")
        tcp_send("FINISH15")
        abort("Credenciales de login erroneas.")
    else:
        #Caso de timeout
        send_action_simple(9, 3)
        raise ImageNotPresentException("portalcheck.png")

def pre_login_screenshot(name):
    pass_text("txtPwd")
    screenshot_save(name)

def go_to_sales():
    image_click("comercial.png")

def get_supplier_id():
    image_click("find_id.png")
    time_wait(1000)
    image_wait("rut.png")
    time_wait(2000)
    for x in range(2):
        press(TAB)
    if "," in EXTRA:
        temp=EXTRA.split(",")
        type(temp[1])
        press(TAB)
        type(temp[0])
    else:
        press(TAB)
        type(EXTRA)
    image_click("buscar_id.png")
    image_wait("id.png")
    image_click("id.png")
    press(TAB)
    press(ENTER)

def download_file(num_days,is_stock=False):
    image_click("periodo.png")
    for x in range(9):
        press(TAB)
    dia = date_to_string(subtract_days(datetime.date.today(),num_days+1),"%d-%m-%Y")
    time_wait(500)
    type(dia)
    for x in range(2):
        press(TAB)
    time_wait(500)
    type(dia)
    image_click("buscar.png")
    while True:
            tcp_send("ESPERO")
            if not image_appeared("waiting.png"):
                break
            log("INFO", "[" + OPTION_LOG_ID + "] Waiting for report")
    image_click("download.png")
    image_wait("dlprompt.png")
    dia = date_to_string(subtract_days(datetime.date.today(),num_days+1),"%Y%m%d")
    if is_stock:
        filename = make_filename(RUT_EMPRESA, dia, dia, NOMBRE_EMPRESA, PORTAL, "B2B", "DIA","INV")
    else:
        filename = make_filename(RUT_EMPRESA, dia, dia, NOMBRE_EMPRESA, PORTAL, "B2B", "DIA")
    type(get_download_directory() + filename)
    press(ENTER)
    time_wait(5000)
    if is_stock:
        data=get_zolbit_format(ENCODING, FILE_TYPE[2:], STOCK_FILE_FORMAT, STOCK_ORDER, STOCK_DELIMITATOR, STOCK_HEADER, STOCK_DATE_FORMAT, get_download_directory(),
            STOCK_UNITS_CONVERSION, STOCK_UNITS_DECIMAL, STOCK_AMOUNT_CONVERSION, STOCK_AMOUNT_DECIMAL, filename+STOCK_FILE_FORMAT)
    else:
        data=get_zolbit_format(ENCODING, FILE_TYPE[:2], SALES_FILE_FORMAT, SALES_ORDER, SALES_DELIMITATOR, SALES_HEADER, SALES_DATE_FORMAT, get_download_directory(),
            SALES_UNITS_CONVERSION, SALES_UNITS_DECIMAL, SALES_AMOUNT_CONVERSION, SALES_AMOUNT_DECIMAL, filename+SALES_FILE_FORMAT)
    print(data)
    temp=data.split(';')
    print(temp[1][:2])
    zipper(filename,filename+SALES_FILE_FORMAT)
    zipper('Z'+filename,'Z'+filename+'.csv')
    tcp_send("SNDFIL" + str(matrix_get("DOWNLOAD_COUNT")+1) + "   '" + filename + ".zip' " + temp[1][:2])
    # tcp_send("SNDFIL" + str(matrix_get("DOWNLOAD_COUNT")+1) + "   '" + filename + ".xlsx'")
    send_action_simple(4, 0, matrix_get("DOWNLOAD_COUNT")+1)
    time_wait(1000)
    matrix_set("DOWNLOAD_COUNT",matrix_get("DOWNLOAD_COUNT")+1)

open_explorer(URL_PORTAL)
login()
if matrix_get("DOWNLOAD_STARTED") == False:
    send_action_simple(3, 0)
    matrix_set("DOWNLOAD_STARTED",True)
go_to_sales()
get_supplier_id()
if not matrix_get("SALES"):
    for x in range(int(matrix_get("DOWNLOAD_COUNT")),7):
        download_file(x)
        matrix_set("SALES",True)
if not matrix_get("STOCK"):
    download_file(0,True)
    matrix_set("STOCK",True)
close_explorer()
tcp_send("FINISH0")