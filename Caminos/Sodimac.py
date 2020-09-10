load_template("/Sikulix/TRIO.py")

set_imagepath("/Sikulix/Imgs/Sodimac/")
set_download_directory("/home/seluser/Downloads/")
set_screenshot_directory("/home/seluser/Screenshots/")

tiendas = ["ACCESORIOS DE AUTOMOVILES", "ARRIENDO HERRAMIENTA IMP TALCA", "ARRIENDO HERRAMIENTAS IMP MAIPU", "ARRIENDO HERRAMIENTAS IMP PUERTO MONTT", 
			"ARRIENDO HERRAMIENTAS IMP CONCEPCION", "ARRIENDO HERRAMIENTA IMP HUECHURABA", "ARRIENDO HERRAMIENTAS IMP LA SERENA", 
			"ARRIENDO HERRAMIENTAS IMP MAPOCHO",  "ARRIENDO HERRAMIENTAS IMP RANCAGUA", "ARRIENDO HERRAMIENTAS IMP RENACA", 
			"ARRIENDO HERRAMIENTAS IMP SAN BERNARDO", "ARRIENDO HERRAMIENTAS IMP SANTA ROSA", "ARRIENDO HERRAMIENTAS IMP TEMUCO",
            "ARRIENDO HERRAMIENTAS IMP VALPARAISO", "ARRIENDO HERRAMIENTAS IMP VESPUCIO", "BO CENTRO DE DISTRIBUICION DE PLANTAS HIJUELAS", 
			"BASE NAVAL TALCAHUANO", "CO 03 VINA DEL MAR", "CO 21 CANTAGALLO", "CO 25 VICUNA MACKENNA", "CO 26 RANCAGUA", 
			"CO 29 VALPARAISO", "CO 30 TALCAHUANO", "CO 40 ANTOFAGASTA", "CO 48 VENTA BODEGA","CO 60 VALLENAR","CO 65 LA FLORIDA", 
			"CO 87 HUECHURABA", "CO TEMUCO CAUPOLICAN", "CAR CENTER QUILIN","CARPA CONSTITUCION", "CARPA MALL PLAZA CONCEPCION", "CARPA SAN PEDRO DE LA PAZ", 
			"CASA INTELIGENTE", "E-COMMERCE", "EX-HC 741 INDEPENDENCIA", "EL ABRA", "ESCUELA CAJEROS SANTIAGO", "ESTUDIO FOTOGRAFICO SANTIAGO",
			"EXPO MEGACENTER", "EXPORTACIONES", "FAENA MINERA MICHILLA", "GC.BANOS", "HC 02 LOS CARRERAS", "HC 04 LA CALERA", 
			"HC 05 ANTOFAGASTA", "HC 07 OSORNO", "HC 09 LOS ANGELES", "HC 11 IQUIQUE", "HC 12 SAN MIGUEL", "HC 13 CHILOE", 
			"HC 16 SAN FELIPE", "HC 19 VALDIVIA", "HC 20 VINA DEL MAR", "HC 23 SAN BERNARDO", "HC 24 PUNTA ARENAS", "HC 27 CALAMA", 
			"HC 32 ARICA", "HC 33 NUNOA LA REINA", "HC 34 LAS CONDES", "HC 35 CURICO", "HC 37 COYHAIQUE", "HC 39 LA SERENA", "HC 41 PUERTO MONTT", 
			"HC 43 TALCA", "HC 44 TEMUCO CAUTIN", "HC 45 HOMY PARQUE ARAUCO", "HC 51 CHILLAN", "HC 54 NUEVA LA FLORIDA", "HC 55 LINARES", 
            "HC 57 COPIAPO", "HC 58 ANGOL", "HC 59 VILLARICA", "HC 63 HUECHURABA", "HC 66 NUBLE", "HC 67 LA REINA", "HC 70 PASEO ESTACION", 
			"HC 713 SAN ANTONIO", "HC 714 MELIPILLA", "HC 716 SANTA CRUZ", "HC 723 QUILICURA", "HC 724 BIO BIO RIBERA NORTE", 
			"HC 725 QUINTA VERGARA", "HC 726 TOBALABA", "HC 727 TALCA PONIENTE", "HC 728 ALTO HOSPICIO", "HC 729 OVALLE", 
			"HC 730 CORONEL", "HC 734 QUILLOTA", "HC 735 HOMY PLAZA EGANA", "HC 737 TALAGANTE", "HC 738 LOS DOMINICOS", "HC 739 COPIAPO CORDILLERA", 
			"HC 74 EL BOSQUE", "HC 743 ANTOFAGASTA II", "HC 745 INDEPENDENCIA", "HC 746 QUILIN", "HC 747 TEMUCO LOS PABLOS","HC 748 CHICUREO EXPRESS","HC 75 PUENTE ALTO", 
                        "HC 79 PARQUE ARAUCO", 
			"HC 81 CONCEPCION", "HC 83 RANCAGUA", "HC 88 MAIPU", "HC 90 QUILPUE", "HC 93 ELTREBOL", "HC 95 LA FLORIDA-VESPUCIO", "HC 96 CERRILLOS", 
			"HC 97 RENACA", "HC 98 COQUIMBO", "HC EL QUISCO", "HC LA SERENA II", "HC SAN FERNANDO", "HO 732 PLAZA VESPUCIO", "HO 733 PLAZA OESTE", 
			"KV ANGOL", "KV HUECHURABA", "KV ANTOFAGASTA", "KV ARICA", "KV CERRILLOS", "KV COPIAPO","KV PUERTO MONTT", "KV PUNTA ARENAS 1", 
			"KV 823 VIRTUAL REMODELACION CERRILLOS", "KV CALAMA","KV EL BELLOTO",  "KV MELIPILLA", "KV OSORNO", "KV RENACA", "KV VALLENAR", 
			"KV VILLARRICA", "KV VILLARRICA-2", "LL HC SANTA CRUZ", "LL PATIO HC- ANGOL", "LL RENACA", "LL T ARICA", "LL T ANTOFAGASTA", "LL T COPIAPO", 
            "LL T COYHAIQUE", "LL T HUECHURABA", "LLT LOS ANGELES", "LLT OSORNO", "LLT PLAZA OESTE", "LL T PUERTO MONTT", "LL T PUNTA ARENAS", 
			"LL T SAN FELIPE", "LABORATORIO CUTCASE-L_A", "LLENANDO HC MELIPILLA", "LLENANDO SAN ANTONIO", "LOGRONO", "OF APOYO A TIENDAS", 
			"OPERACION EL SOLDADO", "OPERACION LOS BRONCES", "PE CON SALDO EN BODEGA", "PUNTO DE RETIRO ALDERETE T", "PUNTO RETIRO COSTANERA CENTER F",
			"PROYECTO CIERRE DE CC28", "PUNTO ENTREGA CHICUREO", "PUNTO ENTREGA OFICINA DE APOYO", "PUNTO RETIRO AHUMADA F",
			"PUNTO RETIRO ALAMEDA M","PUNTO RETIRO ALTO LAS CONDES F", "PUNTO RETIRO ANTOFAGASTA F", "PUNTO RETIRO ARAUCO MAIPU F", 
            "PUNTO RETIRO ARICA F", "PUNTO RETIRO BILBAO T","PUNTO RETIRO BIO-BIO T", "PUNTO RETIRO BUIN T", "PUNTO RETIRO CASTRO F", "PUNTO RETIRO CATEDRAL T", 
			"PUNTO RETIRO CERRILLOS F", "PUNTO RETIRO CERRO BLANCO", "PUNTO RETIRO CHAMISERO T", "PUNTO RETIRO CHILLAN F","PUNTO RETIRO COLINA T", "PUNTO RETIRO CON CON T", 
			"PUNTO RETIRO COPIAPO F", "PUNTO RETIRO COPIAPO LOS CARRERA T", "PUNTO RETIRO CURAUMA T","PUNTO RETIRO CURICO NORTE T", "PUNTO RETIRO DRIVE THRU KENNEDY F",
			"PUNTO RETIRO EL MONTE", "PUNTO RETIRO FALABELLA CALAMA", "PUNTO RETIRO FALABELLA CONCEPCION", "PUNTO RETIRO FALABELLA CURICO", "PUNTO RETIRO FALABELLA LA CALERA",
			"PUNTO RETIRO FALABELLA LOS ANGELES", "PUNTO RETIRO FALABELLA OSORNO", "PUNTO RETIRO FALABELLA OVALLE", "PUNTO RETIRO FALABELLA QUILPUE", "PUNTO RETIRO FALABELLA SAN FELIPE",
			"PUNTO RETIRO FALABELLA SAN FERNANDO", "PUNTO RETIRO FALABELLA TALCA", "PUNTO RETIRO FALABELLA VALDIVIA", "PUNTO RETIRO FALABELLA VINA DEL MAR",
			"PUNTO RETIRO FONTOVA T", 
			"PUNTO RETIRO HUECHURABA T", "PUNTO RETIRO INDEPENDENCIA F", "PUNTO RETIRO IQUIQUE F", "PUNTO RETIRO KENNEDY T","PUNTO RETIRO LA CISTERNA T", 
			"PUNTO RETIRO LA DEHESA F", "PUNTO RETIRO LA FLORIDA T", "PUNTO RETIRO LA SERENA BALMACEDA T","PUNTO RETIRO LA SERENA F", "PUNTO RETIRO LOS ANGELES T", 
			"PUNTO RETIRO LOS DOMINICOS F", "PUNTO RETIRO LOS DOMINICOS M", "PUNTO RETIRO LOS DOMINICOS T", "PUNTO RETIRO LYON F", 
			"PUNTO RETIRO MACHALI T", "PUNTO RETIRO MAITENCILLO T", "PUNTO RETIRO MALL ALAMEDA F", "PUNTO RETIRO MALL COPIAPO F", "PUNTO RETIRO MALL PLAZA ALAMEDA T",
			"PUNTO RETIRO MALL PLAZA ANTOFAGASTA T","PUNTO RETIRO MALL PLAZA COPIAPO T",
			"PUNTO RETIRO MALL PLAZA TOBALABA F", "PUNTO RETIRO MANQUEHUE F", "PUNTO RETIRO MELIPILLA F", 
            "PUNTO RETIRO NATANIEL T", "PUNTO RETIRO OVALLE T", "PUNTO RETIRO PADRE HURTADO T", "PUNTO RETIRO PARQUE ARAUCO F","PUNTO RETIRO PENAFLOR T", 
			"PUNTO RETIRO PIEDRA ROJA T", "PUNTO RETIRO PLAZA EGANA T","PUNTO RETIRO PLAZA EL TREBOL F", "PUNTO RETIRO PLAZA NORTE F","PUNTO RETIRO PLAZA OESTE T", 
			"PUNTO RETIRO PLAZA VESPUCIO", "PUNTO RETIRO PUCON F", "PUNTO RETIRO PUENTE ALTO EYZAGUIRRE", "PUNTO RETIRO PUENTE ALTO T","PUNTO RETIRO PUENTE F", 
			"PUNTO RETIRO PUERTO MONTT F", "PUNTO RETIRO PUNTA ARENAS F", "PUNTO RETIRO QUILICURA T", "PUNTO RETIRO QUILIN T","PUNTO RETIRO QUILLOTA T", "PUNTO RETIRO QUILPUE T", 
			"PUNTO RETIRO RANCAGUA F", "PUNTO RETIRO RENACA T","PUNTO RETIRO RENGO T", "PUNTO RETIRO SAN ANTONIO T", "PUNTO RETIRO SAN BERNARDO ESTACION T","PUNTO RETIRO SAN BERNARDO F", "PUNTO RETIRO SAN FERNANDO T", 
			"PUNTO RETIRO TALAGANTE T", "PUNTO RETIRO TALCA ALAMEDA T", "PUNTO RETIRO TEMUCO F", "PUNTO RETIRO TOTTUS ANTOFAGASTA CENTRO", "PUNTO RETIRO TOTTUS CALAMA",
			"PUNTO RETIRO TOTTUS CHILLAN", "PUNTO RETIRO TOTTUS CIUDAD EMPRESARIAL", "PUNTO RETIRO TOTTUS COQUIMBO", "PUNTO RETIRO TOTTUS EL BOSQUE", "PUNTO RETIRO TOTTUS LA SERENA", 
			"PUNTO RETIRO TOTTUS LOS ANDES", "PUNTO RETIRO TOTTUS SAN BERNARDO PLAZA", "PUNTO RETIRO TOTTUS SANTA JULIA RENACA", "PUNTO RETIRO TOTTUS TALAGANTE CORD", "PUNTO RETIRO TOTTUS TALCA COLIN",
			"PUNTO RETIRO TOTTUS TREBOL", "PUNTO RETIRO TOTTUS VIVACETA", "PUNTO RETIRO TOTTUS WALKER MARTINEZ",
			"PUNTO RETIRO VALLENAR T", "PUNTO RETIRO VALPARAISO F", "PUNTO RETIRO VICUNA MACKENNA T", 
            "PUNTO RETIRO VITACURA T", "PUNTO RETIRO LA PLAZA EGANA F", "PUNTO DE ENTREGA BUIN", "PUNTO DE ENTREGA MAINTECILLO", "PUNTO DE ENTREGA PUCON", 
            "PUNTO DE RETIRO MANQUEHUE F", "RECONSTRUCTOR CAUQUENES", "REMODELACION HC-NUBLE","TVIRTUAL CONTROL PROVEEDORES",            
            "TRIANG. SAN ANTONIO", "USE 06 ANTOFAGASTA", "USE 22 CONCEPCION", "USE 52 SANTIAGO", "USE 73 VINA DEL MAR"]

imgs_tiendas = ["Tienda.png","AccesoriosDeAutomoviles.png","ArriendoHerramientaIMPTalca.png","ArriendoHerramientasIMPMaipu.png","ArriendoHerramientasIMPPuertoMontt.png",
			"ArriendoHerramientasIMPConcepcion.png","ArriendoHerramientasIMPHuechuraba.png", "ArriendoHerramientasIMPLaSerena.png",
			"ArriendoHerramientasIMPMapocho.png","ArriendoHerramientasIMPRancagua.png","ArriendoHerramientasIMPRenaca.png",
			"ArriendoHerramientasIMPSanBernardo.png","ArriendoHerramientasIMPSantaRosa.png","ArriendoHerramientasIMPTemuco.png",
			"ArriendoHerramientasIMPValparaiso.png","ArriendoHerramientasIMPVespucio.png","BOCentroDeDistribuicionDePlantasHijuelas.png",
			"BaseNavalTalcahuano.png","CO03VinaDelMar.png","CO21Cantagallo.png","CO25VicunaMackenna.png","CO26Rancagua.png","CO29Valparaiso.png",
			"CO30Talcahuano.png","CO40Antofagasta.png","CO48VentaBodega.png","CO60Vallenar.png","CO65LaFlorida.png","CO87Huechuraba.png",
			"COTemucoCaupolican.png","carcenterquilin.png","CarpaConstitucion.png", "CarpaMallPlazaConcepcion.png","CarpaSanPedroDeLaPaz.png","CasaInteligente.png",
			"E-Commerce.png","EX-HC741Independencia.png","ElAbra.png","EscuelaCajerosSantiago.png", "EstudioFotograficoSantiago.png", 
			"ExpoMegaCenter.png","Exportaciones.png","FaenaMineraMichilla.png","GC.Banos.png","HC02LosCarreras.png","HC04LaCalera.png",
			"HC05Antofagasta.png","HC07Osorno.png","HC09LosAngeles.png","HC11Iquique.png","HC12SanMiguel.png","HC13Chiloe.png",
			"HC16SanFelipe.png","HC19Valdivia.png","HC20VinaDelMar.png","HC23SanBernardo.png","HC24PuntaArenas.png","HC27Calama.png",
			"HC32Arica.png","HC33NunoaLaReina.png","HC34LasCondes.png","HC35Curico.png","HC37Coyhaique.png","HC39LaSerena.png","HC41PuertoMontt.png",
			"HC43Talca.png","HC44TemucoCautin.png","HC45HomyParqueArauco.png","HC51Chillan.png","HC54NuevaLaFlorida.png","HC55Linares.png",
			"HC57Copiapo.png","HC58Angol.png","HC59VillaRica.png","HC63Huechuraba.png","HC66Nuble.png","HC67LaReina.png","HC70PaseoEstacion.png",
			"HC713SanAntonio.png","HC714Melipilla.png","HC716SantaCruz.png","HC723Quilicura.png","HC724BioBioRiberaNorte.png","HC725QuintaVergara.png",
			"HC726Tobalaba.png","HC727TalcaPoniente.png","HC728AltoHospicio.png","HC729Ovalle.png","HC730Coronel.png","HC734Quillota.png", 
			"HC735HomyPlazaEgana.png","HC737Talagante.png","HC738LosDominicos.png","HC739CopiapoCordillera.png","HC74ElBosque.png","HC743AntofagastaII.png",
			"HC745Independencia.png","HC746Quilin.png","HC747TemucoLosPablos.png","HC748ChicureoExpress.png","HC75PuenteAlto.png","HC79ParqueArauco.png",
                        "HC81Concepcion.png","HC83Rancagua.png","HC88Maipu.png",
			"HC90Quilpue.png","HC93ElTrebol.png","HC95LaFlorida-Vespucio.png","HC96Cerrillos.png","HC97Renaca.png","HC98Coquimbo.png","HCElQuisco.png",
			"HCLaSerenaII.png","HCSanFernando.png","HO732PlazaVespucio.png","HO733PlazaOeste.png","KVAngol.png","KVHuechuraba.png","KVAntofagasta.png",
			"KVArica.png","KVCerrillos.png","KVCopiapo.png","KVPuertoMontt.png","KVPuntaArenas1.png","KV823VirtualRemodelacionCerrillos.png","KVCalama.png",
			"KVElBelloto.png","KVMelipilla.png","KVOsorno.png","KVRenaca.png","KVVallenar.png","KVVillarrica.png","KVVillarrica.png","LLHCSantaCruz.png",
			"LLPatioHC-Angol.png","LLRenaca.png","LLTArica.png","LLTAntofagasta.png","LLTCopiapo.png","LLTCoyhaique.png","LLTHuechuraba.png",
			"LLTLosAngeles.png","LLTOsorno.png","LLTPlazaOeste.png","LLTPuertoMontt.png","LLTPuntaArenas.png","LLTSanFelipe.png","LaboratorioCutCase-L_A.png",
			"LlenadoHCMelipilla.png","LlenadoSanAntonio.png","Logrono.png","OfApoyoATiendas.png","OperacionElSoldado.png","OperacionLosBronces.png",
			"PeConSaldoEnBodega.png", "PuntoDeRetiroAldereteT.png","PuntoRetiroCostaneraCenterF.png","ProyectoCierredeCC28.png",
			"PuntoEntregaChicureo.png","PuntoEntregaOficinaDeApoyo.png","PuntoRetiroAhumadaF.png","PuntoRetiroAlamedaM.png","PuntoRetiroAltoLasCondesF.png",
			"PuntoRetiroAntofagastaF.png","PuntoRetiroAraucoMaipuF.png","PuntoRetiroAricaF.png","PuntoRetiroBilbaoT.png","PuntoRetiroBio-BioT","PuntoRetiroBuinT.png",
			"PuntoRetiroCastroF.png","PuntoRetiroCatedralT.png","PuntoRetiroCerrillosF.png","PuntoRetiroCerroBlancoT.png","PuntoRetiroChamiseroT.png","PuntoRetiroChillanF.png",
			"PuntoRetiroColinaT.png","PuntoRetiroConConT.png", "PuntoRetiroCopiapoF.png","PuntoRetiroCopiapoLosCarreraT.png","PuntoRetiroCuraumaT.png","PuntoRetiroCuricoNorteT.png",
			"PuntoRetiroDriveThruKennedyF.png","PuntoRetiroElMonteT.png","PuntoRetiroFalabellaCalama.png","PuntoRetiroFalabellaConcepcion.png","PuntoRetiroFalabellaCurico.png","PuntoRetiroFalabellaLaCalera.png",
			"PuntoRetiroFalabellaLosAngeles.png","PuntoRetiroFalabellaOsorno.png","PuntoRetiroFalabellaOvalle.png","PuntoRetiroFalabellaQuilpue.png","PuntoRetiroFalabellaSanFelipe.png","PuntoRetiroFalabellaSanFernando.png",
			"PuntoRetiroFalabellaTalca.png","PuntoRetiroValdivia.png","PuntoRetiroFalabellaVinaDelMar.png",
			"PuntoRetiroFontovaT.png","PuntoRetiroHuechurabaT.png","PuntoRetiroIndependenciaF.png","PuntoRetiroIquiqueF.png","PuntoRetiroKennedyT","PuntoRetiroLaCisternaT.png",
			"PuntoRetiroLaDehesaF.png","PuntoRetiroLaFloridaT.png","PuntoRetiroLaSerenaF.png","PuntoRetiroLaSerenaBalmacedaT.png","PuntoRetiroLosAngelesT.png","PuntoRetiroLosDominicosF.png",
			"PuntoRetiroLosDominicosM.png","PuntoRetiroLosDominicosT.png","PuntoRetiroLyonF.png", "PuntoRetiroMachaliT.png","PuntoRetiroMaitencilloT.png",
			"PuntoRetiroMallAlamedaF.png","PuntoRetiroMallCopiapoF.png","PuntoRetiroMallPlazaAlamedaT.png","PuntoRetiroMallPlazaAntofagastaT.png","PuntoRetiroMallPlazaCopiapoT.png",
                        "PuntoRetiroMallPlazaTobalabaF.png","PuntoRetiroManquehueF.png",
			"PuntoRetiroMelipillaF.png","PuntoRetiroNatanielT.png","PuntoRetiroOvalleT.png","PuntoRetiroPadreHurtadoT.png","PuntoRetiroParqueAraucoF.png",
			"PuntoRetiroPenaflorT.png","PuntoRetiroPiedraRojaT.png","PuntoRetiroPlazaEganaT.png","PuntoRetiroPlazaElTrebolF.png","PuntoRetiroPlazaNorteF.png","PuntoRetiroPlazaOesteT.png",
			"PuntoRetiroPlazaVespucio.png","PuntoRetiroPuconF.png","PuntoRetiroPuenteAltoEyzaguirre.png","PuntoRetiroPuenteAltoT.png","PuntoRetiroPuenteF.png",
			"PuntoRetiroPuertoMonttF.png","PuntoRetiroPuntaArenasF.png","PuntoRetiroQuilicuraT.png","PuntoRetiroQuilinT.png","PuntoRetiroQuillotaT.png","PuntoRetiroQuilpueT.png","PuntoRetiroRancaguaF.png",
			"PuntoRetiroRenacaT.png","PuntoRetiroRengoT.png","PuntoRetiroSanAntonioT.png", "PuntoRetiroSanBernardoEstacionT.png","PuntoRetiroSanBernardoF.png","PuntoRetiroSanFernandoT.png","PuntoRetiroTalaganteT.png",
			"PuntoRetiroTalcaAlamedaT.png",
			"PuntoRetiroTemucoF.png","PuntoRetiroTottusAntogastaCentro.png","PuntoRetiroTottusCalama.png","PuntoRetiroTottusChillan.png","PuntoRetiroTottusCiudadEmpresarial.png","PuntoRetiroTottusCoquimbo.png",
			"PuntoRetiroTottusElBosque.png","PuntoRetiroTottusLaSerena.png","PuntoRetiroTottusLosAndes.png","PuntoRetiroTottusSanBernardoPlaza.png","PuntoRetiroTottusSantaJuliaRenaca.png","PuntoRetiroTottusTalaganteCord.png",
			"PuntoRetiroTottusTalcaColin.png","PuntoRetiroTottusTrebol.png","PuntoRetiroTottusVivaceta.png","PuntoRetiroTottusWalkerMartinez.png",
			"PuntoRetiroVallenarT.png","PuntoRetiroValparaisoF.png","PuntoRetiroVicunaMackennaT.png","PuntoRetiroVitacuraT.png",
			"PuntoRetiroLaPlazaEganaF.png","PuntoDeEntregaBuin.png", "PuntoDeEntregaMaintencillo.png","PuntoDeEntregaPucon.png","PuntoDeRetiroManquehueF.png",
			"ReconstructorCauquenes.png","RemodelacionHC-Nuble.png","TVirtualControlProveedores.png",
            "Triang.SanAntonio.png","USE06Antofagasta.png", "USE22Concepcion.png","USE52santiago.png","USE73VinaDdelMar.png"]

def jerarquia_method(): 
    image_click("Jerarquia.png")
    if not image_appeared("Departamento.png"):
        image_hover("Ventas.png")
        image_click("Analisis.png")
        image_click("Jerarquia.png")
        image_click("Departamento.png")
    else:
        image_click("Departamento.png")
    press(TAB)
    for x in range(int(AVANZAR)):
        press(DOWN)
    image_click("Ok.png")

def multi_run():
    obj.login()
    obj.get_to_dashboard()
    obj.dashboard()
    if not matrix_get("SSHOT_1"):
        obj.screenshots()
    if not matrix_get("SSHOT_2"):
        obj.screenshots()
    if not matrix_get("DOWNLOAD_STARTED"):
        obj.get_to_dashboard()
        obj.dashboard()
    if get_downloads_count() < 144:
        obj.get_files(43,get_downloads_count(),int(NUM_LOCALES)-17)
    elif get_downloads_count() < 168:
        obj.get_files(17,get_downloads_count()-144,int(NUM_LOCALES)-77)
    elif get_downloads_count() < 176:
        obj.get_files(279,get_downloads_count()-168,int(NUM_LOCALES)-85)
    elif get_downloads_count() < 178:
        obj.get_files(34,get_downloads_count()-176,int(NUM_LOCALES)-88)
    if get_downloads_count() != int(NUM_LOCALES)*2:
        obj.run()
    else:
        tcp_send("FINISH0")
        close_explorer()

obj = TRIO()
obj.PORTAL = "SODIMAC"
obj.tiendas = tiendas
obj.pop_up = False
obj.jerarquia_procedure = jerarquia_method
obj.imgs_tiendas = imgs_tiendas
obj.sku_num = 6
if EXTRA != 'none':
    obj.special_download = EXTRA
else:
    obj.run = multi_run
if '+' in RUT_EMPRESA:
    obj.rut = RUT_EMPRESA.split("+")
else:
    obj.rut = RUT_EMPRESA
obj.fecha1 = date_to_string(subtract_days(today(),get_weekday_as_int()),"%Y%m%d")
obj.fecha2 = date_to_string(previous_day(today()),"%Y%m%d")
print(imgs_tiendas[279])
obj.run()
