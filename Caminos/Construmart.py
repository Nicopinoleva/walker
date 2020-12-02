exec open_read("/Sikulix/BBR.py")

set_imagepath("/Sikulix/Imgs/Construmart/")
set_download_directory("/home/seluser/Downloads/")
set_screenshot_directory("/home/seluser/Screenshots/")

def pre_ventas_procedure():
    #image_click("mostrar_inv.png")
    image_click("prod_acts.png")

def pre_inventario_procedure():
    image_click("prod_acts2.png")

def boton_azul_procedure():
    image_click("descargar.png")
    image_wait("guardar.png")
    image_click("guardar.png")

def boton_verde_procedure():
    image_click("si.png")
    image_wait("guardar.png")
    image_click("guardar.png")

def finish_method():
    tcp_send("FINISH0")

obj = BBR()
obj.PORTAL = "CONSTRUMART"
obj.passid = "password"
obj.enable_extra_calendar = True
obj.delay_days_tolerance = 1
obj.ventas_procedure = boton_azul_procedure
obj.inventario_procedure = boton_verde_procedure
obj.pre_ventas_procedure = pre_ventas_procedure
obj.pre_inventario_procedure = pre_inventario_procedure
obj.sshot1_procedure = pre_ventas_procedure
obj.sshot2_procedure = pre_ventas_procedure
obj.finish_procedure = finish_method
obj.checker_data["mouse_move"] = (-100, -6)
obj.checker_data["screenshot_save_crop"] = (386, 0, 70, 15)
obj.run()