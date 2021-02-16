set_imagepath("/Sikulix/Imgs/Maicao/")
set_download_directory("/home/seluser/Downloads/")
set_screenshot_directory("/home/seluser/Screenshots/")

PORTAL = "MAICAO"

fecha = previous_day(today())
fechaIni = previous_day(today())
fechaFin = previous_day(today())
fechaDia = int(previous_day(today()).day)
fechaMes = int(previous_day(today()).month)

@generic_login(incorrect="1bad_login.png", correct="1descargas.png", portal=PORTAL)
def login():
    image_click("0user.png")
    type(USERNAME)
    time_wait(5000)
    press(TAB)
    type(PASSWORD)
    pre_login_screenshot()
    time_wait(1000)
    image_click("0entrar.png")

def pre_login_screenshot():
    log_sshot = "{}_{}".format("PRELOGIN", PORTAL)
    pass_text("P101_PASSWORD")
    screenshot_save(log_sshot)

def go_to_mantenedor():
    time_wait(2000)
    image_wait("1logged.png")
    image_click("1descargas.png")
    image_wait("2descargas.png")

def screenshot():
    send_action_simple(9, 0)
    if not matrix_get("SSHOT_1"):
        filename = "{}_{}_{}_{}_{}".format(PORTAL, "B2B", "VTA", RUT_EMPRESA, "ANUAL")
        screenshot_save_crop_with_points(filename, 10, 250, 1260, 430)
        send_action_simple(9, 0)
        tcp_send("SNDSHO1 "+str(get_downloads_count())+"     " + filename + ".png")
        matrix_set("SSHOT_1", True)

def get_file():
    global fechaIni
    global fecha
    #global fechaFin
    if not matrix_get("DOWNLOAD_STARTED"):
        send_action_simple(3, 0)
        matrix_set("DOWNLOAD_STARTED", True)
        time_wait(3000) 
        image_click("2mes.png")
        time_wait(2000)
        if(fechaMes == 1):
            press(ENTER)
        elif(fechaMes == 2):
            press(DOWN)
            press(ENTER)
        elif(fechaMes == 3):
            for i in range (1,3):
                press(DOWN)
                time_wait(300)
            press(ENTER)
        elif(fechaMes == 4):
            for i in range (1,4):
                press(DOWN)
                time_wait(300)
            press(ENTER)
        elif(fechaMes == 5):
            for i in range (1,5):
                press(DOWN)
                time_wait(300)
            press(ENTER)
        elif(fechaMes == 6):
            for i in range (1,6):
                press(DOWN)
                time_wait(300)
            press(ENTER)
        elif(fechaMes == 7):
            for i in range (1,7):
                press(DOWN)
                time_wait(300)
            press(ENTER)
        elif(fechaMes == 8):
            for i in range (1,8):
                press(DOWN)
                time_wait(300)
            press(ENTER)
        elif(fechaMes == 9):
            for i in range (1,9):
                press(DOWN)
                time_wait(300)
            press(ENTER)
        elif(fechaMes == 10):
            for i in range (1,10):
                press(DOWN)
                time_wait(300)
            press(ENTER)
        elif(fechaMes == 11):
            for i in range (1,11):
                press(DOWN)
                time_wait(300)
            press(ENTER)
        elif(fechaMes == 12):
            for i in range (1,12):
                press(DOWN)
                time_wait(300)
            press(ENTER)
        time_wait(8000)
        image_click("2semana.png")
        time_wait(2000) 
        if(fechaDia >= 1 and fechaDia <= 7):
            press(ENTER)
            fechaIni = fechaIni.replace(day=1)
            #fechaFin = fechaFin.replace(day=7)
        elif(fechaDia >= 8 and fechaDia <= 14):
            press(DOWN)
            time_wait(300)
            press(ENTER)
            fechaIni = fechaIni.replace(day=8)
            #fechaFin = fechaFin.replace(day=14)
        elif(fechaDia >= 15 and fechaDia <= 21):
            for i in range (1,3):
                press(DOWN)
                time_wait(300)
            press(ENTER)
            fechaIni = fechaIni.replace(day=15)
            #fechaFin = fechaFin.replace(day=21)
        elif(fechaDia >= 22 and fechaDia <= 28):
            for i in range (1,4):
                press(DOWN)
                time_wait(300)
            press(ENTER)
            fechaIni = fechaIni.replace(day=22)
            #fechaFin = fechaFin.replace(day=28)
        elif(fechaDia >= 29 and fechaDia <= 31):
            for i in range (1,5):
                press(DOWN)
                time_wait(300)
            press(ENTER)
            fechaIni = fechaIni.replace(day=29)
            #fechaFin = fechaFin.replace(day=int(get_last_day_of_month(fechaFin)))
        time_wait(2000) 
        image_click("3descventa.png")
        while(image_appeared("5waiting_desc.png")):
            time_wait(2000)
        image_wait("dlprompt.png")
        filename = RUT_EMPRESA + "_" + date_to_string(fechaIni,"%Y%m%d") + "_" + date_to_string(fecha,"%Y%m%d") + "_" + NOMBRE_EMPRESA + "_" + PORTAL +"_B2B_DIA"
        type(get_download_directory() + filename)
        press(ENTER)
        time_wait(1000)
        zolconvert(False,filename)
        send_action_simple(4, 0, num_files=1)
        # tcp_send("SNDFIL1   '" + filename + ".csv'")

def get_inventario():
    time_wait(3000)
    image_wait("5venta_lista.png")
    image_click("3descinv.png")
    time_wait(10000)
    while(True):
        if image_appeared("5waiting_desc.png"):
            tcp_send("ESPERO")
        else:
            break
    # while(image_appeared("5waiting_desc.png")):
    #       time_wait(2000)
    image_wait("dlprompt.png")
    filename = RUT_EMPRESA +  "_" + date_to_string(fecha,"%Y%m%d") + "_" + date_to_string(fecha,"%Y%m%d") + "_" + date_to_string(fecha,"%Y%m%d") + "_" + NOMBRE_EMPRESA + "_"+ PORTAL +"_B2B_DIA_INV"
    type(get_download_directory() + filename)
    press(ENTER)
    time_wait(10000)
    while(image_appeared("6inv_carga.png")):
        time_wait(8000)
    zolconvert(True,filename)
    send_action_simple(4, 0, num_files=2)
    # tcp_send("SNDFIL2   '" + filename + ".csv'")

def zolconvert(isStock,name):
        if isStock:
            data=get_zolbit_format(ENCODING, FILE_TYPE[2:], STOCK_FILE_FORMAT, STOCK_ORDER, STOCK_DELIMITATOR, STOCK_HEADER, STOCK_DATE_FORMAT, get_download_directory(), 
                STOCK_UNITS_CONVERSION, STOCK_UNITS_DECIMAL, STOCK_AMOUNT_CONVERSION, STOCK_AMOUNT_DECIMAL, name+STOCK_FILE_FORMAT)
            print(data)
            time_wait(5000)
            stockname = RUT_EMPRESA +  "_" + date_to_string(fecha,"%Y%m%d") + "_" + date_to_string(fecha,"%Y%m%d") + "_" + NOMBRE_EMPRESA + "_"+ PORTAL +"_B2B_DIA_INV"
            zipper(name,name+STOCK_FILE_FORMAT)
            zipper('Z'+name,'Z'+stockname+STOCK_FILE_FORMAT)
        else:
            data=get_zolbit_format(ENCODING, FILE_TYPE[:2], SALES_FILE_FORMAT, SALES_ORDER, SALES_DELIMITATOR, SALES_HEADER, SALES_DATE_FORMAT, get_download_directory(), 
                SALES_UNITS_CONVERSION, SALES_UNITS_DECIMAL, SALES_AMOUNT_CONVERSION, SALES_AMOUNT_DECIMAL, name+SALES_FILE_FORMAT)
            print(data)
            time_wait(5000)
            zipper(name,name+SALES_FILE_FORMAT)
            zipper('Z'+name,'Z'+name+SALES_FILE_FORMAT)
        temp=data.split(';')
        print(temp[1][:2])
        matrix_set("DOWNLOAD_COUNT",matrix_get("DOWNLOAD_COUNT")+1)
        tcp_send("SNDFIL " + str(matrix_get("DOWNLOAD_COUNT")) + "    '" + name +  ".zip'" + " " + temp[1][:2])

open_explorer(URL_PORTAL)
login()
screenshot()
go_to_mantenedor()
if matrix_get("DOWNLOAD_COUNT") == 0:
    get_file()
time_wait(5000)
if matrix_get("DOWNLOAD_COUNT") == 1:
    get_inventario()
tcp_send("FINISH0")
close_explorer()

