load_template("/Sikulix/BBR.py")

set_imagepath("/Sikulix/Imgs/Jumbo/")
set_download_directory("/home/seluser/Downloads/")
set_screenshot_directory("/home/seluser/Screenshots/")

if "-" in NOMBRE_EMPRESA:
    sufijo = NOMBRE_EMPRESA.split("-")
    sigla = sufijo[1].split("+")
else:
    sigla = NOMBRE_EMPRESA.split("+")
    
def marca_venta_inventario_procedure(num):
    image_hover("selec_proveedor.png")
    mouse_move(200,0)
    click()
    time_wait(2000)
    for x in range (10):
        press(UP)
        time_wait(200)
    time_wait(1000)
    for x in range (int(sigla[num][-2:])):
        press(DOWN)
        time_wait(200)
    press(ENTER)

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
        send_action_simple(1,15)
        sname = "{}_{}".format("LOGINEXP", "JUMBO")
        log_sshot = "{}_{}".format("PRELOGIN", "JUMBO")
        screenshot_save(sname)
        tcp_send("SNDPIC1 /home/seluser/Screenshots/" + sname + ".png")
        tcp_send("SNDPIC1 /home/seluser/Screenshots/" + log_sshot + ".png")
        tcp_send("FINISH1")
        abort("Credencial login bloqueada.")
    else:
        pass 

def chain_run(counter):
    if obj.enable_checker:
        obj.check_if_updated()
    if not matrix_get("SSHOT_1"):
        obj.screenshot_1(counter)
        matrix_set("SSHOT_1", True)
    if not matrix_get("SSHOT_2"):
        obj.screenshot_2(counter)
        matrix_set("SSHOT_2", True)
    if matrix_get("DOWNLOAD_COUNT") == 0:
        obj.get_ventas(counter)
    time_wait(5000)
    if matrix_get("DOWNLOAD_COUNT") == 1:
        obj.get_inventario(counter)
    if obj.enable_extraDownload:
        obj.extraDownloads(proveedor=int(sigla[counter][-2:]))
    matrix_set("CYCLE_COUNT",counter+1)
    print(matrix_get("CYCLE_COUNT"))

#Heinz
obj = BBR()
obj.PORTAL = "JUMBO"
obj.passid = "password"
obj.delay_days_tolerance = 1
obj.enable_recaptcha = True
obj.enable_newBBR = True
obj.site_key = "6LcVYtEUAAAAALlg52jHvKf9IM8n2FvJfqHSyqxg"
obj.account_procedure = account_special
obj.ventas_procedure = createBoundMethod(boton_azul_procedure,obj)
obj.inventario_procedure = boton_verde_procedure
obj.marca_procedure = marca_venta_inventario_procedure
obj.marca_inv_procedure = marca_venta_inventario_procedure
#obj.pre_ventas_procedure = marca_ventas_procedure
#obj.pre_inventario_procedure = marca_inventario_procedure
#obj.sshot1_procedure = marca_ventas_procedure
#obj.sshot2_procedure = marca_ventas_procedure
obj.finish_procedure = finish_method
if EXTRA != "none" and get_weekday_as_int() == int(AVANZAR):
    obj.enable_extraDownload = True
obj.checker_data["mouse_move"] = (115, -10)
obj.checker_data["screenshot_save_crop"] = (0, 0, 70, 15)
obj.run = chain_run
counter = matrix_get("CYCLE_COUNT")
if "-" in NOMBRE_EMPRESA:
    obj.enable_customRename = True
    obj.marca = sufijo[0]
obj.login()
for x in range(counter,len(sigla)):
    obj.SIGLA = sigla[x][:2]
    obj.run(x)
    close_explorer()
    matrix_set("SSHOT_1",False)
    matrix_set("SSHOT_2",False)
    matrix_set("DOWNLOAD_COUNT",0)
obj.finish_procedure()