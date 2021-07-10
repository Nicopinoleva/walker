exec open_read("/Sikulix/BBR.py")

set_imagepath("/Sikulix/Imgs/Construmart/")
set_download_directory("/home/seluser/Downloads/")
set_screenshot_directory("/home/seluser/Screenshots/")

def boton_azul_procedure():
    image_click("csv.png")
    image_click("seleccionar.png")
    time_wait(5000)
    image_wait("listo.png")
    press(TAB)
    press(ENTER)

def boton_verde_procedure():
    image_click("si.png")
    time_wait(5000)
    image_wait("listo.png")
    press(TAB)
    press(ENTER)

def finish_method():
    tcp_send("FINISH0")

obj = BBR()
obj.PORTAL = "CONSTRUMART"
obj.passid = "password"
obj.enable_recaptcha = True
obj.enable_newBBR = True
obj.custom_bbr = True
obj.enable_special_extra_calendar = True
obj.site_key = "6Le6POkUAAAAAPrhWc5b14fntw6TCU1tRgEKaLnk"
obj.ventas_procedure = boton_azul_procedure
obj.inventario_procedure = boton_verde_procedure
obj.finish_procedure = finish_method
obj.run()
