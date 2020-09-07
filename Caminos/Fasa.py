load_template("/Sikulix/BBR.py")

set_imagepath("/Sikulix/Imgs/Farmaciasahumada/")
set_download_directory("/home/seluser/Downloads/")
set_screenshot_directory("/home/seluser/Screenshots/")

def pre_ventas_procedure():
    image_click("mostrar_inv.png")
    image_click("locales_activos.png")
    image_click("prod_acts.png")

def pre_inventario_procedure():
    image_click("prod_acts.png")

def boton_azul_procedure():
    image_click("descargar.png")
    image_wait("guardar.png", timeout = 60 * 3)
    image_click("guardar.png")

def boton_verde_procedure():
    image_click("si.png")
    image_wait("guardar.png", timeout = 60 * 3)
    image_click("guardar.png")
    
def account_special(): 
    if image_appeared("bloqueado.png") == True:
        send_action_simple(1,15)
        sname = "{}_{}".format("LOGINBLQ", "FASA")
        log_sshot = "{}_{}".format("PRELOGIN", "FASA")
        screenshot_save(sname)
        tcp_send("SNDPIC1 /home/seluser/Screenshots/" + sname + ".png")
        tcp_send("SNDPIC1 /home/seluser/Screenshots/" + log_sshot + ".png")
        tcp_send("FINISH15")
        abort("Credencial login bloqueada.")
    else:
        pass 
def finish_method():
    tcp_send("FINISH0")

obj = BBR()
obj.PORTAL = "FASA"
obj.passid = "password"
obj.delay_days_tolerance = 1
obj.enable_date_inverse = True
obj.account_procedure = account_special
obj.pre_ventas_procedure = pre_ventas_procedure
obj.pre_inventario_procedure = pre_inventario_procedure
obj.ventas_procedure = boton_azul_procedure
obj.inventario_procedure = boton_verde_procedure
obj.sshot1_procedure = pre_ventas_procedure
obj.sshot2_procedure = pre_ventas_procedure
obj.finish_procedure = finish_method
obj.checker_data["mouse_move"] = (-100, -6)
obj.checker_data["screenshot_save_crop"] = (390, 0, 70, 15)
obj.run()
