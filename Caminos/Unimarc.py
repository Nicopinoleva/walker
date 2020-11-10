load_template("/Sikulix/BBR.py")

set_imagepath("/Sikulix/Imgs/Unimarc/")
set_download_directory("/home/seluser/Downloads/")
set_screenshot_directory("/home/seluser/Screenshots/")

def pre_ventas_procedure():
    image_click("mostrar_inv.png")
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
        sname = "{}_{}".format("LOGINBLQ", "UNIMARC")
        log_sshot = "{}_{}".format("PRELOGIN", "UNIMARC")
        screenshot_save(sname)
        tcp_send("SNDPIC1 /home/seluser/Screenshots/" + sname + ".png")
        tcp_send("SNDPIC1 /home/seluser/Screenshots/" + log_sshot + ".png")
        tcp_send("FINISH15")
        abort("Credencial login bloqueada.")
    elif image_appeared("expirada.png") == True:
        send_action_simple(1,7)
        sname = "{}_{}".format("LOGINEXP", "UNIMARC")
        log_sshot = "{}_{}".format("PRELOGIN", "UNIMARC")
        screenshot_save(sname)
        tcp_send("SNDPIC1 /home/seluser/Screenshots/" + sname + ".png")
        tcp_send("SNDPIC1 /home/seluser/Screenshots/" + log_sshot + ".png")
        tcp_send("FINISH7")
        abort("Credencial login expirada.")
    else:
        pass 


def finish_method():
    tcp_send("FINISH0")

obj = BBR()
obj.PORTAL = "UNIMARC"
obj.passid = "password"
obj.enable_extra_calendar = True
obj.account_procedure = account_special
obj.ventas_procedure = boton_azul_procedure
obj.inventario_procedure = boton_verde_procedure
obj.pre_ventas_procedure = pre_ventas_procedure
obj.pre_inventario_procedure = pre_inventario_procedure
obj.sshot1_procedure = pre_ventas_procedure
obj.sshot2_procedure = pre_ventas_procedure
obj.finish_procedure = finish_method
obj.checker_data["mouse_move"] = (-100, -6)
obj.checker_data["screenshot_save_crop"] = (275, 0, 70, 15)
obj.run()