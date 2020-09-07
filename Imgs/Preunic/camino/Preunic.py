set_imagepath("/Sikulix/Imgs/Salcobrand/")
set_download_directory("/home/seluser/Downloads/")
set_screenshot_directory("/home/seluser/Screenshots/")

def captcha():
	pass

PORTAL = "SALCOBRAND"
fecha_guardada = "0000000"

matrix_register("screenshot_done")
matrix_register("download_started")

@generic_login(incorrect="badlogin.png", correct="monito.png", portal=PORTAL)
def login():
	image_click("username.png")
	type(USERNAME)
	press(TAB)
    type(PASSWORD)
    time_wait(10000)
	#captcha()
	image_click("entrar.png")

def go_to_mantenedor():
    time_wait(2000)
    image_click("B2B.png")
	image_wait("preunic_consumo.png")
	image_click("preunic_consumo.png")

def screenshot():
	image_click("ventas.png")
	send_action_simple(9, 0)
	image_click("diaria.png")
	image_wait("busqueda_boton.png")
	image_click("busqueda_boton.png")
	image_click("seleccione.png")
	time_wait(1000)
	press(DOWN)
	press(ENTER)
	press(TAB)
	press(TAB)
    time_wait(3000)
	press(ENTER)
	time_wait(2000)
	press(DOWN)
	press(ENTER)
	press(TAB)
    time_wait(3000)
	press(ENTER)
	time_wait(2000)
	press(DOWN)
    press(ENTER)
	image_click("buscar_boton.png")
	image_wait("cargando.png")
        image_gone_wait("cargando.png")
	if not matrix_get("screenshot_done"):
            image_hover("info.png")
            mouse_move(60, 0)
	    mouse_select(93, 0)
	    copy()
	    fecha = str(get_clipboard())
            log("INFO", fecha)
	    fecha = fecha.split("/")
            log("INFO", str(fecha))
            fecha_final = fecha[2][:4] + fecha[1] + fecha[0]
	    global fecha_guardada
	    fecha_guardada = fecha_final
	    filename = "{}_{}_{}_{}_{}_{}_{}".format(PORTAL, "B2B", "VTA", RUT_EMPRESA, fecha_final, fecha_final, "MENSUAL")
	    screenshot_save_crop_with_points(filename, 102, 447, 1233, 497)
	    send_action_simple(9, 0)
	    tcp_send("SNDSHO1 "+str(get_downloads_count())+"     " + filename + ".png")
            matrix_set("screenshot_done", True)


def get_file():
        if not matrix_get("download_started"):
	    send_action_simple(3, 0)
            matrix_set("download_started", True)
	image_hover("info.png")
	mouse_move(103, 0) #(x, y)
	click()
	result = image_wait_multiple("exportar_boton.png", "sin_resultados.png")
	if result == "exportar_boton.png":
                time_wait(2000)
		image_click("exportar_boton.png")
		image_wait("dlprompt.png")
		filename = "{}_{}_{}_{}_{}_{}_{}_{}".format(RUT_EMPRESA, fecha_guardada, fecha_guardada, NOMBRE_EMPRESA, PORTAL, "B2B", "DIA", "BRUTO")
		type(get_download_directory() + filename)
		press(ENTER)
		time_wait(1000)
		send_action_simple(4, 0, num_files=1)
		tcp_send("SNDFIL1   '" + filename + ".csv'")
	elif result == "sin_resultados.png":
		pass
	else:
		send_action_simple(9, 3)
		raise ImageNotPresentException("(exportar_boton.png, sin_resultados.png)")
	image_click("cerrar.png")



def get_inventario():
	image_click("inventario.png")
	image_click("stock_sugerido.png")
	image_wait("busqueda_boton.png")
	image_click("busqueda_boton.png")
	image_click("seleccione_ss.png")
	time_wait(1000)
	press(DOWN)
	press(ENTER)
	press(TAB)
        time_wait(3000)
	press(ENTER)
	time_wait(1000)
        press(DOWN)
        press(ENTER)
	press(TAB)
        time_wait(3000)
	press(ENTER)
	time_wait(1000)
	press(DOWN)
        press(ENTER)
	image_click("excel_extendido.png")
	image_wait("dlprompt.png")
	filename = "{}_{}_{}_{}_{}_{}_{}_{}_{}".format(RUT_EMPRESA, fecha_guardada, fecha_guardada, NOMBRE_EMPRESA, PORTAL, "B2B", "DIA", "INV", "BRUTO")
	type(get_download_directory() + filename)
	press(ENTER)
	time_wait(20000)
	send_action_simple(4, 0, num_files=2)
	tcp_send("SNDFIL2   '" + filename + ".xlsx'")

open_explorer(URL_PORTAL)
login()
go_to_mantenedor()
screenshot()
if get_downloads_count() == 0:
    get_file()
get_inventario()
tcp_send("FINISH0")
close_explorer()
