exec open_read("/Sikulix/BBR.py")

set_imagepath("/Sikulix/Imgs/ABCDin/")
set_download_directory("/home/seluser/Downloads/")
set_screenshot_directory("/home/seluser/Screenshots/")

def pre_ventas_procedure():
    image_click("mostrar_inv.png")

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

def account_special():
    result = image_wait_multiple("bloqueado.png", "desactivado.png", "comercial.png")
    log_sshot = "{}_{}".format("PRELOGIN", "ABCDIN")
    if result == "bloqueado.png":
        send_action_simple(1,15)
        sname = "{}_{}".format("LOGINBLQ", "ABCDIN")
        screenshot_save(sname)
        tcp_send("SNDPIC1 /home/seluser/Screenshots/" + sname + ".png")
        tcp_send("SNDPIC1 /home/seluser/Screenshots/" + log_sshot + ".png")
        tcp_send("FINISH15")
        abort("Credencial login bloqueada.")
    elif result == "desactivado.png":
        send_action_simple(1,16)
        sname = "{}_{}".format("LOGINDAC", "ABCDIN")
        screenshot_save(sname)
        tcp_send("SNDPIC1 /home/seluser/Screenshots/" + sname + ".png")
        tcp_send("SNDPIC1 /home/seluser/Screenshots/" + log_sshot + ".png")
        tcp_send("FINISH16")
        abort("Credencial login desactivada.")
    else:
        pass

ABCDin = BBR()
ABCDin.PORTAL = "ABCDIN"
ABCDin.passid = "password"
ABCDin.enable_extra_calendar = True
ABCDin.account_procedure = account_special
ABCDin.ventas_procedure = boton_azul_procedure
ABCDin.inventario_procedure = boton_verde_procedure
ABCDin.pre_ventas_procedure = pre_ventas_procedure
ABCDin.sshot1_procedure = pre_ventas_procedure
ABCDin.sshot2_procedure = pre_ventas_procedure
ABCDin.finish_procedure = finish_method
ABCDin.checker_data["mouse_move"] = (-100, -6)
ABCDin.checker_data["screenshot_save_crop"] = (386, 0, 70, 15)
ABCDin.run()
