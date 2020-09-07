set_imagepath("/Sikulix/Imgs/Falabella/")
set_download_directory("/home/seluser/Downloads/")
set_screenshot_directory("/home/seluser/Screenshots/")

rut = RUT_EMPRESA.split("+")

tiendas = ["(ADM) ADMINISTRATIVO","(RM) LYON","(RM) ALTO LAS CONDES","(RM) CENTRO","(RM) LA DEHESA",
			"(RM) MANQUEHUE","(RM) MELIPILLA","(RM) PARQUE ARAUCO","(RM) PLAZA NORTE","(RM) PLAZA OESTE","(RM) PLAZA PUENTE",
			"(RM) PLAZA TOBALABA","(RM) PLAZA VESPUCIO","(RM) ROSAS","(XII) PUNTA ARENAS","FORUS (CALPANY)","(I) IQUIQUE",
			"(II) ANTOFAGASTA","(II) CALAMA","(II) MALL ANTOFAGASTA","(III) COPIAPO","(IV) LA SERENA","(V) LA CALERA",
			"(V) QUILPUE","(V) VALPARAISO","(V) VINA DEL MAR","(VI) RANCAGUA","(VII) CURICO","(VII) TALCA","(VIII) CHILLAN",
			"(VIII) CONCEPCION CENTRO","(VIII) CONCEPCION EL TREBOL","(VIII) LOS ANGELES","(IX) TEMUCO","(X) OSORNO","(X) PUERTO MONTT",
			"(X) VALDIVIA","TIENDA EMPRESAS","TIENDA VENTA A DISTANCIA","(RM) PLAZA EGANA","(RM) SAN BERNARDO","ALDO","AMERICANINO",
			"ARAUCO MAIPU","ARICA","BENNETON","BURT`S BEES","CASTRO","CLARKS","CONNECT","COPIAPO 2","COSTANERA CENTER","ESTACION CENTRAL",
			"GEOX","INDEPENDENCIA","JOSEPH & JOSEPH","LA MARTINA","LOS ANDES","LOS DOMINICOS","MAC","MANGO","MOSSIMO","OVALLE","PACO RABANNE",
			"PROCAFECOLL","PUCON","SAN FELIPE","SAN BERNARDO","SPRING","SYBILLA","WAREHOUSE"]
imgs_tiendas = ["Tienda.png","Administrativo.png","Lyon.png","Alto.png","Centro.png","LaDehesa.png","Manquehue.png","Melipilla.png",
			"ParqueArauco.png","PlazaNorte.png","PlazaOeste.png","PlazaPuente.png","PlazaTobalaba.png","PlazaVespucio.png","Rosas.png","PuntaArenas.png",
			"Forus.png","Iquique.png","Antofagasta.png","Calama.png","MallAntofagasta.png","Copiapo.png","LaSerena.png","LaCalera.png","Quilpue.png",
			"Valparaiso.png","VinaDelMar.png","Rancagua.png","Curico.png","Talca.png","Chillan.png","ConcepcionCentro.png","ConcepcionElTrebol.png",
			"LosAngeles.png","Temuco.png","Osorno.png","PuertoMontt.png","Valdivia.png","TiendaEmpresas.png","TiendaDistancia.png","PlazaEgana.png",
			"SanBernardo.png","Aldo.png","Americanino.png","Arauco.png","Arica.png","Benetton.png","Burt.png","Castro.png","Clarks.png","Connect.png",
			"Copiapo2.png","Costanera.png","EstacionCentral.png","Geox.png","Independencia.png","Joseph.png","LaMartina.png","LosAndes.png","LosDominicos.png",
			"Mac.png","Mango.png","Mossimo.png","Ovalle.png","PacoRabanne.png","Procafecol.png","Pucon.png","SanFelipe.png","SanFernando.png","Spring.png",
                        "Sybilla.png","Warehouse.png"]

fecha1 = date_to_string(subtract_days(today(),get_weekday_as_int()),"%Y%m%d") 
fecha2 = date_to_string(previous_day(today()),"%Y%m%d") 

def login():
    open_explorer(URL_PORTAL)
    image_click("B2b.png")
    press(DOWN)
    press(ENTER)
    time_wait(2000)
    press(TAB)
    type(rut[1])
    press(TAB)
    type(USERNAME)
    press(TAB)
    type(PASSWORD)
    repeat(2):
        press(TAB)
    press(ENTER)
    time_wait(1500)
    result = image_wait_multiple("Credenciales.png", "Expirado.png", "Pop_up_kill.png")
    if result == "Crendeciales.png":
        send_action_simple(1,1)
        sname = "{}_{}".format("LOGIN", "Falabella")
        screenshot_save(sname)
        tcp_send("SNDPIC1 /home/seluser/Screenshots/" + sname + ".png")
        tcp_send("FINISH1")
        abort("Credenciales erroneas")
    elif result == "Expirado.png":
        send_action_simple(1,7)
        sname = "{}_{}".format("LOGIN", "Falabella")
        screenshot_save(sname)
        tcp_send("SNDPIC1 /home/seluser/Screenshots/" + sname + ".png")
        tcp_send("FINISH1")
        abort("Credenciales expiradas")
    elif result == "Pop_up_kill.png":
        if not matrix_get("LOGIN_CORRECT"):
            send_action_simple(1,0)
            matrix_set("LOGIN_CORRECT", True)

def get_to_dashboard():
    image_click("Pop_up_kill.png")
    send_action_simple(9,0)
    image_hover("Ventas.png")
    image_click("Analisis.png")
    image_click("Pop_up_kill_dashboard.png")
    time_wait(1500)

def dashboard():
    image_click("Linea.png")
    repeat(int(AVANZAR)):
        press(DOWN)
    press(ENTER)
    image_click("Ordenar.png")
    repeat(2):
        press(DOWN)
    press(ENTER)
    if get_weekday_as_int() == 0:
        image_click("Semana.png")
        press(DOWN)
        press(ENTER)

def change_units():
    image_click("Unidades.png")
    repeat(2):
        press(DOWN)
    press(ENTER)

def change_store(store):
    image_click(imgs_tiendas[store])
    press(DOWN)
    press(ENTER)
    image_click("Consultar.png")

def download():
    time_wait(2500)
    image_gone_wait("Waiting.png")
    image_click("Pop_up_kill_dashboard.png")
    press(PAGE_DOWN)
    image_click("Csv.png")

def file_rename(files_downloaded,U_M):
    filename = "{}_{}_{}_{}_{}_{}_{}_{}_{}_{}_{}".format(rut[0],fecha1,fecha2,fecha2,tiendas[files_downloaded],U_M,"FALABELLA",NOMBRE_EMPRESA,"B2B","DIA","INV")
    image_wait("Save.png")
    type(filename)
    image_click("Save.png")
    time_wait(2000)
    tcp_send("SNDFIL" + str(get_downloads_count()) +"   '" + filename + ".csv'")

def screenshots(num):
    if num == 1:
        change_units()
    image_click("Consultar.png")
    image_gone_wait("Waiting.png")
    image_click("Pop_up_kill_dashboard.png")
    time_wait(2500)
    if num == 0:
        filename = "{}_{}_{}_{}_{}_{}_{}_{}_{}_{}".format(rut[0],fecha1,fecha2,fecha2,"U","FALABELLA",NOMBRE_EMPRESA,"B2B","DIA","INV")
        screenshot_save_crop(filename,0,0,1360,1020)
        tcp_send("SNDSHO1 " + str(get_downloads_count()) + "     " + filename + ".png")
        matrix_set("SSHOT_1", True)
    elif num == 1:
        filename = "{}_{}_{}_{}_{}_{}_{}_{}_{}_{}".format(rut[0],fecha1,fecha2,fecha2,"M","FALABELLA",NOMBRE_EMPRESA,"B2B","DIA","INV")
        screenshot_save_crop(filename,0,0,1360,1020)
        tcp_send("SNDSHO2 " + str(get_downloads_count()) + "     " + filename + ".png")
        matrix_set("SSHOT_2", True)

def get_to_store(files_downloaded):
    image_click("Tienda.png")
    for x in range(files_downloaded):
        press(DOWN)
    press(ENTER)
    time_wait(1500)

def cycle(files_downloaded,U_M):
    for x in range (files_downloaded,int(NUM_LOCALES)):
        change_store(x)
        download()
        file_rename(x,U_M)
        if get_downloads_count() % int(OPTION_TRACE_EVERY) == 0:
            send_action_simple(4,0,get_downloads_count())

def get_files():
    files_downloaded = get_downloads_count()
    if not matrix_get("DOWNLOAD_STARTED"):
        send_action_simple(3,0)
        matrix_set("DOWNLOAD_STARTED",True)
    if files_downloaded >=0 and files_downloaded < int(NUM_LOCALES) :
        if get_downloads_count() !=0:
            get_to_store(files_downloaded)
        cycle(files_downloaded,"U")
        get_to_dashboard()
        dashboard()
        change_units()
        cycle(0,"M")
    elif files_downloaded >= int(NUM_LOCALES):
        change_units()
        files_downloaded = files_downloaded- int(NUM_LOCALES)
        print(files_downloaded)
        get_to_store(files_downloaded)
        cycle(files_downloaded,"M")
    tcp_send("FINISH0")
    close_explorer()

login()
get_to_dashboard()
dashboard()
if not matrix_get("SSHOT_1"):
    screenshots(0)
if not matrix_get("SSHOT_2"):
    screenshots(1)
get_files()
