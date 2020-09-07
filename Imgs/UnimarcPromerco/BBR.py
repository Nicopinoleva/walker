from datetime import timedelta
class BBR:
    def __init__(self):
        enable_flash(True)
        matrix_register("SSHOT_1")
        matrix_register("SSHOT_2")
        self.delay_days_tolerance = 0 #Cuantos dias de retraso se toleran.
        #0 = solo se admite al dia de ayer
        #1 = se admite desde el dia de ayer y antes de ayer
        self.PORTAL = "UNDEFINED"
        self.enable_date_inverse = False
        self.enable_checker = True
        self.enable_error = False
        self.checker_data = {}
        self.checker_data["mouse_move"] = (240, -5) #(x, y)
        self.checker_data["screenshot_save_crop"] = (0, 0, 70, 15) #(xoffset, yoffset, w, h)
        self.ventas_procedure = self.ventas_procedure_method
        self.inventario_procedure = self.inventario_procedure_method
        self.pre_ventas_procedure = self.pre_ventas_procedure_method
        self.pre_inventario_procedure = self.pre_inventario_procedure_method
        self.sshot1_procedure = self.sshot1_procedure_method
        self.sshot2_procedure = self.sshot2_procedure_method
        self.pre_checker_procedure = self.empty_procedure
        self.issued_day = today()-timedelta(days=1)
        self._portal_loaded = False
        self._download_started = False
        self.files_downloaded_extension = ".zip"
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

    def login(self):
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
        press(TAB)
        type(PASSWORD)
        image_click("ingresar.png")
        result = image_wait_multiple("badlogin.png", "comercial.png", "cerrar.png")
        if result == "badlogin.png":
            #Caso de bad login
            send_action_simple(1, 1)
            sname = "{}_{}".format("LOGIN", self.PORTAL)
            screenshot_save(sname)
            tcp_send("SNDPIC1 /home/seluser/Screenshots/" + sname + ".png")
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
    def date_go_last(self):
        time_wait(100)
        press(LEFT)
        time_wait(100)
        press(RIGHT)
        for i in range(31):
            time_wait(100)
            press(RIGHT)
    def date_go_first(self):
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
        hover("ventas_hover.png")
        m = self.checker_data["mouse_move"]
        s = self.checker_data["screenshot_save_crop"]
        mouse_move(m[0], m[1])
        x = mouse_get_x()
        y = mouse_get_y()
        screenshot_save_crop("checker", x + s[0], y + s[1], s[2], s[3])
        data = get_string_from_image(get_screenshot_directory() + "checker.png")
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
            time_wait(2000)
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
        #self.dynamic_wait("pre_waiting.png")

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
        press(TAB)

    def get_ventas(self):
        self._download_started = True
        self.to_ventas_panel()
        image_click("fecha.png")
        self.date_click(7)
        hoy = today()
        nueva_fecha = self.issued_day-timedelta(days=6)
        nueva_fecha2 = self.issued_day
        self.pre_ventas_procedure()
        image_click("generar_informe.png")
        send_action_simple(3, 0)
        self.waiter()
        image_click("boton_azul.png")
        time_wait(1000)
        if self.enable_date_inverse:
            self.date_click_inverse(7)
        self.ventas_procedure()
        image_wait("dlprompt.png")
        name1 = RUT_EMPRESA + "_" + date_to_string(nueva_fecha,"%Y%m%d") + "_" + date_to_string(nueva_fecha2,"%Y%m%d") + "_" + NOMBRE_EMPRESA + self.marca + "_" + self.PORTAL+"_B2B_DIA"
        type(get_download_directory() + name1)
        time_wait(2000)
        image_click("save.png")
	time_wait(2000)
        send_action_simple(4, 0, num_files=1)
        tcp_send("SNDFIL " + str(get_downloads_count()) + "    '" + name1 + self.files_downloaded_extension + "'")

    def get_inventario(self):
        self.to_ventas_panel()
        image_click("fecha.png")
        for i in range(self.issued_day.day - 1):
            press(RIGHT)
        time_wait(100)
        press(TAB)
        hoy = today()
        nueva_fecha2 = self.issued_day
        self.pre_inventario_procedure()
        image_click("generar_informe.png")
        if not self._download_started:
            send_action_simple(3, 0)
        self.waiter()
        image_click("boton_verde.png")
        time_wait(5000)
        self.inventario_procedure()
        image_wait("dlprompt.png")
        time_wait(2000)
        name2 = RUT_EMPRESA +  "_" + date_to_string(nueva_fecha2,"%Y%m%d") + "_" + date_to_string(nueva_fecha2,"%Y%m%d") + "_" + date_to_string(nueva_fecha2,"%Y%m%d") + "_" + NOMBRE_EMPRESA + self.marca + "_"+self.PORTAL+"_B2B_DIA_INV"
        type(get_download_directory() + name2)
        time_wait(2000)
        image_click("save.png")
	time_wait(2000)
        #image_click("Cerrar.png")
        send_action_simple(4, 0, num_files=2)
        tcp_send("SNDFIL " + str(get_downloads_count()) + "    '" + name2 + self.files_downloaded_extension + "'")

    def screenshot_1(self):
        self.to_ventas_panel()
        if today().day == 1:
            image_click("fecha.png")
            time_wait(1000)
            image_click("left.png")
            time_wait(100)
            press(RIGHT)
            time_wait(100)
            press(LEFT)
            press(TAB)
        #self.date_go_first()
        self.sshot1_procedure()
        image_click("fecha.png")
        image_wait("left.png")
        press(TAB)
        image_click("generar_informe.png")
        self.waiter()
        if today().day == 1:
            date = get_previous_month(today())
        else:
            date = today().replace(day=1)
        nueva_fecha2 = self.issued_day
        name = RUT_EMPRESA +  "_" + date_to_string(date,"%Y%m%d") + "_" + date_to_string(nueva_fecha2,"%Y%m%d") + "_" + NOMBRE_EMPRESA + self.marca + "_"+self.PORTAL+"_B2B_MENSUAL"
        screenshot_save_crop(name,11,230,1325,700)
        tcp_send("SNDSHO1 " + str(get_downloads_count()) + "    '" + name + ".png'")

    def screenshot_2(self):
        self.to_ventas_panel()
        image_click("fecha.png")
        time_wait(1000)
        image_click("left.png")
        hoy = today()
        nueva_fecha = get_previous_month(hoy)
        if today().day == 1:
            time_wait(1000)
            image_click("left.png")
            nueva_fecha = get_previous_month(nueva_fecha)
        self.date_go_first()
        time_wait(100)
        press(TAB)
        image_click("fecha2")
        time_wait(1000)
        image_click("left.png")
        if today().day == 1:
            time_wait(1000)
            image_click("left.png")
        self.date_go_last()
        time_wait(100)
        press(TAB)
        self.sshot2_procedure()
        image_click("generar_informe.png")
        self.waiter()
        nueva_fecha = get_previous_month(hoy)
        if today().day == 1:
            nueva_fecha = get_previous_month(nueva_fecha)
        dia = get_last_day_of_month(nueva_fecha)
        fecha2 = nueva_fecha.replace(day=dia)
        name = RUT_EMPRESA +  "_" + date_to_string(nueva_fecha,"%Y%m%d") + "_" + date_to_string(fecha2,"%Y%m%d") + "_" + NOMBRE_EMPRESA + self.marca + "_"+self.PORTAL+"_B2B_MENSUAL"
        screenshot_save_crop(name,11,230,1325,700)
        tcp_send("SNDSHO2 " + str(get_downloads_count()) + "    '" + name + ".png'")
        tcp_send("FINISH0")

    def run(self):
        self.login()
        if self.enable_checker:
            self.check_if_updated()
        if get_downloads_count() == 0:
            self.get_ventas()
        time_wait(5000)
        if get_downloads_count() == 1:
            self.get_inventario()
        if not matrix_get("SSHOT_1"):
            self.screenshot_1()
            matrix_set("SSHOT_1", True)
        if not matrix_get("SSHOT_2"):
            self.screenshot_2()
            matrix_set("SSHOT_2", True)
        close_explorer()
