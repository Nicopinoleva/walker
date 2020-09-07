import calendar
from datetime import timedelta
set_imagepath("/Sikulix/Imgs/Corona/")
set_download_directory("/home/seluser/Downloads/")
set_screenshot_directory("/home/seluser/Screenshots/")
enable_flash(True)
Beggin_download = MATRIX[2]
Screenshots_taken = 0
LOGIN_VERIFIED = MATRIX[1]
PORTAL_LOADED = False
def string_keep_only_digits(s):
    return ''.join(i for i in s if i.isdigit())

def make_filename(*args, **kwargs):
    kwargs.setdefault("separator", "_")
    result = ""
    for arg in args:
	result += arg + kwargs["separator"]
    return result[:-1]


def tcp_send_action(action, status, num_files=0):
    tcp_send("INSERT into log (log_id, acc_id, stat_id, num_files) values ("+OPTION_LOG_ID+", "+str(action)+", "+str(status)+", "+str(num_files)+")")

PORTAL = "CORONA"

def login():
    global MATRIX
    open_explorer(URL_PORTAL)
    if image_appeared("Error.png") == True:
        image_click("Error.png")
        time_wait(2000)
        image_click("Reload.png")
        time_wait(1000)
        close_explorer()
        login()
        return
    image_click("Usuario.png")
    type(USERNAME)
    press(TAB)
    type(PASSWORD)
    image_click("Ingresar.png")
    result = image_wait_multiple("Credenciales.png", "Comercial.png", "Cerrar.png")
    if result == "Credenciales.png":
        #Caso de bad login
        tcp_send_action(1, 1)
        sname = "{}_{}_{}".format("ERROR", "LOGIN", PORTAL)
        screenshot_save(sname)
        tcp_send("SNDPIC1 /home/seluser/Screenshots/" + sname + ".png")
        tcp_send("FINISH1")
        abort("Credenciales de login erroneas.")
    elif result == "Comercial.png" or result == "Cerrar.png":
        #Caso de login OK
        if LOGIN_VERIFIED == "0":
            tcp_send_action(1, 0)
            MATRIX[1] = "1"
            tcp_send("MATRIX" + "".join(MATRIX))
    else:
        #Caso de timeout
        tcp_send_action(9, 3)
        raise ImageNotPresentException("Comercial.png")
    Get_to_dashboard()
def Get_to_dashboard():
    global PORTAL_LOADED
    repeat(2):
        time_wait(1000)
        if image_appeared("Cerrar.png"):
            image_click("Cerrar.png")
    if not PORTAL_LOADED:
        PORTAL_LOADED = True
        tcp_send_action(9, 0)
    if get_downloads_count() == 0:
        check_if_updated()
    image_click("Comercial.png")
    image_click("Ventas.png")
    time_wait(10000)
    image_click("Fecha.png")
    if get_downloads_count() == 0:
        Date_click(7)
    elif get_downloads_count() == 1:
        Date_click(1)
    elif Screenshots_taken == 0:
        if today().day == 1:
            image_click("Left.png")
            image_click("1.png")
    elif Screenshots_taken == 1:
        image_click("Left.png")
        hoy = today()
        nueva_fecha = Substract_month(hoy)
        if today().day == 1:
            image_click("Left.png")
            nueva_fecha = Substract_month(nueva_fecha)
        image_click("1.png")
        image_click("Fecha2")
        image_click("Left.png")
        if today().day == 1:
            image_click("Left.png")
        dia = calendar.monthrange(nueva_fecha.year, nueva_fecha.month)
        image_click(str(dia[1]) + ".png")
    Get_file()

def Substract_month(d):
    newd = d.replace(
        year=d.year if d.month > 1 else d.year - 1,
        month=d.month - 1 if d.month > 1 else 12,
        day=1
        )
    return newd

def check_if_updated():
    hover("Ventas_hover.png")
    mouse_move(-100, -6)
    x = mouse_get_x()
    y = mouse_get_y()
    screenshot_save_crop("checker", x + 394, y, 70, 15)
    data = get_string_from_image(get_screenshot_directory() + "checker.png")
    check_day = int(string_keep_only_digits(data.split("-")[0]))
    log("INFO", "tesseract: obtained day " + str(check_day))
    if check_day != (today() - timedelta(days=1)).day:
	tcp_send_action(9,11)
        tcp_send("HIBERN")
        abort("Datos de venta no actualizados.")
    log("INFO", "Datos de venta actualizados")

def Date_click(num_dias):
    time_wait(500)
    hoy = today()
    if    hoy.day-num_dias <= 0: 
        image_click("Left.png")
    nueva_fecha = hoy-timedelta(days=num_dias)
    repeat(nueva_fecha.day - 1):
        press(RIGHT)
        time_wait(100)
def Date_click_inverse(num_dias):
    hoy = today()
    if hoy.day - num_dias <= 0:
        image_click("Left.png")
        repeat(31):
            time_wait(100)
            press(RIGHT)
        repeat(num_dias - hoy.day - 1):
            time_wait(100)
            press(LEFT)
    else:
        repeat(num_dias - 1):
            time_wait(100)
            press(LEFT)
    press(TAB)
    
def Get_file():
    global MATRIX
    global Screenshots_taken
    global Beggin_download
    hoy = today()
    nueva_fecha = hoy-timedelta(days=7)
    nueva_fecha2 = hoy-timedelta(days=1)
    image_click("prod_acts.png")
    if get_downloads_count() != 1:
        image_click("mostrar_inv.png")
    image_click("Generar_informe.png")
    if Beggin_download == '0':
        tcp_send_action(3, 0)
        tcp_send("MATRIX" + "".join(MATRIX))
        Beggin_download = '1'
    while True:
        time_wait(2000)
        if not image_appeared("Waiting.png"):
            break
        log("INFO", "[" + OPTION_LOG_ID + "] Waiting for report")
    if get_downloads_count() < 2:
        if get_downloads_count() == 0:
            image_click("Fuente_calendario.png")
            time_wait(5000)
            image_click("Dias.png")
            mouse_move(100, 0)
            click()
            Date_click_inverse(7)
            image_click("Descargar.png")
            image_wait("Cerrar.png")
            image_click("Aceptar.png")
        else:
            image_click("Fuente_periodo.png")
            time_wait(1000)
            image_click("Si.png")
            image_wait("Cerrar.png")
            image_click("Aceptar.png")
        image_wait("Save.png")
        if get_downloads_count() == 0:
            image_double_click("Downloads.png")
            repeat(4):
                press(TAB)
            time_wait(2000)
            name1 = RUT_EMPRESA + "_" + date_to_string(nueva_fecha,"%Y%m%d") + "_" + date_to_string(nueva_fecha2,"%Y%m%d") + "_" + NOMBRE_EMPRESA + "_"+PORTAL+"_B2B_DIA" 
            type(name1)
            time_wait(2000)
            image_click("Save.png")
            time_wait(1000)
            #image_click("Cerrar.png")
            tcp_send_action(4, 0, num_files=1)
            tcp_send("SNDFIL" + str(get_downloads_count()) + "   '" + name1 + ".zip'")
            Get_to_dashboard()
        else:
            time_wait(2000)
            name2 = RUT_EMPRESA +  "_" + date_to_string(nueva_fecha2,"%Y%m%d") + "_" + date_to_string(nueva_fecha2,"%Y%m%d") + "_" + date_to_string(nueva_fecha2,"%Y%m%d") + "_" + NOMBRE_EMPRESA + "_"+PORTAL+"_B2B_DIA_INV"
            type(name2)
            time_wait(2000)
            image_click("Save.png")
            time_wait(1000)
            #image_click("Cerrar.png")
            tcp_send_action(4, 0, num_files=2)
            tcp_send("SNDFIL" + str(get_downloads_count()) + "   '" + name2 + ".zip'")
            Get_to_dashboard()

    else:
        if Screenshots_taken == 0:
            if today().day == 1:
                date = Substract_month(today())
            else:
                date = today().replace(day=1)
            nueva_fecha2 = hoy-timedelta(days=1)
            name = RUT_EMPRESA +  "_" + date_to_string(date,"%Y%m%d") + "_" + date_to_string(nueva_fecha2,"%Y%m%d") + "_" + NOMBRE_EMPRESA + "_"+PORTAL+"_B2B_MENSUAL"
            screenshot_save_crop(name,11,230,1325,700)
            Screenshots_taken = 1
            tcp_send("SNDSHO1 " + str(get_downloads_count()) + "    '" + name + ".png'")
            Get_to_dashboard()
        else:
            hoy = today()
            nueva_fecha = Substract_month(hoy)
            if today().day == 1:
                nueva_fecha = Substract_month(nueva_fecha)
            dia = calendar.monthrange(nueva_fecha.year, nueva_fecha.month)
            fecha2 = nueva_fecha.replace(day=dia[1])
            name = RUT_EMPRESA +  "_" + date_to_string(nueva_fecha,"%Y%m%d") + "_" + date_to_string(fecha2,"%Y%m%d") + "_" + NOMBRE_EMPRESA + "_"+PORTAL+"_B2B_MENSUAL"
            screenshot_save_crop(name,11,230,1325,700)
            tcp_send("SNDSHO2 " + str(get_downloads_count()) + "    '" + name + ".png'")
            tcp_send("FINISH0")
            close_explorer()
login()
