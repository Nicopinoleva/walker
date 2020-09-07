set_imagepath("/Link/Docker/Imgs/Shell/")
set_download_directory("/home/seluser/Downloads/")
set_screenshot_directory("/home/seluser/Screenshots/")

PORTAL = "Petrobras"
fecha_guardada = "0000000"

matrix_register("screenshot_done")
matrix_register("download_started")

import time
import datetime


@generic_login(incorrect="bloqueo.png", correct="monito.png", portal=PORTAL)
def login():
    image_click("username.png")
    type(USERNAME)
    press(TAB)
    type(PASSWORD)
    press(TAB)
    type(RUT_EMPRESA)
    press(TAB)
    press(TAB)
    time_wait(1000)
    image_click("entrar.png")

def go_to_sellthrough():
    time_wait(3000)
    image_wait("sellthrough.png")
    image_click("sellthrough.png")
    time_wait(3000)
    image_wait("informe.png")
    image_click("formatosalida.png")
    time_wait(5000)
    image_click("excel.png")
    press(TAB)
    press(TAB)
    press(TAB)

    copy()
    fecha = str(get_clipboard())
    fecha_obj = string_to_date(fecha, '%m/%d/%y')
    log("INFO", fecha)
    anteriorday = previous_day(fecha_obj)

    anteriorday_str = anteriorday.strftime("%H:%M:%S")
    type(anteriorday_str)

def get_file():

    time_wait(2000)
    image_click("ejecutar.png")
    image_wait("dlprompt.png")
    filename = "{}_{}_{}_{}_{}_{}_{}_{}".format(RUT_EMPRESA, fecha_guardada, fecha_guardada, NOMBRE_EMPRESA, PORTAL, "B2B", "DIA", "BRUTO")
    type(get_download_directory() + filename)
    press(ENTER)
    time_wait(1000)
    send_action_simple(4, 0, num_files=1)
    tcp_send("SNDFIL1   '" + filename + ".csv'")




open_explorer(URL_PORTAL)
login()
go_to_sellthrough()
get_file()
tcp_send("FINISH0")
close_explorer()