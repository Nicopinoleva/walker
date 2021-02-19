from datetime import timedelta
class BBR:
    def __init__(self):
        enable_flash(True)
        self.delay_days_tolerance = 0 #Cuantos dias de retraso se toleran.
        #0 = solo se admite al dia de ayer
        #1 = se admite desde el dia de ayer y antes de ayer
        self.PORTAL = "UNDEFINED"
        self.passid = "UNDEFINED"
        self.SIGLA = NOMBRE_EMPRESA
        self.enable_extra_calendar = False
        self.enable_special_extra_calendar = False
        self.enable_checker = True
        self.enable_error = False
        self.enable_recaptcha = False
        self.enable_newBBR = False
        self.enable_SalesClick = False
        self.enable_customRename = False
        self.enable_extraDownload = False
        self._portal_loaded = False
        self.login_verify = False
        self.custom_date = False
        self.site_key = ""
        self.marca = ""
        self.date1 = ""
        self.date2 = ""
        self.extraDownload = ""
        self.checker_data = {}
        self.checker_data["mouse_move"] = (240, -5) #(x, y)
        self.checker_data["screenshot_save_crop"] = (0, 0, 70, 15) #(xoffset, yoffset, w, h)
        self.issued_day = today()-timedelta(days=1)
        self.files_downloaded_extension = ".zip"
        self.account_procedure = self.account_procedure_method
        self.marca_procedure = self.marca_procedure_method
        self.marca_inv_procedure = self.marca_inv_procedure_method
        self.ventas_procedure = self.ventas_procedure_method
        self.inventario_procedure = self.inventario_procedure_method
        self.pre_ventas_procedure = self.pre_ventas_procedure_method
        self.pre_inventario_procedure = self.pre_inventario_procedure_method
        self.sshot1_procedure = self.sshot1_procedure_method
        self.sshot2_procedure = self.sshot2_procedure_method
        self.finish_procedure = self.finish_procedure_method
        self.pre_checker_procedure = self.empty_procedure

    def empty_procedure(self):
        pass
    def ventas_procedure_method(self):
        pass
    def inventario_procedure_method(self):
        pass
    def pre_ventas_procedure_method(self):
        pass
    def pre_inventario_procedure_method(self):
        pass
    def sshot1_procedure_method(self):
        pass
    def sshot2_procedure_method(self):
        pass
    def finish_procedure_method(self):
        pass
    def account_procedure_method(self):
        pass
    def marca_procedure_method(self,num=0):
        pass
    def marca_inv_procedure_method(self,num=0):
        pass

    def login(self):
        open_explorer(URL_PORTAL)
        log_sshot = "{}_{}".format("PRELOGIN", self.PORTAL)
        time_wait(5000)
        if self.enable_error:
            if image_appeared("error.png") == True:
                image_click("error.png")
                time_wait(2000)
                image_click("reload.png")
                time_wait(1000)
                close_explorer()
                self.login()
                return
        image_click("username.png")
        type(USERNAME)
        time_wait(5000)
        press(TAB)
        type(PASSWORD)
        self.pre_login_screenshot(log_sshot)
        if self.enable_recaptcha:
            self.recaptcha()
        else:
            image_click("ingresar.png")
        self.account_procedure()
        result = image_wait_multiple("badlogin.png", "comercial.png", "cerrar.png", "baduser.png")
        if result in ["badlogin.png", "baduser.png"]:
            #Caso de bad login
            send_action_simple(1, 1)
            sname = "{}_{}".format("LOGIN", self.PORTAL)
            screenshot_save(sname)
            tcp_send("SNDPIC1 /home/seluser/Screenshots/" + sname + ".png")
            tcp_send("SNDPIC1 /home/seluser/Screenshots/" + log_sshot + ".png")
            tcp_send("FINISH1")
            abort("Credenciales de login erroneas.")
        elif result in ["comercial.png", "cerrar.png"]:
            #Caso de login OK
            if not matrix_get("LOGIN_CORRECT"):
                send_action_simple(1, 0)
                matrix_set("LOGIN_CORRECT", True)
        else:
            #Caso de timeout
            send_action_simple(9, 3)
            raise ImageNotPresentException("Portal_didnt_load.png")

    def login_only(self):
        log_sshot = "{}_{}".format("PRELOGIN", self.PORTAL)
        open_explorer(URL_PORTAL)
        time_wait(5000)
        if self.enable_error:
            if image_appeared("error.png") == True:
                image_click("error.png")
                time_wait(2000)
                image_click("reload.png")
                time_wait(1000)
                close_explorer()
                self.login()
                return
        image_click("username.png")
        type(USERNAME)
        time_wait(5000)
        press(TAB)
        type(PASSWORD)
        self.pre_login_screenshot(log_sshot)
        if self.enable_recaptcha:
            captcha_google(self.site_key)
            press(TAB)
            press(ENTER)
            time_wait(2000)
            if image_appeared("invalid.png"):
                send_action_simple(1,14)
                tcp_send("FAILED14")
                manual_finish()
            else:
                send_action_simple(1,13)
        else:
            image_click("ingresar.png")
        self.account_procedure()
        result = image_wait_multiple("badlogin.png", "comercial.png", "cerrar.png", "baduser.png")
        if result in ["badlogin.png", "baduser.png"]:
            #Caso de bad login
            send_action_simple(1, 1)
            sname = "{}_{}".format("LOGIN", self.PORTAL)
            screenshot_save(sname)
            tcp_send("SNDPIC1 /home/seluser/Screenshots/" + sname + ".png")
            tcp_send("SNDPIC1 /home/seluser/Screenshots/" + log_sshot + ".png")
            tcp_send("FINISH1")
            manual_finish()
        elif result in ["comercial.png", "cerrar.png"]:
            #Caso de login OK
            send_action_simple(1, 0)
            tcp_send("FINISH0")
            manual_finish()
        else:
            #Caso de timeout
            tcp_send("INSERT into log (log_id, acc_id, stat_id, num_files, img) values ("+OPTION_LOG_ID+", 9, 3, 0, 'Portal_didnt_load.png');")
            screenshot_save("Portal_didnt_load")
            tcp_send("SNDPIC2 /home/seluser/Screenshots/Portal_didnt_load.png")
            tcp_send("LOGERR into log (log_id, acc_id, stat_id, num_files) values ("+OPTION_LOG_ID+", 1, 1, 0);")
            tcp_send("FINISH1")
            manual_finish()

    def pre_login_screenshot(self,name):
        pass_text(self.passid)
        screenshot_save(name)

    def recaptcha(self):
        captcha_google(self.site_key)
        time_wait(3000)
        press(TAB)
        press(ENTER)
        if image_appeared("invalid.png"):
            send_action_simple(1,14)
            tcp_send("FAILED14")
            abort("Captcha incorrecto")
        else:
            send_action_simple(1,13)

    def date_go_last(self,isSecondCalendar = True, isFirstCalendar = False):
        if self.enable_newBBR:
            hoy = self.issued_day
            nueva_fecha = get_previous_month(today())
            dia = get_last_day_of_month(nueva_fecha)
            if self.enable_special_extra_calendar and not isSecondCalendar and not isFirstCalendar:
                self.date_go_first()
            if isSecondCalendar:
                for i in range(dia - hoy.day):
                    time_wait(100)
                    press(RIGHT)
            else:
                for i in range(dia-1):
                    time_wait(100)
                    press(RIGHT)
        else:
            time_wait(100)
            press(LEFT)
            time_wait(100)
            press(RIGHT)
            for i in range(31):
                time_wait(100)
                press(RIGHT)

    def date_go_first(self):
        hoy = self.issued_day
        time_wait(100)
        press(RIGHT)
        time_wait(100)
        press(LEFT)
        for i in range(hoy.day-1):
            time_wait(100)
            press(LEFT)

    def date_click(self, num_days, isextraCalendar = False, isFirstCalendar = False):
        if isextraCalendar:
            image_click("dias.png")
            mouse_move(95,0)
            click()
            if not image_appeared("left.png"):
                image_click("dias.png")
                mouse_move(100,0)
                click()
                image_wait("left.png")
        time_wait(1000)
        hoy = self.issued_day
        if hoy.day-num_days <= 0:
            image_click("left.png")
            if isFirstCalendar:
                self.date_go_last(isSecondCalendar=False,isFirstCalendar=True)
            else:
                self.date_go_last(isSecondCalendar=False)
            for i in range(num_days - hoy.day - 1):
                time_wait(100)
                press(LEFT)
            if self.enable_newBBR:
                press(ENTER)
        else:
            if isextraCalendar:
                if self.enable_special_extra_calendar:
                    for i in range(num_days - 1):
                        time_wait(100)
                        press(LEFT)
                else:
                    for i in range(hoy.day-num_days):
                        time_wait(100)
                        press(RIGHT)
                if self.enable_newBBR:
                    press(ENTER) 
            else:
                nueva_fecha = subtract_days(hoy, num_days)
                for i in range(nueva_fecha.day):
                    press(RIGHT)
                    time_wait(100)
                if self.enable_newBBR:
                    press(ENTER)
        press(TAB)

    def date_click_dynamic(self, date, x=0, isSecondCalendar = False, isextraCalendar = False):
        print("Dia --> {}, Mes--> {}, Año-->{}".format(date[6:],date[4:6],date[:4]))
        hoy = self.issued_day
        if isextraCalendar:
            image_click("dias.png")
            mouse_move(100+x, 0)
            click()
        else:
            time_wait(1000)
            mouse_move(30,0)
        if date[:4] != hoy.year:
            for x in range(int(hoy.year) - int(date[:4])):
                image_click("year.png")
                time_wait(100)
        if int(date[4:6]) - hoy.month > 0:
            for x in range(int(date[4:6]) - hoy.month):
                time_wait(100)
                image_click("right.png")
        elif int(date[4:6]) - hoy.month < 0:
            for x in range(hoy.month - int(date[4:6])):
                time_wait(100)
                image_click("left.png")
        if int(date[4:6]) == hoy.month and int(date[:4]) == hoy.year:
            image_click("right.png")
        else:
            mouse_move(0,15)
            click() 
        if isSecondCalendar:
            self.date_go_first()
            if int(date[4:6]) == hoy.month and self.enable_newBBR:
                press(RIGHT)
        if isextraCalendar and not self.enable_newBBR:
            self.date_go_first()
        time_wait(100)
        if int(date[6:]) == 1 and not self.enable_newBBR:
            press(RIGHT)
            time_wait(100)
            press(LEFT)
        for x in range(int(date[6:])-1):
            time_wait(100)
            press(RIGHT)
        if self.enable_newBBR:
            press(ENTER)
        else:
            press(TAB)

    def check_if_updated(self):
        while True:
            if image_appeared("cerrar.png"):
                image_click("cerrar.png")
            else:
                break
            time_wait(1500)
        self.pre_checker_procedure()
        if self.enable_newBBR or self.enable_SalesClick:
            image_click("carga_datos.png")
        time_wait(5000)
        if not image_appeared("ventas_hover.png"):
            send_action_simple(9,11)
            tcp_send("HIBERN")
            abort("Portal no actualizado")
        time_wait(5000)
        image_hover("ventas_hover.png")
        mouse_get_x()
        mouse_get_y()
        m = self.checker_data["mouse_move"]
        s = self.checker_data["screenshot_save_crop"]
        mouse_move(m[0], m[1])
        x = mouse_get_x()
        y = mouse_get_y()
        screenshot_save_crop("checker", x + s[0], y + s[1], s[2], s[3])
        data = get_string_from_image(get_screenshot_directory() + "checker.png")
        print(data)
        check_day = int(string_keep_digits(data.split("-")[0]))
        #Obtener la lista de dias que acepta la tolerancia
        days_tolerance = {}
        curday = today()
        for i in range(self.delay_days_tolerance + 1):
            curday = curday - timedelta(days=1)
            days_tolerance[curday.day] = curday 
        log("INFO", "tesseract: obtained day {}. days tolerance is {}".format(str(check_day), str(days_tolerance.keys())))
        if check_day not in days_tolerance:
            send_action_simple(9, 11)
            tcp_send("HIBERN")
            abort("El portal no ha actualizado sus datos de venta.")
        self.issued_day = days_tolerance[check_day]
        log("INFO", "Datos de venta dentro de la tolerancia")

    def dynamic_wait(self, image):
        while image_appeared(image):
            time_wait(2000)
            log("INFO", "Dynamic waiting for " + image)
        log("INFO", "Dyanmic waiting done for " + image)
        
    def waiter(self):
        while True:
            tcp_send("ESPERO")
            if not image_appeared("waiting.png"):
                break
            log("INFO", "[" + OPTION_LOG_ID + "] Waiting for report")

    def to_ventas_panel(self):
        if image_appeared("cerrar.png"):
            image_click("cerrar.png")
        time_wait(1000)
        if image_appeared("cerrar2.png"):
            image_click("cerrar2.png")
        time_wait(1000)
        image_click("comercial.png")
        if not self._portal_loaded:
            self._portal_loaded = True
            send_action_simple(9, 12)
        image_click("ventas.png")
        time_wait(3000)
        # if not image_appeared("fecha.png"):
        if image_appeared("cerrar.png"):
            image_click("cerrar.png")
        if not self.enable_newBBR:
            time_wait(30000)
        else:
            time_wait(5000)

    def zolconvert(self,isStock,name):
        unzip(name,STOCK_FILE_FORMAT)
        if isStock:
            data=get_zolbit_format(ENCODING, FILE_TYPE[2:], STOCK_FILE_FORMAT, STOCK_ORDER, STOCK_DELIMITATOR, STOCK_HEADER, STOCK_DATE_FORMAT, get_download_directory(), 
                STOCK_UNITS_CONVERSION, STOCK_UNITS_DECIMAL, STOCK_AMOUNT_CONVERSION, STOCK_AMOUNT_DECIMAL, name+STOCK_FILE_FORMAT)
            print(data)
            time_wait(5000)
            nueva_fecha2 = self.issued_day
            if self.enable_customRename:
                stockname = RUT_EMPRESA +  "_" + date_to_string(nueva_fecha2,"%Y%m%d") + "_" + date_to_string(nueva_fecha2,"%Y%m%d") + "_" + self.marca + "_"+self.PORTAL+"_"+self.SIGLA+"_B2B_DIA_INV"
            else:
                stockname = RUT_EMPRESA +  "_" + date_to_string(nueva_fecha2,"%Y%m%d") + "_" + date_to_string(nueva_fecha2,"%Y%m%d") + "_" + self.SIGLA +  "_"+self.PORTAL+"_B2B_DIA_INV"
            zipper('Z'+name,'Z'+stockname+STOCK_FILE_FORMAT)
        else:
            data=get_zolbit_format(ENCODING, FILE_TYPE[:2], SALES_FILE_FORMAT, SALES_ORDER, SALES_DELIMITATOR, SALES_HEADER, SALES_DATE_FORMAT, get_download_directory(), 
                SALES_UNITS_CONVERSION, SALES_UNITS_DECIMAL, SALES_AMOUNT_CONVERSION, SALES_AMOUNT_DECIMAL, name+SALES_FILE_FORMAT)
            print(data)
            time_wait(5000)
            zipper('Z'+name,'Z'+name+SALES_FILE_FORMAT)
        temp=data.split(';')
        print(temp[1][:2])
        matrix_set("DOWNLOAD_COUNT",matrix_get("DOWNLOAD_COUNT")+1)
        tcp_send("SNDFIL " + str(matrix_get("DOWNLOAD_COUNT")) + "    '" + name + self.files_downloaded_extension + "'" + " " + temp[1][:2])

    def get_ventas(self,num=0):
        self.to_ventas_panel()
        image_click("fecha.png")
        if self.custom_date:
            self.date_click_dynamic(self.date1)
            image_click("fecha2")
            self.date_click_dynamic(self.date2,isSecondCalendar=True)
        else:
            self.date_click(7,isFirstCalendar=True)
        self.pre_ventas_procedure()
        self.marca_procedure(num)
        image_click("generar_informe.png")
        if matrix_get("DOWNLOAD_STARTED") == False:
            send_action_simple(3, 0)
            matrix_set("DOWNLOAD_STARTED",True)
        self.waiter()
        if self.custom_date:
            if self.enable_customRename:
                name = RUT_EMPRESA +  "_" + self.date1 + "_" + self.date2 + "_" +  self.marca + "_" + self.PORTAL + "_" + self.SIGLA +"_B2B_MENSUAL"
            else:
                name = RUT_EMPRESA +  "_" + self.date1 + "_" + self.date2  + "_" + self.SIGLA +  "_" + self.PORTAL + "_B2B_MENSUAL"
            screenshot_save_crop(name,11,230,1325,700)
            tcp_send("SNDSHO1 " + str(get_downloads_count()) + "    '" + name + ".png'")
        image_click("boton_azul.png")
        if self.enable_newBBR:
            image_click("fuente_calendario.png")
        time_wait(1000)
        if self.enable_extra_calendar:
            if self.custom_date:
                self.date_click_dynamic(self.date1,isextraCalendar=True)
                if self.date2 != "none":
                    self.date_click_dynamic(self.date2,isSecondCalendar=True,isextraCalendar=True,x=270)
            else:
                self.date_click(7,isextraCalendar=True)
        self.ventas_procedure()
        image_wait("dlprompt.png")
        nueva_fecha = self.issued_day-timedelta(days=6)
        nueva_fecha2 = self.issued_day
        if self.custom_date:
            if self.enable_customRename:
                name1 = RUT_EMPRESA + "_" + self.date1 + "_" + self.date2 + "_" + self.marca +  "_" + self.PORTAL + "_" + self.SIGLA +"_B2B_DIA"
            else:
                name1 = RUT_EMPRESA + "_" + self.date1 + "_" + self.date2 + "_" + self.SIGLA +  "_" + self.PORTAL+"_B2B_DIA"
        else:
            if self.enable_customRename:
                name1 = RUT_EMPRESA + "_" + date_to_string(nueva_fecha,"%Y%m%d") + "_" + date_to_string(nueva_fecha2,"%Y%m%d") + "_" + self.marca +  "_" + self.PORTAL + "_" + self.SIGLA +"_B2B_DIA"
            else:
                name1 = RUT_EMPRESA + "_" + date_to_string(nueva_fecha,"%Y%m%d") + "_" + date_to_string(nueva_fecha2,"%Y%m%d") + "_" + self.SIGLA +  "_" + self.PORTAL+"_B2B_DIA"
        type(get_download_directory() + name1)
        time_wait(2000)
        image_click("save.png")
        time_wait(2000)
        self.zolconvert(False,name1)
        send_action_simple(4, 0, num_files=1)
        matrix_set("SALES",True)

    def get_inventario(self,num=0):
        self.to_ventas_panel()
        image_click("fecha.png")
        time_wait(500)
        for i in range(self.issued_day.day - 1):
            press(RIGHT)
            time_wait(100)
        if self.enable_newBBR:
            time_wait(100)
            press(ENTER)
        time_wait(100)
        press(TAB)
        nueva_fecha2 = self.issued_day
        self.pre_inventario_procedure()
        self.marca_inv_procedure(num)
        image_click("generar_informe.png")
        self.waiter()
        if self.enable_newBBR:
            image_click("boton_azul.png")
            image_click("periodo.png")
        else:
            image_click("boton_verde.png")
        time_wait(5000)
        self.inventario_procedure()
        image_wait("dlprompt.png")
        time_wait(2000)
        if self.enable_customRename:
            name = RUT_EMPRESA +  "_" + date_to_string(nueva_fecha2,"%Y%m%d") + "_" + date_to_string(nueva_fecha2,"%Y%m%d") + "_" + date_to_string(nueva_fecha2,"%Y%m%d") + "_" + self.marca + "_"+self.PORTAL+"_"+self.SIGLA+"_B2B_DIA_INV"
        else:
            name = RUT_EMPRESA +  "_" + date_to_string(nueva_fecha2,"%Y%m%d") + "_" + date_to_string(nueva_fecha2,"%Y%m%d") + "_" + date_to_string(nueva_fecha2,"%Y%m%d") + "_" + self.SIGLA +  "_"+self.PORTAL+"_B2B_DIA_INV"
        type(get_download_directory() + name)
        time_wait(2000)
        image_click("save.png")
        time_wait(30000)
        self.zolconvert(True,name)
        send_action_simple(4, 0, num_files=2)
        matrix_set("STOCK",True)
        time_wait(2000)
        image_click("cerrar.png")

    def screenshot_1(self,num=0):
        self.to_ventas_panel()
        self.sshot1_procedure()
        self.marca_procedure(num)
        if not self.enable_newBBR:
            image_click("fecha.png")
            image_wait("left.png")
            press(TAB)
        image_click("generar_informe.png")
        self.waiter()
        date = previous_day(today()).replace(day=1)
        nueva_fecha2 = self.issued_day
        if self.enable_customRename:
            name = RUT_EMPRESA +  "_" + date_to_string(date,"%Y%m%d") + "_" + date_to_string(nueva_fecha2,"%Y%m%d") + "_" +  self.marca + "_" + self.PORTAL + "_"+ self.SIGLA +"_B2B_MENSUAL"
        else:
            name = RUT_EMPRESA +  "_" + date_to_string(date,"%Y%m%d") + "_" + date_to_string(nueva_fecha2,"%Y%m%d") + "_" + self.SIGLA +  "_"+self.PORTAL+"_B2B_MENSUAL"
        screenshot_save_crop(name,11,230,1325,700)
        tcp_send("SNDSHO1 " + str(get_downloads_count()) + "    '" + name + ".png'")

    def screenshot_2(self,num=0):
        self.to_ventas_panel()
        image_click("fecha.png")
        time_wait(1000)
        image_click("left.png")
        if not self.enable_newBBR:
            self.date_go_first()
        else:
            press(ENTER)
        time_wait(100)
        press(TAB)
        time_wait(2000)
        image_click("fecha2.png")
        time_wait(1000)
        image_click("left.png")
        self.date_go_last()
        if self.enable_newBBR:
            press(ENTER)
        time_wait(100)
        press(TAB)
        self.sshot2_procedure()
        self.marca_procedure(num)
        image_click("generar_informe.png")
        self.waiter()
        hoy = today()
        nueva_fecha = get_previous_month(hoy)
        if today().day == 1:
            nueva_fecha = get_previous_month(nueva_fecha)
        dia = get_last_day_of_month(nueva_fecha)
        fecha2 = nueva_fecha.replace(day=dia)
        if self.enable_customRename:
            name = RUT_EMPRESA +  "_" + date_to_string(nueva_fecha,"%Y%m%d") + "_" + date_to_string(fecha2,"%Y%m%d") + "_" +  self.marca + "_" + self.PORTAL + "_" + self.SIGLA +"_B2B_MENSUAL"
        else:
            name = RUT_EMPRESA +  "_" + date_to_string(nueva_fecha,"%Y%m%d") + "_" + date_to_string(fecha2,"%Y%m%d") + "_" + self.SIGLA + "_"+self.PORTAL+"_B2B_MENSUAL"
        screenshot_save_crop(name,11,230,1325,700)
        tcp_send("SNDSHO2 " + str(get_downloads_count()) + "    '" + name + ".png'") 

    def downloadSpecial(self,down_num,proveedor,extra_down=0):
        image_click("comercial.png")
        image_click("participacion.png")
        time_wait(2000)
        if proveedor >= 0:
            image_hover("selec_proveedor.png")
            mouse_move(200,0)
            click()
            time_wait(2000)
            for x in range (10):
                press(UP)
                time_wait(200)
            time_wait(1000)
            for x in range (proveedor):
                press(DOWN)
                time_wait(200)
            press(ENTER)
        image_click("definir_rubro.png")
        image_wait("cerrar.png")
        time_wait(500)
        press(TAB)
        for y in range(down_num-1):
            press(DOWN)
            time_wait(100)
        press(RIGHT)
        time_wait(500)
        press(DOWN)
        for y in range(extra_down):
            press(DOWN)
            time_wait(100)
        time_wait(500)
        press(SPACE)
        time_wait(500)
        image_hover("extradownload.png")
        mouse_move(10,-10)
        screenshot_save_crop(str(down_num) + str(extra_down+1),mouse_get_x(),mouse_get_y(),200,20)
        temp = get_string_from_image(get_screenshot_directory() + str(down_num) + str(extra_down+1) + ".png")
        invalid = ('<','>',':','"','/','|',"?",'*',"\\")
        print(temp)
        for x in invalid:
            if x in temp:
                temp = "SUBRUBRO\n"
        print(temp[1])
        name = temp[:-5]
        if not name[1].isupper():
            name = "SUBRUBRO"
        print(name)
        image_click("seleccionar.png")
        image_click("generar_informe.png")
        self.waiter()
        if image_appeared("no.png"):
            image_click("no.png")
        else:
            image_click("boton_azul.png")
            image_click("fuentes.png")
            image_wait("cerrar.png")
            press(TAB)
            time_wait(500)
            for x in range(2):
                press(DOWN)
                time_wait(500)
            press(TAB)
            time_wait(500)
            press(ENTER)
            time_wait(2000)
            image_wait("cerrar.png")
            press(TAB)
            time_wait(500)
            press(ENTER)
            image_wait("dlprompt.png")
            type(get_download_directory() + self.SIGLA + "-" + str(name) + "-" + self.marca + str(down_num) + str(extra_down+1))
            image_click("save.png")
            time_wait(4000)
            tcp_send("SNDFIL " + str(get_downloads_count()) + "    '" + self.SIGLA + "-" + str(name) + "-" + self.marca + str(down_num) + str(extra_down+1) + self.files_downloaded_extension + "'")
            image_click("cerrar.png")
                
    def extraDownloads(self, proveedor = -1):
        print("La sigla es {}, y la marca es {}".format(self.SIGLA,self.marca))
        subRubroDict = {}
        rubro = ""
        if "," in self.extraDownload:
            temp = self.extraDownload.split(",")
            rubro = temp[0]
            for x in range (1,len(temp)):
                temp2 = temp[x].split("+")
                subRubroDict[temp2[0]] = temp2[1]
        else:
            rubro = self.extraDownload
        file_start = matrix_get("EXTRA_CYCLE_COUNT")+1
        # print("El ciclo principal parte de {}".format(file_start))
        for x in range(file_start,int(rubro)+1):
            # print("El ciclo principal va en {}".format(matrix_get("EXTRA_CYCLE_COUNT")+1))
            if str(x) in subRubroDict:
                # print("El subsiclo parte de {}".format(matrix_get("IN_CYCLE_COUNT")))
                for y in range(int(matrix_get("IN_CYCLE_COUNT")),int(subRubroDict[str(x)])):
                    self.downloadSpecial(x,proveedor,extra_down=y)
                    matrix_set("IN_CYCLE_COUNT",matrix_get("IN_CYCLE_COUNT")+1)
                    # print("El subsiclo va en {}".format(matrix_get("IN_CYCLE_COUNT")))
                matrix_set("IN_CYCLE_COUNT",0)
            else:
                self.downloadSpecial(x,proveedor)
            matrix_set("EXTRA_CYCLE_COUNT",matrix_get("EXTRA_CYCLE_COUNT")+1)

    def run(self):
        if not self.login_verify:
            if len(DATE) != 1:
                self.custom_date = True
                temp = DATE.split("-")
                self.date1 = temp[0]
                self.date2 = temp[1]
            self.login()
            if self.enable_checker:
                self.check_if_updated()
            if self.custom_date:
                self.get_ventas()
                while(True):
                    newDate = tcp_send_recieve("ENDHIS")
                    print(len(newDate))
                    if len(newDate) < 6:
                        break
                    else:
                        temp = newDate.split("-")
                        self.date1 = temp[0][2:]
                        self.date2 = temp[1]
                        self.get_ventas()
                close_explorer()
                tcp_send("FINISH")
            else:
                if not matrix_get("SSHOT_1"):
                    self.screenshot_1()
                    matrix_set("SSHOT_1", True)
                if not matrix_get("SSHOT_2"):
                    self.screenshot_2()
                    matrix_set("SSHOT_2", True)
                if not matrix_get("SALES"):
                    self.get_ventas()
                time_wait(5000)
                if not matrix_get("STOCK"):
                    self.get_inventario()
                if self.enable_extraDownload:
                    self.extraDownloads()
            self.finish_procedure()
            close_explorer()
        else:
            self.login_only()
            close_explorer()
# def date_click_inverse(self, num_days):
    #     image_click("dias.png")
    #     mouse_move(100, 0)
    #     click()
    #     hoy = self.issued_day
    #     if hoy.day - num_days <= 0:
    #         image_click("left.png")
    #         self.date_go_last()
    #         for i in range(num_days - hoy.day - 1):
    #             time_wait(100)
    #             press(LEFT)
    #     else:
    #         for i in range(num_days - 1):
    #             time_wait(100)
    #             press(LEFT)
    #     press(TAB)