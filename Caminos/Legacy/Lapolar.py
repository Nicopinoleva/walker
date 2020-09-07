import calendar
from datetime import timedelta
set_imagepath("/Sikulix/Imgs/LaPolar/")
set_download_directory("/home/seluser/Downloads/")
set_screenshot_directory("/home/seluser/Screenshots/")
enable_flash(True)
matrix_register("DOWNLOAD_STARTED")
PORTAL = "LAPOLAR"

def string_keep_only_digits(s):
    return ''.join(i for i in s if i.isdigit())

@generic_login_extended(incorrect=["badlogin.png"], correct=["comercial.png", "cerrar.png"], portal=PORTAL)
def login():
    open_explorer(URL_PORTAL)
    time_wait(5000)
    if image_appeared("error.png") == True:
        image_click("error.png")
        time_wait(2000)
        image_click("reload.png")
        time_wait(1000)
        close_explorer()
        login()
        return
    image_click("username.png")
    type(USERNAME)
    press(TAB)
    type(PASSWORD)
    image_click("ingresar.png")

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

def waiter():
    while True:
        time_wait(2000)
        if not image_appeared("waiting.png"):
            break
        log("INFO", "[" + OPTION_LOG_ID + "] Waiting for report")

def to_ventas_panel():
    if image_appeared("cerrar.png"):
        image_click("cerrar.png")
    if image_appeared("cerrar2.png"):
        image_click("cerrar2.png")
    image_click("comercial.png")
    image_click("ventas.png")
    time_wait(10000)

def date_click(num_dias):
    time_wait(1000)
    hoy = today()
    if    hoy.day-num_dias <= 0:
        image_click("left.png")
    nueva_fecha = subtract_days(hoy, num_dias)
    repeat(nueva_fecha.day - 1):
        press(RIGHT)
        time_wait(100)
    press(TAB)

def get_ventas():
    to_ventas_panel()
    image_click("fecha.png")
    date_click(7)
    hoy = today()
    nueva_fecha = hoy-timedelta(days=7)
    nueva_fecha2 = hoy-timedelta(days=1)
    image_click("prod_acts.png")
    image_click("mostrar_inv.png")
    image_click("generar_informe.png")
    if not matrix_get("DOWNLOAD_STARTED"):
        send_action_simple(3, 0)
        matrix_set("DOWNLOAD_STARTED", True)
    waiter()
    image_click("fuente_cal.png")
    time_wait(1000)
    image_click("descargar.png")
    time_wait(10000)
    image_wait("guardar.png", timeout=60 * 3)
    image_click("guardar.png")
    image_wait("dlprompt.png")
    name1 = RUT_EMPRESA + "_" + date_to_string(nueva_fecha,"%Y%m%d") + "_" + date_to_string(nueva_fecha2,"%Y%m%d") + "_" + NOMBRE_EMPRESA + "_"+PORTAL+"_B2B_DIA" 
    type(get_download_directory() + name1)
    time_wait(2000)
    image_click("save.png")
    time_wait(1000)
    send_action_simple(4, 0, num_files=1)
    tcp_send("SNDFIL" + str(get_downloads_count()) + "   '" + name1 + ".zip'")

def get_inventario():
    to_ventas_panel()
    image_click("fecha.png")
    date_click(1)
    hoy = today()
    nueva_fecha2 = hoy-timedelta(days=1)
    image_click("prod_acts.png")
    image_click("generar_informe.png")
    if not matrix_get("DOWNLOAD_STARTED"):
        send_action_simple(3, 0)
        matrix_set("DOWNLOAD_STARTED", True)
    waiter()
    image_click("fuente_inv.png")
    time_wait(5000)
    image_click("si.png")
    time_wait(5000)
    image_wait("guardar.png", timeout=60 * 3)
    image_click("guardar.png")
    image_wait("dlprompt.png")
    time_wait(2000)
    name2 = RUT_EMPRESA +  "_" + date_to_string(nueva_fecha2,"%Y%m%d") + "_" + date_to_string(nueva_fecha2,"%Y%m%d") + "_" + date_to_string(nueva_fecha2,"%Y%m%d") + "_" + NOMBRE_EMPRESA + "_"+PORTAL+"_B2B_DIA_INV"
    type(get_download_directory() + name2)
    time_wait(2000)
    image_click("save.png")
    time_wait(1000)
    #image_click("Cerrar.png")
    send_action_simple(4, 0, num_files=2)
    tcp_send("SNDFIL" + str(get_downloads_count()) + "   '" + name2 + ".zip'")

def screenshot_1():
    to_ventas_panel()
    image_click("fecha.png")
    if today().day == 1:
        image_click("left.png")
    image_click("1.png")
    image_click("prod_acts.png")
    image_click("mostrar_inv.png")
    image_click("generar_informe.png")
    waiter()
    if today().day == 1:
        date = get_previous_month(today())
    else:
        date = today().replace(day=1)
    nueva_fecha2 = today()-timedelta(days=1)
    name = RUT_EMPRESA +  "_" + date_to_string(date,"%Y%m%d") + "_" + date_to_string(nueva_fecha2,"%Y%m%d") + "_" + NOMBRE_EMPRESA + "_"+PORTAL+"_B2B_MENSUAL"
    screenshot_save_crop(name,11,230,1325,700)
    tcp_send("SNDSHO1 " + str(get_downloads_count()) + "    '" + name + ".png'")

def screenshot_2():
    to_ventas_panel()
    image_click("fecha.png")
    image_click("left.png")
    hoy = today()
    nueva_fecha = get_previous_month(hoy)
    if today().day == 1:
        image_click("left.png")
        nueva_fecha = get_previous_month(nueva_fecha)
    image_click("1.png")
    image_click("fecha2")
    image_click("left.png")
    if today().day == 1:
        image_click("left.png")
    dia = get_last_day_of_month(nueva_fecha)
    image_click(str(dia) + ".png")
    image_click("generar_informe.png")
    waiter()
    nueva_fecha = get_previous_month(hoy)
    if today().day == 1:
        nueva_fecha = get_previous_month(nueva_fecha)
    dia = get_last_day_of_month(nueva_fecha)
    fecha2 = nueva_fecha.replace(day=dia)
    name = RUT_EMPRESA +  "_" + date_to_string(nueva_fecha,"%Y%m%d") + "_" + date_to_string(fecha2,"%Y%m%d") + "_" + NOMBRE_EMPRESA + "_"+PORTAL+"_B2B_MENSUAL"
    screenshot_save_crop(name,11,230,1325,700)
    tcp_send("SNDSHO2 " + str(get_downloads_count()) + "    '" + name + ".png'")
    tcp_send("FINISH0")

login()
if get_downloads_count() == 0:
    check_if_updated()
    get_ventas()
if get_downloads_count() == 1:
    get_inventario()
screenshot_1()
screenshot_2()
close_explorer()
