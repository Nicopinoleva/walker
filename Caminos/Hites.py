load_template("/Sikulix/BBR.py")

set_imagepath("/Sikulix/Imgs/Hites/")
set_download_directory("/home/seluser/Downloads/")
set_screenshot_directory("/home/seluser/Screenshots/")

def pre_ventas_inventario_procedure():
    image_click("prod_acts.png")

def boton_azul_procedure():
    image_click("csv.png")
    image_click("descargar.png")
    image_wait("listo.png")
    press(TAB)
    press(ENTER)

def boton_verde_procedure():
    image_click("csv.png")
    image_click("seleccionar.png")
    image_wait("listo.png")
    press(TAB)
    press(ENTER)

def finish_method():
    tcp_send("FINISH0")

obj = BBR()
obj.PORTAL = "HITES"
obj.passid = "password"
obj.enable_newBBR = True
obj.site_key = "6Le6POkUAAAAAPrhWc5b14fntw6TCU1tRgEKaLnk"
obj.enable_recaptcha = True
obj.ventas_procedure = boton_azul_procedure
obj.inventario_procedure = boton_verde_procedure
obj.pre_ventas_procedure = pre_ventas_inventario_procedure
obj.pre_inventario_procedure = pre_ventas_inventario_procedure
obj.sshot1_procedure = pre_ventas_inventario_procedure
obj.sshot2_procedure = pre_ventas_inventario_procedure
obj.finish_procedure = finish_method
# obj.checker_data["mouse_move"] = (0, 0)
# obj.checker_data["screenshot_save_crop"] = (206, -5, 72, 15)
obj.run()
