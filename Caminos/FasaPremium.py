load_template("/Sikulix/BBR.py")

set_imagepath("/Sikulix/Imgs/Farmaciasahumada/")
set_download_directory("/home/seluser/Downloads/")
set_screenshot_directory("/home/seluser/Screenshots/")

def to_ventas_premium_panel():
    if image_appeared("cerrar.png"):
        image_click("cerrar.png")
    time_wait(1000)
    if image_appeared("cerrar2.png"):
        image_click("cerrar2.png")
    time_wait(1000)
    image_click("comercial.png")
    if not obj._portal_loaded:
        obj._portal_loaded = True
        send_action_simple(9, 12)
    time_wait(1000)
    image_click("venta_premium.png")
    time_wait(30000)

def pre_ventas_procedure():
    image_click("mostrar_inv.png")
    image_click("locales_activos.png")
    image_click("prod_acts.png")

def pre_inventario_procedure():
    image_click("locales_activos.png")
    image_click("prod_acts.png")

def boton_azul_procedure():
    image_click("descargar.png")
    image_wait("guardar.png", timeout = 60 * 3)
    image_click("guardar.png")

def boton_verde_procedure():
    image_click("si.png")
    image_wait("guardar.png", timeout = 60 * 3)
    image_click("guardar.png")

def finish_method():
    tcp_send("FINISH0")
    
obj = BBR()
obj.PORTAL = "FASA"
obj.delay_days_tolerance = 1
obj.enable_date_inverse = True
obj.pre_ventas_procedure = pre_ventas_procedure
obj.pre_inventario_procedure = pre_inventario_procedure
obj.ventas_procedure = boton_azul_procedure
obj.inventario_procedure = boton_verde_procedure
obj.sshot1_procedure = pre_ventas_procedure
obj.sshot2_procedure = pre_ventas_procedure
obj.to_ventas_panel = to_ventas_premium_panel
obj.finish_procedure = finish_method
obj.checker_data["mouse_move"] = (-100, -6)
obj.checker_data["screenshot_save_crop"] = (390, 0, 70, 15)
obj.run()
