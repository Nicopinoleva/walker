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

def account_special(): 
    if image_appeared("desactivado.png") == True:
        send_action_simple(1,16)
        sname = "{}_{}".format("LOGINDSC", "PARIS")
        log_sshot = "{}_{}".format("PRELOGIN", "PARIS")
        screenshot_save(sname)
        tcp_send("SNDPIC1 /home/seluser/Screenshots/" + sname + ".png")
        tcp_send("SNDPIC1 /home/seluser/Screenshots/" + log_sshot + ".png")
        tcp_send("FINISH16")
        abort("Credencial login desactivada.")
    else:
        pass

obj = BBR()
obj.PORTAL = "PARIS"
obj.passid = "password"
obj.enable_special_extra_calendar = True
obj.enable_extra_calendar = True
obj.enable_extra_calendar_no_first = True
obj.enable_newBBR = True
obj.account_procedure = account_special
obj.site_key = "6LcVYtEUAAAAALlg52jHvKf9IM8n2FvJfqHSyqxg"
obj.enable_recaptcha = True
obj.ventas_procedure = boton_azul_procedure
obj.inventario_procedure = boton_verde_procedure
obj.pre_ventas_procedure = pre_ventas_procedure
obj.pre_inventario_procedure = pre_inventario_procedure
obj.sshot1_procedure = pre_ventas_procedure
obj.sshot2_procedure = pre_ventas_procedure
obj.finish_procedure = finish_method
# obj.checker_data["mouse_move"] = (205, -5)
# obj.checker_data["screenshot_save_crop"] = (0, 0, 70, 15)
obj.run()