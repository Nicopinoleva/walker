load_template("/Sikulix/BBR.py")

set_imagepath("/Sikulix/Imgs/Jumbo/")
set_download_directory("/home/seluser/Downloads/")
set_screenshot_directory("/home/seluser/Screenshots/")
set_min_similarity(0.75)

def boton_azul_procedure(objectReference):
    if objectReference.custom_date:
        image_click("dias")
        mouse_move(370,0)
        click()
        objectReference.date_click_dynamic(objectReference.date2,isSecondCalendar=True)
    image_click("descargar.png")
    image_wait("listo.png")
    press(TAB)
    press(ENTER)

def boton_verde_procedure():
    image_click("si.png")
    image_wait("listo.png")
    press(TAB)
    press(ENTER)

def finish_method():
    tcp_send("FINISH0")

def account_special(): 
    if image_appeared("expirada.png") == True:
        send_action_simple(1,7)
        sname = "{}_{}".format("LOGINEXP", "JUMBO")
        log_sshot = "{}_{}".format("PRELOGIN", "JUMBO")
        screenshot_save(sname)
        tcp_send("SNDPIC1 /home/seluser/Screenshots/" + sname + ".png")
        tcp_send("SNDPIC1 /home/seluser/Screenshots/" + log_sshot + ".png")
        tcp_send("FINISH7")
        abort("Credencial login expirada.")
    else:
        pass 

obj = BBR()
obj.PORTAL = "JUMBO_SI"
obj.passid = "password"
obj.delay_days_tolerance = 1
if EXTRA != "none" and get_weekday_as_int() == int(AVANZAR):
    obj.enable_extraDownload = True
obj.enable_newBBR = True
obj.enable_recaptcha = True
obj.site_key = "6LcVYtEUAAAAALlg52jHvKf9IM8n2FvJfqHSyqxg"
obj.account_procedure = account_special
obj.ventas_procedure = createBoundMethod(boton_azul_procedure,obj)
obj.inventario_procedure = boton_verde_procedure
obj.finish_procedure = finish_method
obj.checker_data["mouse_move"] = (115, -10)
obj.checker_data["screenshot_save_crop"] = (0, 0, 70, 15)
obj.run()