load_template("/Sikulix/BBR.py")

set_imagepath("/Sikulix/Imgs/Unimarc/")
set_download_directory("/home/seluser/Downloads/")
set_screenshot_directory("/home/seluser/Screenshots/")

sigla = NOMBRE_EMPRESA.split("+")

def marca_inventario_procedure(num):
    image_click("prod_acts.png")
    image_double_click("selec_proveedor.png")
    time_wait(2000)
    for x in range (10):
        press(UP)
        time_wait(200)
        press(TAB)
        click()
        time_wait(1000)
    for x in range (int(sigla[num][-2:])):
        press(DOWN)
        time_wait(200)

def marca_ventas_procedure(num):
    image_click("mostrar_inv.png")
    image_click("prod_acts.png")
    image_hover("selec_proveedor.png")
    mouse_get_x()
    mouse_get_y()
    mouse_move(120,0)
    mouse_get_x()
    mouse_get_y()
    click()
    time_wait(2000)
    for x in range (10):
        press(UP)
        time_wait(200)
        press(TAB)
        click()
        time_wait(1000)
    for x in range (int(sigla[num][-2:])):
        press(DOWN)
        time_wait(200)

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

def finish_method():
    tcp_send("FINISH0")

def account_special(): 
    if image_appeared("bloqueado.png") == True:
        send_action_simple(1,15)
        sname = "{}_{}".format("LOGINBLQ", "UNIMARC")
        log_sshot = "{}_{}".format("PRELOGIN", "UNIMARC")
        screenshot_save(sname)
        tcp_send("SNDPIC1 /home/seluser/Screenshots/" + sname + ".png")
        tcp_send("SNDPIC1 /home/seluser/Screenshots/" + log_sshot + ".png")
        tcp_send("FINISH1")
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

def chain_run(counter):
    obj.login()
    if obj.enable_checker:
        obj.check_if_updated()
    if not matrix_get("SSHOT_1"):
        obj.screenshot_1(counter)
        matrix_set("SSHOT_1", True)
    if not matrix_get("SSHOT_2"):
        obj.screenshot_2(counter)
        matrix_set("SSHOT_2", True)
    if not matrix_get("SALES"):
        obj.get_ventas(counter)
    time_wait(5000)
    if not matrix_get("STOCK"):
        obj.get_inventario(counter)
    close_explorer()
    matrix_set("CYCLE_COUNT",counter+1)

#Heinz
obj = BBR()
obj.PORTAL = "UNIMARC"
obj.passid = "password"
obj.enable_newBBR = True
obj.enable_recaptcha = True
obj.site_key = "6Le6POkUAAAAAPrhWc5b14fntw6TCU1tRgEKaLnk"
obj.account_procedure = account_special
obj.ventas_procedure = boton_azul_procedure
obj.inventario_procedure = boton_verde_procedure
obj.marca_procedure = marca_ventas_procedure
obj.marca_inv_procedure = marca_inventario_procedure
#obj.pre_ventas_procedure = marca_ventas_procedure
#obj.pre_inventario_procedure = marca_inventario_procedure
#obj.sshot1_procedure = marca_ventas_procedure
#obj.sshot2_procedure = marca_ventas_procedure
obj.finish_procedure = finish_method
obj.checker_data["mouse_move"] = (150, -7)
obj.checker_data["screenshot_save_crop"] = (0, 0, 70, 15)
obj.run = chain_run
counter = matrix_get("CYCLE_COUNT")
for x in range(counter,len(sigla)):
    obj.SIGLA = sigla[x][:2]
    obj.run(x)
    matrix_set("SSHOT_1",False)
    matrix_set("SSHOT_2",False)
    matrix_set("SALES",False)
    matrix_set("STOCK",False)
    matrix_set("DOWNLOAD_COUNT",0)
obj.finish_procedure()
