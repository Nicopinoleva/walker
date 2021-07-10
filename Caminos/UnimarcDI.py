exec open_read("/Sikulix/BBR.py")

set_imagepath("/Sikulix/Imgs/Unimarc/")
set_download_directory("/home/seluser/Downloads/")
set_screenshot_directory("/home/seluser/Screenshots/")

def pre_ventas_procedure():
    image_click("mostrar_inv.png")
    image_click("prod_acts.png")

def pre_inventario_procedure():
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

def to_detalle_inventario_panel():
    if image_appeared("cerrar.png"):
        image_click("cerrar.png")
    time_wait(1000)
    if image_appeared("cerrar2.png"):
        image_click("cerrar2.png")
    time_wait(1000)
    image_click("logistica.png")
    if not obj._portal_loaded:
        obj._portal_loaded = True
        send_action_simple(9, 12)
    image_click("detalle_inv.png")
    time_wait(3000)

def get_detalle_inventario():
    to_detalle_inventario_panel()
    time_wait(100)
    hoy = today()
    nueva_fecha2 = obj.issued_day
    obj.pre_inventario_procedure()
    image_click("generar_informe.png")
    obj.waiter()
    image_click("boton_azul.png")
    image_click("dato_fuente.png")
    time_wait(5000)
    obj.inventario_procedure()
    image_wait("dlprompt.png")
    time_wait(2000)
    name2 = RUT_EMPRESA +  "_" + date_to_string(nueva_fecha2,"%Y%m%d") + "_" + date_to_string(nueva_fecha2,"%Y%m%d") + "_" + date_to_string(nueva_fecha2,"%Y%m%d") + "_" + NOMBRE_EMPRESA  + "_"+obj.PORTAL+"_B2B_DIA_INV"
    type(get_download_directory() + name2)
    time_wait(2000)
    image_click("save.png")
    time_wait(2000)
    send_action_simple(4, 0, num_files=2)
    tcp_send("SNDFIL" + str(get_downloads_count()) + "    '" + name2 + obj.files_downloaded_extension + "'")
    obj.finish_procedure()
    

obj = BBR()
obj.PORTAL = "UNIMARC"
obj.enable_newBBR = True
obj.enable_recaptcha = True
obj.site_key = "6Le6POkUAAAAAPrhWc5b14fntw6TCU1tRgEKaLnk"
obj.account_procedure = account_special
obj.ventas_procedure = boton_azul_procedure
obj.inventario_procedure = boton_verde_procedure
obj.pre_ventas_procedure = pre_ventas_procedure
obj.pre_inventario_procedure = pre_inventario_procedure
obj.sshot1_procedure = pre_ventas_procedure
obj.sshot2_procedure = pre_ventas_procedure
#### Se remplaza por la funcion de detalle inventario
obj.get_inventario = get_detalle_inventario
####
# obj.checker_data["mouse_move"] = (150, -7)
# obj.checker_data["screenshot_save_crop"] = (0, 0, 70, 15)
obj.finish_procedure = finish_method
obj.run()
