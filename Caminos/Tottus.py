load_template("/Sikulix/TRIO.py")

set_imagepath("/Sikulix/Imgs/Tottus/")
set_download_directory("/home/seluser/Downloads/")
set_screenshot_directory("/home/seluser/Screenshots/")


tiendas = ["104-NATANIEL","107-PUENTE ALTO EYZAG.","114-CATEDRAL","115-VENTA NO PRESENCIAL FONTOVA","122-NO UTILIZAR","126-VIVACETA",
			"132-LA CISTERNAS","133-FACTORIA","136-TOTTUS MAIPU PAJARITO","148-APP TOTTUS","208-QUILLOTA","212-PENALOLEN",
			"213-VINA DEL MAR SANTA JULIA","220-MAITENCILLO","304-TALCA","312-LOS ANGELES ALEMANIA","313-CURICO NORTE",
			"314-LINARES","315-TOTTUS ANGOL","403-BODEGA MELIPILLA","404-BODEGA SAN ANTONIO","405-CD PUERTO MADERO",
		    "406-BODEGA LA NEGRA ANTF","411-CD FRUTAS Y VERDURAS","414-CENTRO PRODUCCION TALAGANTE CORDILLERA",
			"415-CENTRO PRODUCCION SAN ANTONIO","416-CENTRO PRODUCCION COLINA","418-CD TOP FRIO","421-NO UTILIZAR",
			"424-CENTRO PRODUCCION PUENTE ALTO","425-CP PANADERIA PZA OESTE","426-CP PANADERIA PTE ALTO",
			"428-CASA PASTAS","431-CD CT VERDE","499-ADM. CENTRAL TALAGENTA","502-ANTOFAGASTA II","508-NO UTILIZAR",
			"511-VALLENAR","9907-CT TRANSPORTISTA VTA VERDE"]

imgs_tiendas = ["Tienda.png","104-nataniel.png","107-puentealtoeyzag.png","114-catedral.png","115-ventanopresencialfontova.png",
			"122-noutilizar.png","126-vivaceta.png","132-lacisternas.png","133-factoria.png",
			"136-tottusmaipupajarito.png","148-apptottus.png","208-quillota.png","212-penalolen.png","213-vinadelmarsantajulia.png",
			"220-maitencillo.png","304-talca.png","312-losangelesalemania.png","313-curiconorte.png","314-linares.png",
			"315-tottusangol.png","403-bodegamelipilla.png","404-bodegasanantonio.png","405-cdpuertomadero.png","406-bodegalanegraantf.png",
			"411-cdfrutasyverduras.png","414-centroproducciontalagantecordillera.png","415-centroproduccionsanantonio.png",
			"416-centroproduccioncolina.png","418-cdtopfrio","421-noutilizar","424-centroproduccionpuentealto.png",
            "425-cppanaderiapzaoeste.png","426-cppanaderiaptealto.png","428-casapastas.png","431-cdctverde.png",
			"499-adm.centraltalagenta.png","502-antofagastaii.png","508-noutilizar.png","511-vallenar.png","9907-cttransportistavtaverde.png"]

#tiendas = ["101-SAN BERNANDO PLAZA","102-SAN BERNARDO ESTACION","103-PUENTE ALTO","104-NATANIEL","105-PEDRO FONTOVA","106-PLAZA OESTE",
			#"107-PUENTE ALTO EYZAG.","108-LA FLORIDA","109-KENNEDY","110-COLINA","111-ALAMEDA","112-EL BOSQUE","113-PASEO PUENTE","114-CATEDRAL",
			#"115-VENTA NO PRESENCIAL FONTOVA","116-HUECHURABA","117-TT MALL PLAZA TOBALABA","118-VICUNA MACKENNA","119-TOTTUS EL RODEO LO BARNECHEA",
			#"120-VITACURA","121-PLAZA EGANA","122-NO UTILIZAR","123-MP LOS DOMINICOS","124-WALKER MARTINEZ","125-CHAMISERO","126-VIVACETA",
			#"127-CIUDAD EMPRESARIAL","128-CERRO BLANCO RECOLETA","129-QUILICURA","130-VITACURA ALDERETE","131-PIEDRA ROJA","132-LA CISTERNAS",
			#"133-FACTORIA","136-TOTTUS MAIPU PAJARITO","137-ESCUELA MILITAR","147-TIENDA GRIS PENALOLEN","148-APP TOTTUS","201-EL MONTE","202-TALAGANTE PLAZA",
			#"203-PENAFLOR","204-MELIPILLA","205-SAN ANTONIO","206-TALAGANTE CORDILLERA","207-LA CALERA","208-QUILLOTA","209-PADRE HURTADO","210-LLOLLEO",
			#"211-SAN FELIPE","212-PENALOLEN","213-VINA DEL MAR SANTA JULIA","214-VINA DEL MAR","215-QUILPUE","216-LAS PALMAS QUILLOTA",
			#"218-CON CON MANANTIALES","219-RENACA","220-MAITENCILLO","221-LOS ANDES","301-BUIN","302-RENGO","303-SAN FERNANDO","304-TALCA",
			#"305-MACHALI","306-LOS ANGELES","307-EL TREBOL TALCAHUANO","308-RANCAGUA CENTRO","309-TOTTUS BIO BIO","310-CHILLAN","311-TALCA COLIN",
			#"312-LOS ANGELES ALEMANIA","313-CURICO NORTE","314-LINARES","315-TOTTUS ANGOL","408-BOD. ESTA.CENTRAL (PUDAHUEL)","409-CD PRODUCCION PLAZA OESTE",
			#"410-CD PROD PLATOS PREP. PIZZA","413-CENTRO PRODUCCION PLAZA OESTE","414-CENTRO PRODUCCION TALAGANTE CORDILLERA",
			#"415-CENTRO PRODUCCION SAN ANTONIO","416-CENTRO PRODUCCION COLINA","420-CD PESO VARIABLE FIAMBRERIA-QUESOS","424-CENTRO PRODUCCION PUENTE ALTO",
			#"425-CP PANADERIA PZA OESTE","426-CP PANADERIA PTE ALTO","427-CP MULTIFRIGO","428-CASA PASTAS","431-CD CT VERDE","499-ADM. CENTRAL TALAGENTA",
			#"501-ANTOFAGASTA MALL","502-ANTOFAGASTA II","503-CALAMA MALL","504-CALAMA CENTRO","505-OVALLE","506-COPIAPO","507-TOTTUS MP COPIAPO",
			#"508-NO UTILIZAR","509-COQUIMBO TIERRAS BLANCAS","510-TOTTUS BALMACEDA LA SERENA","511-VALLENAR"]

#imgs_tiendas = ["Tienda.png","101-sanbernandoplaza.png","102-sanbernardoestacion.png","103-puentealto.png","104-nataniel.png","105-pedrofontova.png","106-plazaoeste.png",
			#"107-puentealtoeyzag.png","108-laflorida.png","109-kennedy.png","110-colina.png","111-alameda.png","112-elbosque.png","113-paseopuente.png",
			#"114-catedral.png","115-ventanopresencialfontova.png","116-huechuraba.png","117-ttmallplazatobalaba.png","118-vicunamackenna.png",
			#"119-tottuselrodeolobarnechea.png","120-vitacura.png","121-plazaegana.png","122-noutilizar.png","123-mplosdominicos.png","124-walkermartinez.png",
			#"125-chamisero.png","126-vivaceta.png","127-ciudadempresarial.png","128-cerroblancorecoleta.png","129-quilicura.png","130-vitacuraalderete.png",
			#"131-piedraroja.png","132-lacisternas.png","133-factoria.png","136-tottusmaipupajarito.png","137-escuelamilitar.png","147-tiendagrispenalolen.png",
			#"148-apptottus.png","201-elmonte.png","202-talaganteplaza.png","203-penaflor.png","204-melipilla.png","205-sanantonio.png",
			#"206-talagantecordillera.png","207-lacalera.png","208-quillota.png","209-padrehurtado.png","210-llolleo.png","211-sanfelipe.png",
			#"212-penalolen.png","213-vinadelmarsantajulia.png","214-vinadelmar.png","215-quilpue.png","216-laspalmasquillota.png","218-conconmanantiales.png",
			#"219-renaca.png","220-maitencillo.png","221-losandes.png","301-buin.png","302-rengo.png","303-sanfernando.png","304-talca.png",
			#"305-machali.png","306-losangeles.png","307-eltreboltalcahuano.png","308-rancaguacentro.png","309-tottusbiobio.png","310-chillan.png",
			#"311-talcacolin.png","312-losangelesalemania.png","313-curiconorte.png","314-linares.png","315-tottusangol.png","408-bodestacentral(pudahuel).png",
			#"409-cdproduccionplazaoeste.png","410-cdprodplatospreppizza.png","413-centroproduccionplazaoeste.png","414-centroproducciontalagantecordillera.png",
                        #"415-centroproduccionsanantonio.png","416-centroproduccioncolina.png","420-cdpesovariablefiambreriaquesos.png","424-centroproduccionpuentealto.png",
                        #"425-cppanaderiapzaoeste.png","426-cppanaderiaptealto.png","427-cpmultifrigo.png","428-casapastas.png","431-cdctverde.png",
			#"499-adm.centraltalagenta.png","501-antofagastamall.png","502-antofagastaii.png","503-calamamall.png","504-calamacentro.png","505-ovalle.png",
			#"506-copiapo.png","507-tottusmpcopiapo.png","508-noutilizar.png","509-coquimbotierrasblancas.png","510-tottusbalmacedalaserena.png",
			#"511-vallenar.png"]

def jerarquia_method():
    image_click("Jerarquia.png")
    image_click("Division.png")
    mouse_move(200,0)
    click()
    time_wait(500)
    for x in range(int(AVANZAR)):
        press(DOWN)
    press(ENTER)
    image_click("Ok.png")

obj = TRIO()
obj.PORTAL = "TOTTUS"
obj.tiendas = tiendas
obj.imgs_tiendas = imgs_tiendas
obj.sku_num = 1 
obj.pop_up = False
obj.jerarquia_procedure = jerarquia_method
if EXTRA != 'none':
    obj.special_download = EXTRA
if '+' in RUT_EMPRESA:
    obj.rut = RUT_EMPRESA.split("+")
else:
    obj.rut = RUT_EMPRESA
obj.fecha1 = date_to_string(subtract_days(today(),get_weekday_as_int()),"%Y%m%d")
obj.fecha2 = date_to_string(previous_day(today()),"%Y%m%d")
obj.run()
