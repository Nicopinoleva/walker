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
        self.enable_date_inverse = False
        self.enable_checker = True
        self.enable_error = False
        self.enable_recaptcha = False
        self.enable_newBBR = False
        self.enable_SalesClick = False
        self.enable_customRename = False
        self.enable_extraDownload = False
        self.login_verify = False
        self.site_key = ""
        self.checker_data = {}
        self.checker_data["mouse_move"] = (240, -5) #(x, y)
        self.checker_data["screenshot_save_crop"] = (0, 0, 70, 15) #(xoffset, yoffset, w, h)
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
        self.issued_day = today()-timedelta(days=1)
        self._portal_loaded = False
        self.files_downloaded_extension = ".zip"
        self.desc = 0
        self.marca = ""

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
        result = image_wait_multiple("badlogin.png", "comercial.png", "cerrar.png")
        if result == "badlogin.png":
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
                tcp_send("FAILED")
                manual_finish()
            else:
                send_action_simple(1,13)
        else:
            image_click("ingresar.png")
        self.account_procedure()
        result = image_wait_multiple("badlogin.png", "comercial.png", "cerrar.png")
        if result == "badlogin.png":
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
            tcp_send("FAILED")
            abort("Captcha incorrecto")
        else:
            send_action_simple(1,13)

    def date_go_last(self):
        if self.enable_newBBR:
            hoy = self.issued_day
            nueva_fecha = get_previous_month(today())
            dia = get_last_day_of_month(nueva_fecha)
            for i in range(dia - hoy.day):
                press(RIGHT)
            press(ENTER)
        else:
            time_wait(100)
            press(LEFT)
            time_wait(100)
            press(RIGHT)
            for i in range(31):
                time_wait(100)
                press(RIGHT)

    def date_go_first(self):
        if self.enable_newBBR:
            press(ENTER)
        else:
            time_wait(100)
            press(RIGHT)
            time_wait(100)
            press(LEFT)
            for i in range(31):
                time_wait(100)
                press(LEFT)

    def date_click_inverse(self, num_dias):
        image_click("dias.png")
        mouse_move(100, 0)
        click()
        hoy = self.issued_day
        if hoy.day - num_dias <= 0:
            image_click("left.png")
            self.date_go_last()
            for i in range(num_dias - hoy.day - 1):
                time_wait(100)
                press(LEFT)
        else:
            for i in range(num_dias - 1):
                time_wait(100)
                press(LEFT)
        press(TAB)

    def check_if_updated(self):
        if image_appeared("cerrar.png"):
            image_click("cerrar.png")
        self.pre_checker_procedure()
        if self.enable_newBBR or self.enable_SalesClick:
            image_click("carga_datos.png")
        if not image_appeared("ventas_hover.png"):
            send_action_simple(9,11)
            tcp_send("HIBERN")
            abort("Portal no actualizado")
        hover("ventas_hover.png")
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
        time_wait(30000)

    def date_click(self, num_dias):
        time_wait(1000)
        hoy = self.issued_day
        if hoy.day-num_dias <= 0:
            image_click("left.png")
            self.date_go_last()
            for i in range(num_dias - hoy.day - 1):
                time_wait(100)
                press(LEFT)
        else:
            nueva_fecha = subtract_days(hoy, num_dias)
            for i in range(nueva_fecha.day):
                press(RIGHT)
                time_wait(100)
            if self.enable_newBBR:
                press(ENTER)
        press(TAB)

    def get_ventas(self,num=0):
        self.to_ventas_panel()
        image_click("fecha.png")
        self.date_click(7)
        hoy = today()
        nueva_fecha = self.issued_day-timedelta(days=6)
        nueva_fecha2 = self.issued_day
        self.pre_ventas_procedure()
        self.marca_procedure(num)
        image_click("generar_informe.png")
        if matrix_get("DOWNLOAD_STARTED") == False:
            send_action_simple(3, 0)
            matrix_set("DOWNLOAD_STARTED",True)
        self.waiter()
        image_click("boton_azul.png")
        if self.enable_newBBR:
            image_click("fuente_calendario.png")
        time_wait(1000)
        if self.enable_date_inverse:
            self.date_click_inverse(7)
        self.ventas_procedure()
        image_wait("dlprompt.png")
        if self.enable_customRename:
            name1 = RUT_EMPRESA + "_" + date_to_string(nueva_fecha,"%Y%m%d") + "_" + date_to_string(nueva_fecha2,"%Y%m%d") + "_" + self.marca +  "_" + self.PORTAL + "_" + self.SIGLA +"_B2B_DIA"
        else:
            name1 = RUT_EMPRESA + "_" + date_to_string(nueva_fecha,"%Y%m%d") + "_" + date_to_string(nueva_fecha2,"%Y%m%d") + "_" + self.SIGLA +  "_" + self.PORTAL+"_B2B_DIA"
        type(get_download_directory() + name1)
        time_wait(2000)
        image_click("save.png")
        time_wait(2000)
        send_action_simple(4, 0, num_files=1)
        tcp_send("SNDFIL " + str(get_downloads_count()) + "    '" + name1 + self.files_downloaded_extension + "'")
        matrix_set("DOWNLOAD_COUNT",1)

    def get_inventario(self,num=0):
        self.to_ventas_panel()
        image_click("fecha.png")
        for i in range(self.issued_day.day - 1):
            press(RIGHT)
        if self.enable_newBBR:
            press(RIGHT)
            press(ENTER)
        time_wait(100)
        press(TAB)
        hoy = today()
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
            name2 = RUT_EMPRESA +  "_" + date_to_string(nueva_fecha2,"%Y%m%d") + "_" + date_to_string(nueva_fecha2,"%Y%m%d") + "_" + date_to_string(nueva_fecha2,"%Y%m%d") + "_" + self.marca + "_"+self.PORTAL+"_"+self.SIGLA+"_B2B_DIA_INV"
        else:
            name2 = RUT_EMPRESA +  "_" + date_to_string(nueva_fecha2,"%Y%m%d") + "_" + date_to_string(nueva_fecha2,"%Y%m%d") + "_" + date_to_string(nueva_fecha2,"%Y%m%d") + "_" + self.SIGLA +  "_"+self.PORTAL+"_B2B_DIA_INV"
        type(get_download_directory() + name2)
        time_wait(2000)
        image_click("save.png")
        time_wait(30000)
        send_action_simple(4, 0, num_files=2)
        tcp_send("SNDFIL " + str(get_downloads_count()) + "    '" + name2 + self.files_downloaded_extension + "'")
        matrix_set("DOWNLOAD_COUNT",2)
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
        self.date_go_first()
        time_wait(100)
        press(TAB)
        image_click("fecha2")
        time_wait(1000)
        image_click("left.png")
        self.date_go_last()
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

    def downloadSpecial(self,down_num,extra_down=0):
        image_click("comercial.png")
        image_click("participacion.png")
        image_click("definir_rubro.png")
        image_wait("cerrar.png")
        time_wait(500)
        press(TAB)
        for y in range(down_num):
            press(DOWN)
            time_wait(500)
        press(RIGHT)
        time_wait(500)
        press(DOWN)
        for y in range(extra_down):
            press(DOWN)
            time_wait(500)
        time_wait(500)
        press(SPACE)
        time_wait(500)
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
            press(DOWN)
            time_wait(500)
            press(DOWN)
            time_wait(500)
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
            file = "ExtraFile" + str(down_num) + str(extra_down) 
            type(get_download_directory() + file)
            image_click("save.png")
            time_wait(4000)
            tcp_send("SNDFIL " + str(get_downloads_count()) + "    '" + file + self.files_downloaded_extension + "'")
            image_click("cerrar.png")
        if extra_down == 0:
            matrix_set("CYCLE_COUNT",matrix_get("CYCLE_COUNT")+1)

    def extraDownloads(self):
        subRubroDict = {}
        rubro = ""
        if "," in EXTRA:
            temp = EXTRA.split(",")
            rubro = temp[0]
            for x in range (1,len(temp)):
                temp2 = temp[x].split("+")
                subRubroDict[temp2[0]] = temp2[1]
        else:
            rubro = EXTRA
        file_start = matrix_get("CYCLE_COUNT")
        for x in range(file_start,int(rubro)+1):
            self.downloadSpecial(x)
            if str(x) in subRubroDict:
                for y in range(1,int(subRubroDict[str(x)])):
                    self.downloadSpecial(x,extra_down=y)

    def run(self):
        if not self.login_verify:
            self.login()
            if self.enable_checker:
                self.check_if_updated()
            if not matrix_get("SSHOT_1"):
                self.screenshot_1()
                matrix_set("SSHOT_1", True)
            if not matrix_get("SSHOT_2"):
                self.screenshot_2()
                matrix_set("SSHOT_2", True)
            if get_downloads_count() == 0:
                self.get_ventas()
            time_wait(5000)
            if get_downloads_count() == 1:
                self.get_inventario()
            if self.enable_extraDownload:
                self.extraDownloads()
            self.finish_procedure()
            close_explorer()
        else:
            self.login_only()
            close_explorer()
