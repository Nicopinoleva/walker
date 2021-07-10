import shutil

set_imagepath("/Sikulix/Imgs/Walmart/")
set_download_directory("/home/seluser/Downloads/")
set_screenshot_directory("/home/seluser/Screenshots/")

img_num = 0
spanish_special = False
text_sshot = SSHOT_TXT.split(",")
files_downloaded = int(matrix_get("FILES_DOWNLOADED"))
imgs_language = ["Spanish.png", "Mis_reportes.png", "Buscar.png", "Iniciar_busqueda.png", "Modificar.png", "Tiempo.png",
			"Rango_1.png", "Fecha_pos.png", "Esta_entre.png", "Modificar_2.png", "Fecha_1.png", "Y.png", 
                        "Submitir.png" , "Renombre.png", "Ejecutar.png", "Solicitud_submitida.png", "Estado.png", 
                        "Error_datos.png", "Formateo.png", "English.png", "My_reports.png", "Search.png", "Beggin_search.png", "Modify.png", 
                        "Times.png", "Range_1.png", "Pos_date.png", "Is_between.png", "Modify_2.png", "Date_1.png", "And.png", 
                        "Submit.png", "Rename.png", "Run_now.png", "Query_submitted.png", "Status.png", "Data_error.png", "Formater.png"]
fechas = [[date_to_string(previous_day(today()),"%Y%m%d"), date_to_string(subtract_days(today(),7),"%Y%m%d"), date_to_string(get_first_day_of_month(previous_day(today())),"%Y%m%d"),
          date_to_string(get_previous_month(previous_day(today())),"%Y%m%d"), date_to_string(get_previous_month(previous_day(today())),"%Y%m") + 
          str(get_last_day_of_month(get_previous_month(previous_day(today()))))],
          [date_to_string(previous_day(today()),"%m-%d-%Y"), date_to_string(subtract_days(today(),7),"%m-%d-%Y"), 
          date_to_string(get_first_day_of_month(previous_day(today())),"%m-%d-%Y"), date_to_string(get_previous_month(previous_day(today())),"%m-%d-%Y"), 
          date_to_string(get_previous_month(previous_day(today())),"%m") + "-" + 
          str(get_last_day_of_month(get_previous_month(previous_day(today())))) + "-" + date_to_string(previous_day(today()),"%Y")]]
          #1 día atrás,7 días atrás,primer día del mes actual,primer día del mes anterior,último dia mes anterior
files_names = ["{}_{}_{}_{}_{}_{}_{}".format(RUT_EMPRESA,fechas[0][1],fechas[0][0],NOMBRE_EMPRESA,"LIDER","B2B","DIA"),
        "{}_{}_{}_{}_{}_{}_{}_{}_{}".format(RUT_EMPRESA,fechas[0][0],fechas[0][0],fechas[0][0],NOMBRE_EMPRESA,"LIDER","B2B","DIA","INV"),
        "{}_{}_{}_{}_{}_{}_{}_{}_{}".format(RUT_EMPRESA,fechas[0][0],fechas[0][0],fechas[0][0],NOMBRE_EMPRESA,"LIDER","B2B","DIA","CD"),
        "{}_{}_{}_{}_{}_{}_{}_{}".format(RUT_EMPRESA,fechas[0][2],fechas[0][0],NOMBRE_EMPRESA,"LIDER","B2B","MENSUAL","SSHOTS"),
        "{}_{}_{}_{}_{}_{}_{}_{}".format(RUT_EMPRESA,fechas[0][3],fechas[0][4],NOMBRE_EMPRESA,"LIDER","B2B","MENSUAL","SSHOTS")]

def login():
    global spanish_special
    open_explorer(URL_PORTAL)
    image_click("Username.png")
    time_wait(5000)
    type(USERNAME)
    press(TAB)
    time_wait(5000)
    type(PASSWORD)
    press(TAB)
    press(ENTER)
    time_wait(5000)
    result = image_wait_multiple("Credentials.png","Credenciales.png","Blocked.png","Expired.png","Expirada.png","Retail.png","Retail_new.png")
    if result in ["Credentials.png","Credenciales.png"]:
        send_action_simple(1,1)
        sname = "{}_{}".format("LOGIN", "WALMART")
        screenshot_save(sname)
        tcp_send("SNDPIC1 /home/seluser/Screenshots/" + sname + ".png")
        tcp_send("FINISH1")
        abort("Credenciales erroneas")
    elif result in ["Expired.png","Expirada.png"]:
        send_action_simple(1,7)
        sname = "{}_{}".format("LOGINEXP", "WALMART")
        screenshot_save(sname)
        tcp_send("SNDPIC1 /home/seluser/Screenshots/" + sname + ".png")
        tcp_send("FINISH7")
        abort("Credenciales expiradas")
    elif result in["Retail.png","Retail_new.png"]:
        if not matrix_get("LOGIN_CORRECT"):
            send_action_simple(1,0)
            matrix_set("LOGIN_CORRECT",True)
    elif result == "Blocked.png":
        send_action_simple(1,15)
        sname = "{}_{}".format("LOGINBLQ", "WALMART")
        screenshot_save(sname)
        tcp_send("SNDPIC1 /home/seluser/Screenshots/" + sname + ".png")
        tcp_send("FINISH15")
        abort("Credenciales bloqueadas")
    else:
        log("INFO", "Portal didn't load")
        send_action_simple(9,3)
        tcp_send("FAILED3")
        abort()
    time_wait(2000)
    result = image_wait_multiple("Apps.png","Aplicaciones.png","Apps_new_EN.png","Apps_new_ES.png")
    if result in ["Apps_new_EN.png","Apps_new_ES.png"]:
        new_view(result)
        language_check()
    else:
        language_check()
        if image_appeared("Aplicaciones.png"):
            spanish_special = True
            image_click("Aplicaciones.png")
        else:
            image_click("Apps.png")
        time_wait(2000)
        if not image_appeared("Decision_support.png"):
            press_with_ctr("f")
            type("Soporte") 
            press_with_ctr("a")
            press(DELETE)
            time_wait(2000)
            if image_appeared("Soporte_decision.png"):
                image_click("Soporte_decision.png")
            else:
                log("INFO", "Portal didn't load")
                send_action_simple(9,3)
                tcp_send("FAILED3")
                abort()
        else:
            image_click("Decision_support.png")

def language_check():
    global img_num
    time_wait(5000)
    result = image_wait_multiple("Spanish.png","Spanish2.png","English.png","English2.png")
    if result in ["Spanish.png","Spanish2.png"]:
        log("INFO", "Language: Spanish")
        send_action_simple(9,0)
    elif result in ["English.png","English2.png"]:
        log("INFO", "Language: English")
        img_num = 19
        send_action_simple(9,0)
    else:
        log("INFO", "Language could not be identified")
        send_action_simple(9,3)
        tcp_send("FAILED3")
        abort()

def new_view(img):
    image_click(img)
    image_click("Decision_support_new.png")

def run_cycle():
    for x in range(int(NUM_LOCALES)+int(NUM_SSHOTS)):
        if not matrix_get("FILE_" + str(x+1) + "_RUNNING"):
            get_to_dashboard(x)
    if not matrix_get("ALL_RUNNING"):
        matrix_set("ALL_RUNNING",True)
        tcp_send("YAPEDI"+str(int(NUM_LOCALES)+int(NUM_SSHOTS)))
        log("INFO", "Files running, sleeping...")
        close_explorer()
        manual_finish()

def get_to_dashboard(file_to_run):
    image_click(imgs_language[img_num + 1])#Mis_reportes.png
    image_click(imgs_language[img_num + 2])#Buscar.png
    image_click(imgs_language[img_num + 3])#Iniciar_busqueda.png
    if file_to_run < 2:
        type("RP Vta Diaria")
        press(ENTER)
        press_with_ctr("a")
        press(DELETE)
        press_with_ctr("f")
        time_wait(5000)
        type("RP Vta Diaria")
        time_wait(2000)
        image_right_click("RP_Vta_Diaria.png")
        dashboard()
        if file_to_run == 0:
            sales_file()
        else:
            stock_CD_file(file_to_run)
    elif file_to_run == 2:
        type("RPRO CD")
        press(ENTER)
        press_with_ctr("a")
        press(DELETE)
        press_with_ctr("f")
        time_wait(5000)
        type("RPRO CD")
        time_wait(2000)
        image_right_click("RPRO_CD.png")
        dashboard()
        stock_CD_file(file_to_run)
    elif file_to_run > 2:
        type("RPRO SS")
        press(ENTER)
        press_with_ctr("a")
        press(DELETE)
        press_with_ctr("f")
        time_wait(5000)
        type("RPRO SS")
        time_wait(2000)
        image_right_click("RPRO_SS.png")
        dashboard()
        screenshot_file(file_to_run)
    file_exec(file_to_run)

def dashboard():
    image_click(imgs_language[img_num + 4])#Modificar.png
    time_wait(5000)
    if spanish_special:
        image_click("Tiempo_special.png")
        image_click("Rango_1_special.png")
        image_double_click("Fecha_pos_special.png")
        image_click("Esta_entre_special.png")
    else:
        image_click(imgs_language[img_num + 5])#Tiempo.png
        image_click(imgs_language[img_num + 6])#Rango_1.png
        image_double_click(imgs_language[img_num + 7])#Fecha_pos.png
        image_click(imgs_language[img_num + 8])#Esta_entre.png
    result = image_wait_multiple("Pos_date_2.png","Fecha_pos_2.png","Fecha_pos_2_EN.png")
    if result == "Pos_date_2.png":
        image_click("Pos_date_2.png")
    elif result == "Fecha_pos_2.png":
        image_click("Fecha_pos_2.png")
    else:
        image_click("Fecha_pos_2_EN.png")
    image_click(imgs_language[img_num + 9])#Modificar_2.png
    image_click(imgs_language[img_num + 10])#Fecha_1.png
    press_with_ctr("a")
    press(DELETE)

def sales_file():
    time_wait(1000)
    type(fechas[1][1])#7 dias atrás formarto mm-dd-yyyy
    press(TAB)
    press(DELETE)
    time_wait(1000)
    type(fechas[1][0])#1 día atrás formamto mm-dd-yyyy
    file_exec_rename(fechas[1][1],fechas[1][0],"_VTA")
    
def stock_CD_file(file_to_run):
    time_wait(1000)
    type(fechas[1][0])#1 día atrás formamto mm-dd-yyyy
    press(TAB)
    press(DELETE)
    time_wait(1000)
    type(fechas[1][0])#1 día atrás formamto mm-dd-yyyy
    if file_to_run == 1:
        file_exec_rename(fechas[1][0],fechas[1][0],"_INV")
    else:
        file_exec_rename(fechas[1][0],fechas[1][0],"_CD")

def screenshot_file(file_to_run):
    time_wait(1000)
    if file_to_run == 3:
        type(fechas[1][2])#primer día del mes actual formato mm-dd-yyyy
        press(TAB)
        press(DELETE)
        time_wait(1000)
        type(fechas[1][0])#1 día atrás formamto mm-dd-yyyy
        file_exec_rename(fechas[1][2],fechas[1][0],"_SS")
    else:
        type(fechas[1][3])#primer día del mes anterior formato mm-dd-yyyy
        press(TAB)
        press(DELETE)
        time_wait(1000)
        type(fechas[1][4])#último día del mes anterior formamto mm-dd-yyyy
        file_exec_rename(fechas[1][3],fechas[1][4],"_SS") 

def file_exec_rename(fecha1,fecha2,file):
    image_click(imgs_language[img_num + 11])#Y.png
    image_click(imgs_language[img_num + 12])#Submitir.png
    image_click(imgs_language[img_num + 13])#Renombre.png
    press_with_ctr("a")
    press(DELETE)
    type(fecha1 + "_" + fecha2 + file)

def file_exec(file_to_run):
    image_click(imgs_language[img_num + 14])#Ejecutar.png//Run_now.png
    result = image_wait_multiple("Error.png",imgs_language[img_num + 15])
    if result == "Error.png":
        send_action_simple(7,3)
        log("INFO", "Portal isn't allowing to run files")
        tcp_send("FINISH5")
        abort()
    elif result == imgs_language[img_num + 15]:
        send_action_simple(3,0,files_downloaded,file_to_run+1)
        time_wait(2000)
        sname = "{}_{}_{}".format("Job","id",str(file_to_run+1))
        screenshot_save_crop(sname,int(text_sshot[0]), int(text_sshot[1]), int(text_sshot[2]), int(text_sshot[3]))
        time_wait(1500)
        tcp_send("SNDPIC1 /home/seluser/Screenshots/" + sname + ".png")
        matrix_set("FILE_" + str(file_to_run+1) + "_RUNNING",True)
    else:
        log("INFO", "File didn't run")
        send_action_simple(3,9,files_downloaded,str(file_to_run+1))
    image_click("Close.png")

def get_files():
    while(True):
        for x in range(int(NUM_LOCALES)+int(NUM_SSHOTS)):
            if matrix_get("FILE_" + str(x+1) + "_RUNNING") and not matrix_get("FILE_" + str(x+1) + "_DOWNLOADED"):
                download(x)
        run_cycle()
        tcp_send("DUERMO"+str(files_downloaded))

def download(file_num):
    global files_downloaded
    image_click(imgs_language[img_num + 16])#Estado.png//Status.png
    image_hover("Close.png")
    image_click("/home/seluser/Screenshots/Job_id_" + str(file_num+1) + ".png")#Job_id_x.png
    time_wait(2000)
    result = image_wait_multiple("Ok_1.png","Ok_2.png")
    if result == "Ok_1.png":
        image_click("Save_file.png")
        image_click("Ok_1.png")
        time_wait(2000)
        type(files_names[file_num])
        press(ENTER)
        files_downloaded +=1
        send_action_simple(4,0,files_downloaded,file_num+1)
        matrix_set("FILE_" + str(file_num+1) + "_DOWNLOADED",True)
        matrix_set("FILES_DOWNLOADED",files_downloaded)
        time_wait(5000)
        if(file_num+1>=4):
            shutil.move("/home/seluser/Downloads/" + files_names[file_num] + ".htm", "/home/seluser/Screenshots/" + files_names[file_num] + ".htm")
            tcp_send("SNDSHO" + str(file_num-2) + " " + str(files_downloaded) + "     '" + files_names[file_num] + ".htm'")
        else:
            tcp_send("SNDFIL" + str(files_downloaded) + "   '/home/seluser/Downloads/" + files_names[file_num] + ".zip'")
        if files_downloaded == int(NUM_LOCALES)+int(NUM_SSHOTS):
            finish()
        if image_appeared(imgs_language[img_num + 16]) == True:
            image_click(imgs_language[img_num + 16])#Estado.png//Status.png
            image_hover("Close.png")
        elif image_appeared("Close.png") == True:
            image_click("Close.png")
    elif result == "Ok_2.png":
        image_click("Ok_2.png")
        time_wait(3000)
        if image_appeared(imgs_language[img_num + 17]) or image_appeared(imgs_language[img_num + 18]):#Error_datos.png//Data_error.png#Formateo.png//Formater.png
            matrix_set("FILE_" + str(file_num+1) + "_RUNNING",False)
            send_action_simple(4,9,files_downloaded,file_num+1)
        image_click(imgs_language[img_num + 16])#Estado.png//Status.png
        image_hover("Close.png")
    else: 
        image_click(imgs_language[img_num + 16])#Estado.png//Status.png
        image_hover("Close.png")

def finish():
    tcp_send("FINISH0")
    manual_finish()

use_firefox(True)
login()
run_cycle()
get_files()
