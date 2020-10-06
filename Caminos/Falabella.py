load_template("/Sikulix/TRIO.py")

set_imagepath("/Sikulix/Imgs/Falabella/")
set_download_directory("/home/seluser/Downloads/")
set_screenshot_directory("/home/seluser/Screenshots/")


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

def jerarquia_method():
    image_click("Jerarquia.png")
    mouse_move(285,0)
    click()
    for x in range(int(AVANZAR)):
        press(DOWN)
    press(ENTER)

obj = TRIO()
obj.PORTAL = "FALABELLA"
obj.pop_up = True
obj.jerarquia_procedure = jerarquia_method
obj.sku_num = 2
obj.tiendas = tiendas
obj.imgs_tiendas = imgs_tiendas
if EXTRA != 'none':
    obj.special_download = EXTRA
if '+' in RUT_EMPRESA:
    obj.rut = RUT_EMPRESA.split("+")
else:
    obj.rut = RUT_EMPRESA
obj.fecha1 = date_to_string(subtract_days(today(),get_weekday_as_int()),"%Y%m%d")
obj.fecha2 = date_to_string(previous_day(today()),"%Y%m%d")
obj.run()
