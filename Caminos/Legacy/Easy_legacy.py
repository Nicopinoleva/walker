import calendar
from datetime import timedelta
set_imagepath("/Sikulix/Imgs/Easy/")
set_download_directory("/home/seluser/Downloads/")
set_screenshot_directory("/home/seluser/Screenshots/")
enable_flash(True)

matrix_register("LOGIN_CORRECTO")
matrix_register("BEGIN_DOWNLOAD")

Beggin_download = '0'
Screenshots_taken = 0

def string_keep_only_digits(s):
    return ''.join(i for i in s if i.isdigit())

def tcp_send_action(action, status, num_files=0):
    tcp_send("INSERT into log (log_id, acc_id, stat_id, num_files) values ("+OPTION_LOG_ID+", "+str(action)+", "+str(status)+", "+str(num_files)+")")

PORTAL = "EASY"

def check_if_updated():
    hover("Ventas_hover.png")
    mouse_move(240, -5)
    x = mouse_get_x()
    y = mouse_get_y()
    screenshot_save_crop("checker", x, y, 70, 15)
    data = get_string_from_image(get_screenshot_directory() + "checker.png")
    check_day = int(string_keep_only_digits(data.split("-")[0]))
    log("INFO", "tesseract: obtained day " + str(check_day))
    if check_day != (today() - timedelta(days=1)).day:
        tcp_send("HIBERN")
        abort("El portal no ha actualizado sus datos de venta.")
    log("INFO", "Datos de venta actualizados")


def login():
    open_explorer(URL_PORTAL)
    if image_appeared("Error.png") == True:
        image_click("Error.png")
        time_wait(2000)
        image_click("Reload.png")
        time_wait(1000)
        close_explorer()
        login()
        return
    image_click("Email.png")
    type(USERNAME)
    press(TAB)
    type(PASSWORD)
    image_click("Log_in.png")
    result = image_wait_multiple("Credenciales.png", "Comercial.png", "Cerrar.png")
    if result == "Credenciales.png":
        #Caso de bad login
        tcp_send_action(1, 1)
        sname = make_filename("ERROR", "LOGIN", portal)
        screenshot_save(sname)
        tcp_send("SNDPIC1 /home/seluser/Screenshots/" + sname + ".png")
        tcp_send("FINISH1")
        abort("Credenciales de login erroneas.")
    elif result == "Comercial.png" or result == "Cerrar.png":
        #Caso de login OK
        if not matrix_get("LOGIN_CORRECTO"):
            tcp_send_action(1, 0)
            matrix_set("LOGIN_CORRECTO", True)
    else:
        #Caso de timeout
        tcp_send_action(9, 3)
        raise ImageNotPresentException("(Credenciales.png, Comercial.png, Cerrar.png)")
    Get_to_dashboard()
def Get_to_dashboard():
    repeat(2):
        if image_appeared("Cerrar.png"):
            image_click("Cerrar.png")
    if get_downloads_count() == 0:
        check_if_updated()
    image_click("Comercial.png")
    image_click("Ventas.png")
    time_wait(10000)
    image_wait("Fecha.png")
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

def Date_click(num_dias):
    hoy = today()
    if    hoy.day-num_dias <= 0: 
        image_click("Left.png")
    nueva_fecha = hoy-timedelta(days=num_dias)
    dia_click_img = str(nueva_fecha.day) + ".png"
    time_wait(3000)
    image_click(dia_click_img)

def Get_file():
    global Screenshots_taken
    hoy = today()
    nueva_fecha = hoy-timedelta(days=7)
    nueva_fecha2 = hoy-timedelta(days=1)
    image_click("Generar_informe.png")
    if not matrix_get("BEGIN_DOWNLOAD"):
        tcp_send_action(3, 0)
        matrix_set("BEGIN_DOWNLOAD", True)
    while True:
        time_wait(2000)
        if not image_appeared("Waiting.png"):
            break
        log("INFO", "[" + OPTION_LOG_ID + "] Waiting for report")
    if get_downloads_count() < 2:
        if get_downloads_count() == 0:
            image_click("Fuente_calendario.png")
            time_wait(2000)
            image_click("Seleccionar.png")
            image_wait("Guardar.png")
            image_click("Guardar.png")
            time_wait(2000)
        else:
            image_click("Fuente_periodo.png")
            time_wait(1000)
            image_click("Seleccionar.png")
            image_wait("Guardar.png")
            image_click("Guardar.png")
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
