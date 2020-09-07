load_template("/Sikulix/BBR.py")

set_imagepath("/Sikulix/Imgs/Jumbo")
set_download_directory("/home/seluser/Downloads/")
set_screenshot_directory("/home/seluser/Screenshots/")

#NOMBRE_EMPRESA2 = NOMBRE_EMPRESA
sigla = NOMBRE_EMPRESA.split("+")

def pre_ventas_procedure_hz():
    #image_click("mostrar_inv.png")
    #image_click("prod_acts.png")
    image_click("selec_marca.png")
    #while(not image_appeared("heinz.png")):
    #   press(DOWN)
    for i in range (1,24):
        press(DOWN)
        time_wait(200)

def pre_ventas_procedure_im():
    #image_click("mostrar_inv.png")
    #image_click("prod_acts.png")
    image_click("selec_marca.png")
    #while(not image_appeared("heinz.png")):
    #   press(DOWN)
    for i in range (1,30):
        press(DOWN)
        time_wait(200)

def pre_ventas_procedure_kr():
    #image_click("mostrar_inv.png")
    #image_click("prod_acts.png")
    image_click("selec_marca.png")
    #while(not image_appeared("heinz.png")):
    #   press(DOWN)
    for i in range (1,35):
        press(DOWN)
        time_wait(200)

def pre_ventas_procedure_lp():
    #image_click("mostrar_inv.png")
    #image_click("prod_acts.png")
    image_click("selec_marca.png")
    #while(not image_appeared("heinz.png")):
    #   press(DOWN)
    for i in range (1,38):
        press(DOWN)
        time_wait(200)

def pre_inventario_procedure_hz():
	#image_click("prod_acts.png")
    image_click("selec_marca.png")
    #while(not image_appeared("heinz.png")):
    #   press(DOWN)
    for i in range (1,24):
        press(DOWN)
        time_wait(200)

def pre_inventario_procedure_im():
    #image_click("prod_acts.png")
    image_click("selec_marca.png")
    #while(not image_appeared("heinz.png")):
    #   press(DOWN)
    for i in range (1,30):
        press(DOWN)
        time_wait(200)

def pre_inventario_procedure_kr():
    #image_click("prod_acts.png")
    image_click("selec_marca.png")
    #while(not image_appeared("heinz.png")):
    #   press(DOWN)
    for i in range (1,35):
        press(DOWN)
        time_wait(200)

def pre_inventario_procedure_lp():
    #image_click("prod_acts.png")
    image_click("selec_marca.png")
    #while(not image_appeared("heinz.png")):
    #   press(DOWN)
    for i in range (1,38):
        press(DOWN)
        time_wait(200)

def boton_azul_procedure():
    time_wait(3000)
    image_click("descargar.png")
    image_wait("guardar.png", timeout = 60 * 3)
    image_click("guardar.png")

def boton_verde_procedure():
    image_click("si.png")
    image_wait("guardar.png", timeout = 60 * 3)
    image_click("guardar.png")

def finish_method():
    tcp_send("FINISH0")

def chain_run():
    obj.login()
    if obj.enable_checker:
        obj.check_if_updated()
    if not matrix_get("SSHOT_1"):
        obj.screenshot_1()
        matrix_set("SSHOT_1", True)
    if not matrix_get("SSHOT_2"):
        obj.screenshot_2()
        matrix_set("SSHOT_2", True)
    if get_downloads_count() == obj.desc:
        obj.get_ventas()
    obj.desc = obj.desc + 1
    time_wait(5000)
    if get_downloads_count() == obj.desc:
        obj.get_inventario()
    obj.desc = obj.desc + 1
    obj.empty_finish()
    close_explorer()

#Heinz
obj = BBR()
obj.PORTAL = "JUMBO_SI"
#NOMBRE_EMPRESA = NOMBRE_EMPRESA2.split("+")
#print(sigla[0])
#NOMBRE_EMPRESA = sigla[0]
NOMBRE_EMPRESA = "PH"
#print(NOMBRE_EMPRESA)
obj.desc = 0
obj.enable_recaptcha = True
obj.site_key = "6LcVYtEUAAAAALlg52jHvKf9IM8n2FvJfqHSyqxg"
#obj.marca = "HZ"
obj.delay_days_tolerance = 1
obj.enable_date_inverse = False
obj.enable_error = True
obj.ventas_procedure = boton_azul_procedure
obj.inventario_procedure = boton_verde_procedure
obj.pre_ventas_procedure = pre_ventas_procedure_hz
obj.pre_inventario_procedure = pre_inventario_procedure_hz
obj.sshot1_procedure = pre_ventas_procedure_hz
obj.sshot2_procedure = pre_ventas_procedure_hz
obj.checker_data["mouse_move"] = (240, -5)
obj.checker_data["screenshot_save_crop"] = (0, 0, 70, 15)
obj.run = chain_run
obj.run()
matrix_set("SSHOT_1",False)
matrix_set("SSHOT_2",False)

#Impo
obj = BBR()
obj.PORTAL = "JUMBO_SI"
#NOMBRE_EMPRESA = NOMBRE_EMPRESA2.split("+")
#print(sigla[1])
#NOMBRE_EMPRESA = sigla[1]
NOMBRE_EMPRESA = "PI"
#print(NOMBRE_EMPRESA)
obj.desc = 2
obj.enable_recaptcha = True
obj.site_key = "6LcVYtEUAAAAALlg52jHvKf9IM8n2FvJfqHSyqxg"
#obj.marca = "IM"
obj.delay_days_tolerance = 1
obj.enable_date_inverse = False
obj.enable_error = True
obj.ventas_procedure = boton_azul_procedure
obj.inventario_procedure = boton_verde_procedure
obj.pre_ventas_procedure = pre_ventas_procedure_im
obj.pre_inventario_procedure = pre_inventario_procedure_im
obj.sshot1_procedure = pre_ventas_procedure_im
obj.sshot2_procedure = pre_ventas_procedure_im
obj.checker_data["mouse_move"] = (240, -5)
obj.checker_data["screenshot_save_crop"] = (0, 0, 70, 15)
obj.run = chain_run
obj.run()
matrix_set("SSHOT_1",False)
matrix_set("SSHOT_2",False)

#Kraft
obj = BBR()
obj.PORTAL = "JUMBO_SI"
#NOMBRE_EMPRESA = NOMBRE_EMPRESA2.split("+")
#print(sigla[2])
#NOMBRE_EMPRESA = sigla[2]
NOMBRE_EMPRESA = "PK"
#print(NOMBRE_EMPRESA)
obj.desc = 4
obj.enable_recaptcha = True
obj.site_key = "6LcVYtEUAAAAALlg52jHvKf9IM8n2FvJfqHSyqxg"
#obj.marca = "KR"
obj.delay_days_tolerance = 1
obj.enable_date_inverse = False
obj.enable_error = True
obj.ventas_procedure = boton_azul_procedure
obj.inventario_procedure = boton_verde_procedure
obj.pre_ventas_procedure = pre_ventas_procedure_kr
obj.pre_inventario_procedure = pre_inventario_procedure_kr
obj.sshot1_procedure = pre_ventas_procedure_kr
obj.sshot2_procedure = pre_ventas_procedure_kr
obj.checker_data["mouse_move"] = (240, -5)
obj.checker_data["screenshot_save_crop"] = (0, 0, 70, 15)
obj.run = chain_run
obj.run()
matrix_set("SSHOT_1",False)
matrix_set("SSHOT_2",False)

#LP
obj = BBR()
obj.PORTAL = "JUMBO_SI"
#NOMBRE_EMPRESA = NOMBRE_EMPRESA2.split("+")
#print(sigla[3])
#NOMBRE_EMPRESA = sigla[3]
NOMBRE_EMPRESA = "PL"
#print(NOMBRE_EMPRESA)
obj.desc = 6
obj.enable_recaptcha = True
obj.site_key = "6LcVYtEUAAAAALlg52jHvKf9IM8n2FvJfqHSyqxg"
#obj.marca = "LP"
obj.delay_days_tolerance = 1
obj.enable_date_inverse = False
obj.enable_error = True
obj.ventas_procedure = boton_azul_procedure
obj.inventario_procedure = boton_verde_procedure
obj.pre_ventas_procedure = pre_ventas_procedure_lp
obj.pre_inventario_procedure = pre_inventario_procedure_lp
obj.sshot1_procedure = pre_ventas_procedure_lp
obj.sshot2_procedure = pre_ventas_procedure_lp
obj.empty_finish = finish_method
obj.checker_data["mouse_move"] = (240, -5)
obj.checker_data["screenshot_save_crop"] = (0, 0, 70, 15)
obj.run = chain_run
obj.run()
