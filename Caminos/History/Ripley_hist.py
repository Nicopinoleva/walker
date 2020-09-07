set_imagepath("/Sikulix/Imgs/Ripley")
set_download_directory("/home/seluser/Downloads")
set_screenshot_directory("/home/seluser/Screenshots")

def get_primer_dia_del_mes(date):
	return date.replace(day=1)

def substract_day(date, days=1):
	return date - datetime.timedelta(days)

def custom_date_to_string(date):
	return date.strftime("%d-%m-%Y")
def format_date_screenshot(date):
	return date.strftime("%Y%m%d")

def tcp_send_action(action, status, num_files=0):
	lol=1
	#tcp_send("INSERT into log (log_id, acc_id, stat_id, num_files) values ("+OPTION_LOG_ID+", "+str(action)+", "+str(status)+", "+str(num_files)+")")

def make_filename(*args, **kwargs):
	kwargs.setdefault("separator", "_")
	result = ""
	for arg in args:
		result += arg + kwargs["separator"]
	return result[:-1]

yesterday = substract_day(datetime.date.today())
primer_dia_mes = get_primer_dia_del_mes(yesterday)
portal = "RIPLEY"
numero_de_archivo=1
total_archivos_a_descargar=NUM_LOCALES


def login():
	image_click("loguser.png")
	type(USERNAME)
	image_click("pswd.png")
	type(PASSWORD)
	image_click("entrar.png")
	time_wait(2000)
	result = image_wait_multiple("badlogin.png", "portalcheck.png")
	if result == "badlogin.png":
		#Caso de bad login
		tcp_send_action(1, 1)
		sname = make_filename("ERROR", "LOGIN", portal)
		screenshot_save(sname)
		#tcp_send("SNDPIC1 /home/seluser/Screenshots/" + sname + ".png")
		#tcp_send("FINISH1")
		abort("Credenciales de login erroneas.")
	elif result == "portalcheck.png":
		#Caso de login OK
		tcp_send_action(1, 0)
	else:
		#Caso de timeout
		tcp_send_action(9, 3)
		raise ImageNotPresentException("portalcheck.png")

def ir_a_seccion(seccion, first=False):
	image_click("consultas.png")
	if first:
		tcp_send_action(9, 0)
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
	primer_dia_mes_str = custom_date_to_string(primer_dia_mes)
	type(primer_dia_mes_str)
	repeat(8):
		press(TAB)
	press(SPACE)
	image_click("buscar.png")
	image_wait("criterios.png")
	image_click("criterios.png")
	sname = "RIPLEY_B2B_VTA_"+RUT_EMPRESA+"_"+format_date_screenshot(primer_dia_mes)+"_"+format_date_screenshot(yesterday)+"_MENSUAL"
	screenshot_save_crop_with_points(sname, 180, 287, 1348, 618)
	#tcp_send("SNDSHO1 0    " + sname + ".png")

def download_hist(x, fecha):
	numero_de_archivo=x
	tcp_send_action(3, 0)
	image_wait("consdet.png")
	image_click("consdet.png")
	image_wait("diaria.png")
	image_click("diaria.png")
	press(TAB)
	press(TAB)
	ayer = custom_date_to_string(fecha)
	type(ayer)
	press(TAB)
	type(ayer)
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
	ayer_slugy = format_date_screenshot(fecha)
	b2b = "B2B"
	dia = "DIA"
	filename = make_filename(RUT_EMPRESA, ayer_slugy, ayer_slugy, portal, b2b, dia)
	type(get_download_directory() + filename)
	press(ENTER)
	time_wait(500)
	#tcp_send("SNDFIL" +  numero_de_archivo + "   '" + filename + ".csv'")
	tcp_send_action(4, 0, num_files=numero_de_archivo)   # action:4=progreso descarga
	#time_wait(1000)
	
def assign_yesterday():
	global total_archivos_a_descargar
	global numero_de_archivo
	global total_archivos_descargados
	total_archivos_descargados=get_files_count(get_download_directory())
	global yesterday
	print("total_archivos_descargados: {}".format(str(total_archivos_descargados)))

	if total_archivos_descargados >= 1 and total_archivos_descargados < total_archivos_a_descargar:
		log("INFO1", "Archivos descargados: {} / Numero de archivo: {} / Total archivos a descargar: {} / Yesterday: {}".format(str(total_archivos_descargados),str(numero_de_archivo),str(total_archivos_a_descargar), str(yesterday)))	
		numero_de_archivo = total_archivos_descargados+1
		total_archivos_a_descargar = total_archivos_a_descargar - total_archivos_descargados
		yesterday = substract_day(datetime.date.today(), total_archivos_descargados+1)
		log("INFO2", "Archivos descargados: {} / Numero de archivo: {} / Total archivos a descargar: {} / Yesterday: {}".format(str(total_archivos_descargados),str(numero_de_archivo),str(total_archivos_a_descargar), str(yesterday)))	
	elif total_archivos_descargados == total_archivos_a_descargar:
		log("INFO", "Todos los archivos fueron descargados")
		total_archivos_a_descargar = 0
	elif total_archivos_descargados == 0:
		yesterday = substract_day(datetime.date.today())
		log("INFO", "Ningun archivo previamente descargado, comienza la descarga")
		total_archivos_a_descargar= NUM_LOCALES
		numero_de_archivo= 1
	else:
		log("ERROR", "total_archivos_descargados es negativo: {}".format(str(total_archivos_descargados)))
		close_explorer()
	return int(total_archivos_a_descargar)	
	
		
	
	# click()
	# image_wait("dlprompt.png")
	# time_wait(5000)
	# inventario_filename = make_filename(RUT_EMPRESA, ayer_slugy, ayer_slugy, ayer_slugy, portal, b2b, dia, "INV")
	# type(get_download_directory() + inventario_filename)
	# press(ENTER)
	# time_wait(1000)
	# tcp_send("SNDFIL2   '" + inventario_filename + ".csv'")
	# tcp_send_action(4, 0, num_files=2)
	# time_wait(5000)
	# tcp_send("FINISH0")

open_explorer(URL_PORTAL)
login()
total_archivos_para_descargar=assign_yesterday()
ir_a_seccion("consdet.png")
for x in range(total_archivos_para_descargar):
	download_hist(x+numero_de_archivo+1,yesterday)
	log("INFO", "Descarga ejecutada, iteracion numero: {} / Dia: {}".format(str(x+numero_de_archivo+1), str(yesterday)))
	yesterday=substract_day(yesterday)

close_explorer()
