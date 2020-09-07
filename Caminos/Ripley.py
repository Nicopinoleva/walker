set_imagepath("/Sikulix/Imgs/Ripley/")
set_download_directory("/home/seluser/Downloads/")
set_screenshot_directory("/home/seluser/Screenshots/")

def get_primer_dia_del_mes(date):
	return date.replace(day=1)

def substract_day(date, num):
	return date - datetime.timedelta(num)

def custom_date_to_string(date):
	return date.strftime("%d-%m-%Y")
def format_date_screenshot(date):
	return date.strftime("%Y%m%d")


def make_filename(*args, **kwargs):
	kwargs.setdefault("separator", "_")
	result = ""
	for arg in args:
		result += arg + kwargs["separator"]
	return result[:-1]

yesterday = substract_day(datetime.date.today(),1)
primer_dia_mes = get_primer_dia_del_mes(yesterday)
primer_dia_mes_str = date_to_string(primer_dia_mes,"%d-%m-%Y")
first_day_of_previous_month = get_first_day_of_month(get_previous_month(previous_day(today())))
first_day_of_previous_month_str = date_to_string(first_day_of_previous_month,"%d-%m-%Y")
last_day_of_previous_month_str = str(get_last_day_of_month(get_previous_month(previous_day(today())))) + "-" + date_to_string(get_first_day_of_month(get_previous_month(previous_day(today()))),"%m-%Y") 
last_day_of_previous_month_str2 = date_to_string(get_first_day_of_month(get_previous_month(previous_day(today()))),"%Y%m") + str(get_last_day_of_month(get_previous_month(previous_day(today()))))
portal = "RIPLEY"

def login():
        log_sshot = "{}_{}".format("PRELOGIN", portal) 
	image_click("loguser.png")
        press(TAB)
	type(USERNAME)
	press(TAB)
	type(PASSWORD)
        pre_login_screenshot(log_sshot)
	image_click("entrar.png")
	time_wait(2000)	
	while(1):
		result = image_wait_multiple("badlogin.png", "portalcheck.png", "elegir_prove.png")
		if result == "badlogin.png":
			#Caso de bad login
			send_action_simple(1, 1)
			sname = make_filename("ERROR", "LOGIN", portal)
			screenshot_save(sname)
                        tcp_send("SNDPIC1 /home/seluser/Screenshots/" + sname + ".png")
                        tcp_send("SNDPIC1 /home/seluser/Screenshots/" + log_sshot + ".png")
			tcp_send("FINISH1")
			abort("Credenciales de login erroneas.")
			break
		elif result == "portalcheck.png":
			#Caso de login OK
			send_action_simple(1, 0)
                        matrix_set("LOGIN_CORRECT",True)
			break
		elif result == "elegir_prove.png":
			#Caso de opcion proveedor
			for i in range (1,6):
				press(TAB)
			press(DOWN)
			press(DOWN)
			image_click("entrar.png")
		else:
			#Caso de timeout
			send_action_simple(9, 3)
			raise ImageNotPresentException("portalcheck.png")
			break

def pre_login_screenshot(name):
    pass_text("txtPassword")
    screenshot_save(name)

def ir_a_seccion(seccion, first=False):
	image_click("consultas.png")
	if first:
		send_action_simple(9, 0)
	image_wait("ventas.png")
	image_click("ventas.png")
	image_wait(seccion)
	image_click(seccion)

def screenshot():
	ir_a_seccion("consres.png", first=True)
	image_wait("diaria.png")
	image_click("diaria.png")
	repeat(3):
		press(TAB)
        if not matrix_get("SSHOT_1"):
            time_wait(1000)
            primer_dia_mes_str = date_to_string(primer_dia_mes,"%d-%m-%Y")
            type(primer_dia_mes_str)
            time_wait(1000)
            repeat(8):
                time_wait(1000)
                press(TAB)
        else:
            time_wait(1000)
            type(first_day_of_previous_month_str)
            time_wait(1000)
            press(TAB)
            time_wait(1000)
            type(last_day_of_previous_month_str)
            repeat(7):
                time_wait(1000)
                press(TAB)
	press(SPACE)
	image_click("buscar.png")
	image_wait("criterios.png")
	image_click("criterios.png")
        if not matrix_get("SSHOT_1"):
            sname = "RIPLEY_B2B_VTA_"+RUT_EMPRESA+"_"+date_to_string(primer_dia_mes,"%Y%m%d")+"_"+date_to_string(yesterday,"%Y%m%d")+"_"+NOMBRE_EMPRESA+ "_MENSUAL"	
	    screenshot_save_crop_with_points(sname, 180, 287, 1348, 618)
	    tcp_send("SNDSHO1 0    " + sname + ".png")
            matrix_set("SSHOT_1",True)
        else:
            sname = "RIPLEY_B2B_VTA_"+RUT_EMPRESA+"_"+date_to_string(first_day_of_previous_month,"%Y%m%d")+"_"+last_day_of_previous_month_str2+"_"+NOMBRE_EMPRESA+ "_MENSUAL"
            screenshot_save_crop_with_points(sname, 180, 287, 1348, 618)
            tcp_send("SNDSHO2 0    " + sname + ".png")
            matrix_set("SSHOT_2",True)

def download():
	send_action_simple(3, 0)
	ir_a_seccion("consdet.png")
	image_wait("diaria.png")
	image_click("diaria.png")
	press(TAB)
	press(TAB)
	ayer = custom_date_to_string(yesterday)
	type(ayer)
	repeat(11):
		press(TAB)
	press(SPACE)
	press(TAB)
	press(TAB)
	press(SPACE)
	image_click("buscar.png")
	image_wait("upempresa.png")
	hover("upempresa.png")
	mouse_move(0, 20)
	click()
	image_wait("dlprompt.png")
	ayer_slugy = format_date_screenshot(yesterday)
	b2b = "B2B"
	dia = "DIA"
	filename = make_filename(RUT_EMPRESA, ayer_slugy, ayer_slugy, NOMBRE_EMPRESA, portal, b2b, dia)
	type(get_download_directory() + filename)
	press(ENTER)
	time_wait(1000)
	tcp_send("SNDFIL1   '" + filename + ".csv'")
	send_action_simple(4, 0, num_files=1)
	time_wait(5000)
	click()
	image_wait("dlprompt.png")
	time_wait(5000)
	inventario_filename = make_filename(RUT_EMPRESA, ayer_slugy, ayer_slugy, ayer_slugy, NOMBRE_EMPRESA, portal, b2b, dia, "INV")
	type(get_download_directory() + inventario_filename)
	press(ENTER)
	time_wait(1000)
	tcp_send("SNDFIL2   '" + inventario_filename + ".csv'")
	send_action_simple(4, 0, num_files=2)

def download_week(num_days):
	ir_a_seccion("consdet.png")
	image_wait("diaria.png")
	image_click("diaria.png")
	press(TAB)
	press(TAB)
	dia = custom_date_to_string(substract_day(datetime.date.today(),num_days))
	type(dia)
        press(TAB)
        type(dia)
	repeat(10):
		press(TAB)
	press(SPACE)
	press(TAB)
	press(TAB)
	press(SPACE)
	image_click("buscar.png")
	image_wait("upempresa.png")
	hover("upempresa.png")
	mouse_move(0, 20)
	click()
	image_wait("dlprompt.png")
        dia_slugy = format_date_screenshot(substract_day(datetime.date.today(),num_days))
	b2b = "B2B"
	dia = "DIA"
	filename = make_filename(RUT_EMPRESA, dia_slugy, dia_slugy, NOMBRE_EMPRESA, portal, b2b, dia)
	type(get_download_directory() + filename)
	press(ENTER)
	time_wait(1000)
	tcp_send("SNDFIL" + str(get_downloads_count()) + "   '" + filename + ".csv'")
	send_action_simple(4, 0, get_downloads_count())
	time_wait(5000)

open_explorer(URL_PORTAL)
login()
screenshot()
screenshot()
download()
for x in range (get_downloads_count(),8):
	download_week(x)
tcp_send("FINISH0")
close_explorer()