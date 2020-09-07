load_template("/Sikulix/BBR.py")

set_imagepath("/Sikulix/Imgs/Easy/")
set_download_directory("/home/seluser/Downloads/")
set_screenshot_directory("/home/seluser/Screenshots/")

def pre_inventario_procedure():
    image_click("mostrar_inv.png")

def boton_azul_procedure():
    image_click("seleccionar.png")
    image_wait("guardar.png", timeout = 60 * 3)
    image_click("guardar.png")

def boton_verde_procedure():
    image_click("seleccionar.png")
    image_wait("guardar.png", timeout = 60 * 3)
    image_click("guardar.png")

def finish_method():
    tcp_send("FINISH0")

 
def account_special():
    if image_appeared("bloqueado.png"):
        send_action_simple(1,15)
        sname = "{}_{}".format("LOGINBLQ", "EASY")
        log_sshot = "{}_{}".format("PRELOGIN", "EASY")
        screenshot_save(sname)
        tcp_send("SNDPIC1 /home/seluser/Screenshots/" + sname + ".png")
        tcp_send("SNDPIC1 /home/seluser/Screenshots/" + log_sshot + ".png")
        tcp_send("FINISH15")
        abort("Credencial login bloqueada.")

obj = BBR()
obj.PORTAL = "EASY"
obj.passid = "password"
obj.site_key = "6LcVYtEUAAAAALlg52jHvKf9IM8n2FvJfqHSyqxg"
obj.enable_recaptcha = True
obj.delay_days_tolerance = 0
obj.enable_date_inverse = False
obj.enable_error = False
obj.account_procedure = account_special
obj.ventas_procedure = boton_azul_procedure
obj.inventario_procedure = boton_verde_procedure
#obj.files_downloaded_extension = ".csv"
#obj.pre_ventas_procedure = pre_ventas_procedure
obj.pre_inventario_procedure = pre_inventario_procedure
#obj.sshot1_procedure = pre_ventas_procedure
obj.finish_procedure = finish_method
obj.checker_data["mouse_move"] = (240, -5)
obj.checker_data["screenshot_save_crop"] = (0, 0, 70, 14)
obj.run()
