set_imagepath("/Sikulix/Imgs/Ripley/")
set_download_directory("/home/seluser/Downloads/")
set_screenshot_directory("/home/seluser/Screenshots/")

def get_primer_dia_del_mes(date):
    return date.replace(day=1)

def substract_day(date, num):
    return date - datetime.timedelta(num)

def custom_date_to_string(date):
    return date.strftime("%d-%m-%Y")

def format_date_screenshot(date):
    return date.strftime("%Y%m%d")


def make_filename(*args, **kwargs):
    kwargs.setdefault("separator", "_")
    result = ""
    for arg in args:
        result += arg + kwargs["separator"]
    return result[:-1]

yesterday = substract_day(datetime.date.today(),1)
primer_dia_mes = get_primer_dia_del_mes(yesterday)
primer_dia_mes_str = date_to_string(primer_dia_mes,"%d-%m-%Y")
first_day_of_previous_month = get_first_day_of_month(get_previous_month(previous_day(today())))
first_day_of_previous_month_str = date_to_string(first_day_of_previous_month,"%d-%m-%Y")
last_day_of_previous_month_str = str(get_last_day_of_month(get_previous_month(previous_day(today())))) + "-" + date_to_string(get_first_day_of_month(get_previous_month(previous_day(today()))),"%m-%Y") 
last_day_of_previous_month_str2 = date_to_string(get_first_day_of_month(get_previous_month(previous_day(today()))),"%Y%m") + str(get_last_day_of_month(get_previous_month(previous_day(today()))))
date1 = ""
date2 = ""
portal = "RIPLEY"
coords_sshot = SSHOT_CXY.split(",")

def login():
    log_sshot = "{}_{}".format("PRELOGIN", portal) 
    image_click("loguser.png")
    press(TAB)
    time_wait(5000)
    type(USERNAME)
    press(TAB)
    time_wait(5000)
    type(PASSWORD)
    pre_login_screenshot(log_sshot)
    image_click("entrar.png")
    time_wait(2000) 
    while(1):
        result = image_wait_multiple("badlogin.png", "portalcheck.png", "elegir_prove.png", "baduser.png")
        if result == "badlogin.png":
            #Caso de bad login
            send_action_simple(1, 1)
            sname = make_filename("ERROR", "LOGIN", portal)
            screenshot_save(sname)
            tcp_send("SNDPIC1 /home/seluser/Screenshots/" + sname + ".png")
            tcp_send("SNDPIC1 /home/seluser/Screenshots/" + log_sshot + ".png")
            tcp_send("FINISH1")
            abort("Credenciales de login erroneas.")
            break
        elif result == "portalcheck.png":
            #Caso de login OK
            send_action_simple(1, 0)
            matrix_set("LOGIN_CORRECT",True)
            break
        elif result == "elegir_prove.png":
            #Caso de opcion proveedor
            for i in range (1,6):
                press(TAB)
            press(DOWN)
            press(DOWN)
            image_click("entrar.png")
        elif result == "baduser.png":
            send_action_simple(1, 15)
            sname = make_filename("ERROR", "LOGIN", portal)
            screenshot_save(sname)
            tcp_send("SNDPIC1 /home/seluser/Screenshots/" + sname + ".png")
            tcp_send("SNDPIC1 /home/seluser/Screenshots/" + log_sshot + ".png")
            tcp_send("FINISH15")
            abort("Credenciales de login erroneas.")
            break
        else:
            #Caso de timeout
            send_action_simple(9, 3)
            raise ImageNotPresentException("portalcheck.png")
            break

def pre_login_screenshot(name):
    pass_text("txtPassword")
    screenshot_save(name)

def ir_a_seccion(seccion, first=False):
    image_click("consultas.png")
    if first:
        send_action_simple(9, 0)
    image_wait("ventas.png")
    image_click("ventas.png")
    mouse_move(20,0)
    time_wait(500)
    if not image_appeared(seccion):
        image_click("ventas.png")
    image_click(seccion)

def screenshot(sshot):
    ir_a_seccion("consres.png", first=True)
    image_wait("diaria.png")
    image_click("diaria.png")
    time_wait(1000)
    for x in range(3):
        press(TAB)
        time_wait(100)
    if sshot == "1":
        time_wait(1000)
        primer_dia_mes_str = date_to_string(primer_dia_mes,"%d-%m-%Y")
        type(primer_dia_mes_str)
        time_wait(1000)
        for x in range(8):
            press(TAB)
            time_wait(100)
    else:
        time_wait(1000)
        type(first_day_of_previous_month_str)
        time_wait(1000)
        press(TAB)
        time_wait(1000)
        type(last_day_of_previous_month_str)
        for x in range(7):
            press(TAB)
            time_wait(100)
    press(SPACE)
    image_click("buscar.png")
    image_wait("criterios.png")
    image_click("criterios.png")
    if sshot == "1":
        sname = "RIPLEY_B2B_VTA_"+RUT_EMPRESA+"_"+date_to_string(primer_dia_mes,"%Y%m%d")+"_"+date_to_string(yesterday,"%Y%m%d")+"_"+NOMBRE_EMPRESA+ "_MENSUAL" 
        screenshot_save_crop_with_points(sname, int(coords_sshot[0]), int(coords_sshot[1]), int(coords_sshot[2]), int(coords_sshot[3]))
        tcp_send("SNDSHO1 0    " + sname + ".png")
        matrix_set("SSHOT_1",True)
    else:
        sname = "RIPLEY_B2B_VTA_"+RUT_EMPRESA+"_"+date_to_string(first_day_of_previous_month,"%Y%m%d")+"_"+last_day_of_previous_month_str2+"_"+NOMBRE_EMPRESA+ "_MENSUAL"
        screenshot_save_crop_with_points(sname, int(coords_sshot[0]), int(coords_sshot[1]), int(coords_sshot[2]), int(coords_sshot[3]))
        tcp_send("SNDSHO2 0    " + sname + ".png")
        matrix_set("SSHOT_2",True)

def download_week(num_days,isHist=False):
    ir_a_seccion("consdet.png")
    image_wait("diaria.png")
    image_click("diaria.png")
    time_wait(1000)
    for x in range(2):
        press(TAB)
        time_wait(100)
    if isHist:
        print("Dia --> {}, Mes--> {}, Año-->{}".format(date1[6:],date1[4:6],date1[:4]))
        dia = "{}-{}-{}".format(date1[6:],date1[4:6],date1[:4])
    else:
        dia = custom_date_to_string(substract_day(datetime.date.today(),num_days+1))
    time_wait(500)
    type(dia)
    press(TAB)
    time_wait(1000)
    type(dia)
    time_wait(1000)
    for x in range(10):
        time_wait(100)
        press(TAB)
    press(SPACE)
    press(TAB)
    press(TAB)
    press(SPACE)
    image_click("buscar.png")
    image_wait("upempresa.png")
    image_click("upempresa.png")
    press(TAB)
    press(ENTER)
    image_wait("dlprompt.png")
    if isHist:
        dia_slugy = date1
    else:
        dia_slugy = format_date_screenshot(substract_day(datetime.date.today(),num_days+1))
    b2b = "B2B"
    dia = "DIA"
    filename = make_filename(RUT_EMPRESA, dia_slugy, dia_slugy, NOMBRE_EMPRESA, portal, b2b, dia)
    type(get_download_directory() + filename)
    press(ENTER)
    time_wait(5000)
    data=get_zolbit_format(ENCODING, FILE_TYPE[:2], SALES_FILE_FORMAT, SALES_ORDER, SALES_DELIMITATOR, SALES_HEADER, SALES_DATE_FORMAT, get_download_directory(), 
                SALES_UNITS_CONVERSION, SALES_UNITS_DECIMAL, SALES_AMOUNT_CONVERSION, SALES_AMOUNT_DECIMAL, filename+SALES_FILE_FORMAT)
    print(data)
    temp=data.split(';')
    print(temp[1][:2])
    time_wait(5000)
    zipper(filename,filename+SALES_FILE_FORMAT)
    zipper('Z'+filename,'Z'+filename+SALES_FILE_FORMAT)
    tcp_send("SNDFIL" + str(matrix_get("DOWNLOAD_COUNT")+1) + "   '" + filename + ".zip' " + temp[1][:2])
    # tcp_send("SNDFIL" + str(matrix_get("DOWNLOAD_COUNT")+1) + "   '" + filename + ".csv'")
    send_action_simple(4, 0, matrix_get("DOWNLOAD_COUNT")+1)
    time_wait(1000)
    if not isHist:
        matrix_set("DOWNLOAD_COUNT",matrix_get("DOWNLOAD_COUNT")+1)

def download_stock():
    ir_a_seccion("consdet.png")
    image_wait("diaria.png")
    image_click("diaria.png")
    time_wait(1000)
    for x in range(2):
        press(TAB)
        time_wait(100)
    ayer = custom_date_to_string(yesterday)
    time_wait(1000)
    type(ayer)
    time_wait(1000)
    for x in range(11):
        time_wait(100)
        press(TAB)
    press(SPACE)
    for x in range(2):
        press(TAB)
        time_wait(100)
    press(SPACE)
    image_click("buscar.png")
    image_wait("upempresa.png")
    image_click("upempresa.png")
    press(TAB)
    press(ENTER)
    image_wait("dlprompt.png")
    ayer_slugy = format_date_screenshot(yesterday)
    b2b = "B2B"
    dia = "DIA"
    inventario_filename = make_filename(RUT_EMPRESA, ayer_slugy, ayer_slugy, ayer_slugy, NOMBRE_EMPRESA, portal, b2b, dia, "INV")
    zolname = make_filename(RUT_EMPRESA, ayer_slugy, ayer_slugy, NOMBRE_EMPRESA, portal, b2b, dia, "INV")
    type(get_download_directory() + inventario_filename)
    press(ENTER)
    time_wait(5000)
    data=get_zolbit_format(ENCODING, FILE_TYPE[2:], STOCK_FILE_FORMAT, STOCK_ORDER, STOCK_DELIMITATOR, STOCK_HEADER, STOCK_DATE_FORMAT, get_download_directory(), 
                STOCK_UNITS_CONVERSION, STOCK_UNITS_DECIMAL, STOCK_AMOUNT_CONVERSION, STOCK_AMOUNT_DECIMAL, inventario_filename+STOCK_FILE_FORMAT)
    print(data)
    temp=data.split(';')
    print(temp[1][:2])
    time_wait(5000)
    zipper(inventario_filename,inventario_filename+STOCK_FILE_FORMAT)
    zipper('Z'+inventario_filename,'Z'+zolname+STOCK_FILE_FORMAT)
    tcp_send("SNDFIL" + str(matrix_get("DOWNLOAD_COUNT")+1) + "   '" + inventario_filename + ".zip' " + temp[1][:2])
    # tcp_send("SNDFIL" + str(matrix_get("DOWNLOAD_COUNT")+1) + "   '" + inventario_filename + ".csv'")
    send_action_simple(4, 0, matrix_get("DOWNLOAD_COUNT")+1)
    matrix_set("DOWNLOAD_COUNT",matrix_get("DOWNLOAD_COUNT")+1)
    time_wait(5000)

open_explorer(URL_PORTAL)
login()
global DATE
if len(DATE) != 1:
    temp = DATE.split("-")
    if "NH" in temp[0]:
        date1 = temp[0][2:]
    else:
        date1 = temp[0]
    date2 = temp[1]
    download_week(0,isHist=True)
    while(True):
        newDate = tcp_send_recieve("ENDHIS")
        DATE = newDate
        print(DATE)
        if len(newDate) < 6:
            break
        else:
            temp = newDate.split("-")
            date1 = temp[0][2:]
            date2 = temp[1]
            download_week(0,isHist=True)
else:
    if not matrix_get("SSHOT_1"):
        screenshot("1")
    if not matrix_get("SSHOT_2"):
        screenshot("2")
    if matrix_get("DOWNLOAD_STARTED") == False:
        send_action_simple(3, 0)
        matrix_set("DOWNLOAD_STARTED",True)
    if not matrix_get("SALES"):
        for x in range (int(matrix_get("DOWNLOAD_COUNT")),7):
            download_week(x)
        matrix_set("SALES",True)
    if not matrix_get("STOCK"):
        download_stock()
        matrix_set("STOCK",True)
close_explorer()
tcp_send("FINISH0")