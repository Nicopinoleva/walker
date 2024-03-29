exec open_read("/Sikulix/BBR.py")

set_imagepath("/Sikulix/Imgs/Paris/")
set_download_directory("/home/seluser/Downloads/")
set_screenshot_directory("/home/seluser/Screenshots/")

def pre_ventas_procedure():
    image_click("locales_activos.png")
    image_click("mostrar_inv.png")
    image_click("prod_acts.png")

def pre_inventario_procedure():
    image_click("prod_acts.png")
    image_click("locales_activos.png")

def boton_azul_procedure():
    image_click("descargar.png")
    image_wait("guardar.png")
    image_click("guardar.png")

def boton_verde_procedure():
    image_click("si.png")
    image_wait("guardar.png")
    image_click("guardar.png")

def pre_checker():
    image_click("cargas_datos.png")

obj = BBR()
obj.PORTAL = "PARIS"
obj.enable_date_inverse = True
obj.ventas_procedure = boton_azul_procedure
obj.inventario_procedure = boton_verde_procedure
obj.pre_ventas_procedure = pre_ventas_procedure
obj.pre_inventario_procedure = pre_inventario_procedure
obj.sshot1_procedure = pre_ventas_procedure
obj.sshot2_procedure = pre_ventas_procedure
obj.pre_checker_procedure = pre_checker
obj.checker_data["mouse_move"] = (240, -5)
obj.checker_data["screenshot_save_crop"] = (0, 0, 70, 15)
obj.run()
