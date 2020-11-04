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

def boton_azul_procedure():
    image_click("descargar.png")
    image_wait("guardar.png")
    image_click("guardar.png")

def boton_verde_procedure():
    image_click("si.png")
    image_wait("guardar.png")
    image_click("guardar.png")

def pre_checker():
    image_click("cargas_datos.png")

def to_detalle_inventario_panel():
        if image_appeared("cerrar.png"):
            image_click("cerrar.png")
        time_wait(1000)
        if image_appeared("cerrar2.png"):
            image_click("cerrar2.png")
        time_wait(1000)
        image_click("abastecimiento.png")
        if not obj._portal_loaded:
            obj._portal_loaded = True
            send_action_simple(9, 12)
        image_click("detalle_inv.png")
        time_wait(30000)

def get_detalle_inventario():
    to_detalle_inventario_panel()
    time_wait(100)
    hoy = today()
    nueva_fecha2 = obj.issued_day
    obj.pre_inventario_procedure()
    image_click("generar_informe.png")
    obj.waiter()
    image_click("boton_azul.png")
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
    tcp_send("SNDFIL " + str(get_downloads_count()) + "    '" + name2 + obj.files_downloaded_extension + "'")

def finish_method():
    tcp_send("FINISH0")

obj = BBR()
obj.PORTAL = "PARIS"
obj.enable_extra_calendar = True
obj.ventas_procedure = boton_azul_procedure
obj.inventario_procedure = boton_verde_procedure
obj.pre_ventas_procedure = pre_ventas_procedure
obj.pre_inventario_procedure = pre_inventario_procedure
obj.sshot1_procedure = pre_ventas_procedure
obj.sshot2_procedure = pre_ventas_procedure
obj.pre_checker_procedure = pre_checker
#### Se remplaza por la funcion de detalle inventario
obj.get_inventario = get_detalle_inventario
####
obj.finish_procedure = finish_method
obj.checker_data["mouse_move"] = (240, -5)
obj.checker_data["screenshot_save_crop"] = (0, 0, 70, 15)
obj.run()
