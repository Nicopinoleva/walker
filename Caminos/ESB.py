class ESB:
    def __init__(self):
        self.PORTAL = "UNDEFINED"
        self.passid = "txtPassword"
        self.mantenedor_procedure = self.mantenedor_procedure_img
        self._fecha_guardada = "0000000"
        self._fecha_inventario = "0000000"
        self.files_downloaded_extension = ".xls"
        self.login_verify = False

    def mantenedor_procedure_img(self):
        pass

    def login(self):
        open_explorer(URL_PORTAL)
        log_sshot = "{}_{}".format("PRELOGIN", self.PORTAL)
        image_click("username.png")
        type(USERNAME)
        press(TAB)
        time_wait(5000)
        type(PASSWORD)
        self.pre_login_screenshot(log_sshot)
        captcha_sb()
        result = image_wait_multiple("captcha_ok.png", "captcha_err.png")
        if result =="captcha_ok.png":
            send_action_simple(9,13)
        elif result == "captcha_err.png":
            send_action_simple(9,14)
            close_explorer()
            tcp_send("FAILED")
            abort("Captcha incorrecto")
        else:
            log("INFO", "Captcha no aparece")
            sname = "{}_{}".format("CAPTCHA",self.PORTAL)
            tcp_send("SNDPIC1 /home/seluser/Screenshots/" + sname + ".png")
            tcp_send("SNDPIC1 /home/seluser/Screenshots/" + log_sshot + ".png")
        image_click("entrar.png")
        result = image_wait_multiple("badlogin.png", "monito.png")
        if result == "badlogin.png":
            send_action_simple(1,1)
            sname = "{}_{}".format("LOGIN", self.PORTAL)
            screenshot_save(sname)
            tcp_send("SNDPIC1 /home/seluser/Screenshots/" + sname + ".png")
            tcp_send("SNDPIC1 /home/seluser/Screenshots/" + log_sshot + ".png")
            tcp_send("FINISH1")
            abort("Credenciales erroneas")
        else:
            if not matrix_get("LOGIN_CORRECT"):
                send_action_simple(1,0)
                matrix_set("LOGIN_CORRECT", True)

    def login_only(self):
        log_sshot = "{}_{}".format("PRELOGIN", self.PORTAL)
        open_explorer(URL_PORTAL)
        image_click("username.png")
        type(USERNAME)
        press(TAB)
        type(PASSWORD)
        captcha_sb()
        result = image_wait_multiple("captcha_ok.png", "captcha_err.png")
        if result =="captcha_ok.png":
            send_action_simple(9,13)
        elif result == "captcha_err.png":
            send_action_simple(9,14)
            close_explorer()
            tcp_send("FAILED")
            abort("Captcha incorrecto")
        else:
            log("INFO", "Captcha no aparece")
            sname = "{}_{}".format("CAPTCHA",self.PORTAL)
            tcp_send("SNDPIC1 /home/seluser/Screenshots/" + sname + ".png")
        image_click("entrar.png")
        result = image_wait_multiple("badlogin.png", "monito.png")
        if result == "badlogin.png":
            send_action_simple(1,1)
            sname = "{}_{}".format("LOGIN", self.PORTAL)
            screenshot_save(sname)
            tcp_send("SNDPIC1 /home/seluser/Screenshots/" + sname + ".png")
            tcp_send("SNDPIC1 /home/seluser/Screenshots/" + log_sshot + ".png")
            tcp_send("FINISH1")
            abort("Credenciales erroneas")
        elif result == "monito.png":
            send_action_simple(1,0)
            tcp_send("FINISH0")
        else:
            send_action_simple(9,3)
            screenshot_save("Portal_didnt_load")
            tcp_send("SNDPIC1 /home/seluser/Screenshots/Portal_didnt_load.png")
            tcp_send("SNDPIC1 /home/seluser/Screenshots/" + log_sshot + ".png")
            tcp_send("FINISH3")

    def pre_login_screenshot(self,name):
        pass_text(self.passid)
        screenshot_save(name)

    def go_to_mantenedor(self):
        time_wait(2000)
        image_click("B2B.png")
        self.mantenedor_procedure()
        send_action_simple(9, 0)

    def screenshot(self):
        image_click("ventas.png")
        image_click("mensual.png")
        image_wait("busqueda_boton.png")
        image_click("busqueda_boton.png")
        image_click("proveedor.png")
        mouse_move(100,0)
        click()
        screenshot_save_crop("Chequeo_LAB", 0, 0, 1360, 1020)
        tcp_send("SNDPIC2 /home/seluser/Screenshots/" + "Chequeo_LAB" + ".png")
        time_wait(15000)
        image_click("busqueda.png")
        image_click("busqueda.png")
        date1 = previous_day(today())
        date2 = get_previous_month(date1)
        time_wait(5000)
        press(TAB)
        if not matrix_get("SSHOT_1"):
            time_wait(1000)
            press(DOWN)
            time_wait(1000)
            press(TAB)
            time_wait(1000)
            press(TAB)
            time_wait(1000)
            for x in range (0,date1.month):
                press(DOWN)
                time_wait(1000)
            press(TAB)
            time_wait(1000)
            press(DOWN)
            time_wait(1000)
            press(TAB)
            time_wait(1000)
            press(DOWN)
        else:
            time_wait(1000)
            press(TAB)
            if date2.year != date1.year:
                time_wait(1000)
                press(DOWN)
            time_wait(1000)
            press(TAB)
            if date2.month == 12:
                for x in range (11):
                    time_wait(1000)
                    press(DOWN)
            else:
                time_wait(1000)
                press(UP)
        image_click("buscar_boton.png")
        image_wait("cargando.png")
        image_gone_wait("cargando.png",int(TIMEOUT*3))
        fecha1 = None
        fecha2 = None
        if not matrix_get("SSHOT_1"):
            fecha1 = date_to_string(get_first_day_of_month(date1),"%Y%m%d")
            fecha2 = date_to_string(date1,"%Y%m%d")
        else:
            fecha1 = date_to_string(get_first_day_of_month(date2),"%Y%m%d")
            fecha2 = date_to_string(get_first_day_of_month(date2),"%Y%m") + str(get_last_day_of_month(date2)) 
        filename = "{}_{}_{}_{}_{}_{}_{}".format(self.PORTAL, "B2B", "VTA", RUT_EMPRESA, fecha1, fecha2, "MENSUAL")
        screenshot_save_crop(filename, 94, 245, 1152, 355)
        if not matrix_get("SSHOT_1"):
            tcp_send("SNDSHO1 " + str(get_downloads_count()) + "     " + filename + ".png")
            matrix_set("SSHOT_1", True)
        else:
            tcp_send("SNDSHO2 " + str(get_downloads_count()) + "     " + filename + ".png")
            matrix_set("SSHOT_2", True)
        
    def get_file_dashboard(self):
        if not matrix_get("DOWNLOAD_STARTED"):
            send_action_simple(3, 0)
            matrix_set("DOWNLOAD_STARTED", True) 
        image_click("ventas.png")
        image_click("diaria.png")
        image_wait("busqueda_boton.png")
        image_click("busqueda_boton.png")
        for x in range(5):
            time_wait(3000)
            if not image_appeared("seleccione.png"):
                image_click("busqueda_boton.png")
            else:
                break
        image_click("seleccione.png")
        time_wait(1500)
        press(DOWN)
        press(ENTER)
        press(TAB)
        press(TAB)
        time_wait(3000)
        press(ENTER)
        time_wait(2000)
        press(DOWN)
        press(ENTER)
        press(TAB)
        time_wait(3000)
        press(ENTER)
        time_wait(2000)
        press(DOWN)
        press(ENTER)
        image_click("buscar_boton.png")
        image_wait("cargando.png")
        image_gone_wait("cargando.png",int(TIMEOUT*3))
        image_wait("total_ventas.png")
        time_wait(3000)
        image_hover("info.png")
        mouse_move(66, 0)
        mouse_select(68, 0)
        copy()
        time_wait(2000)
        fecha = str(get_clipboard())
        log("INFO", fecha)
        fecha = fecha.split("/")
        log("INFO", str(fecha))
        fecha_final = fecha[2][:4] + fecha[1] + fecha[0]
        self._fecha_inventario = fecha_final

    def get_file(self,num):
        time_wait(2000)
        image_hover("info.png")
        mouse_move(66+(100*num), 0)
        mouse_select(68, 0)
        copy()
        time_wait(2000)
        fecha = str(get_clipboard())
        log("INFO", fecha)
        fecha = fecha.split("/")
        log("INFO", str(fecha))
        fecha_final = fecha[2][:4] + fecha[1] + fecha[0]
        self._fecha_guardada = fecha_final
        image_hover("info.png")
        mouse_move(100+(100*num), 0) #(x, y)
        click()
        time_wait(3000)
        for x in range(5):    
            result = image_wait_multiple("exportar_boton.png", "sin_resultados.png")
            if result == "exportar_boton.png":
                time_wait(2000)
                image_click("exportar_boton.png")
                image_wait("dlprompt.png")
                filename = "{}_{}_{}_{}_{}_{}_{}_{}".format(RUT_EMPRESA, self._fecha_guardada, self._fecha_guardada, NOMBRE_EMPRESA, self.PORTAL, "B2B", "DIA", "BRUTO")
                type(get_download_directory() + filename)
                press(ENTER)
                time_wait(1000)
                send_action_simple(4, 0, get_downloads_count())
                time_wait(3000)
                tcp_send("SNDFIL" + str(get_downloads_count()) +"   '" + filename + ".xls'")
                break
            elif result == "sin_resultados.png":
                send_action_simple(3,9,get_downloads_count()+1,int(fecha[0]+fecha[1]))
                log("INFO", "Error archivo: " + str(get_downloads_count() + 1))
                break
            else:
                if x == 5:
                    send_action_simple(9, 3)
                    raise ImageNotPresentException("(exportar_boton.png, sin_resultados.png)") 
                image_hover("info.png")
                mouse_move(100+(100*num), 0) #(x, y)
                click()
        image_click("cerrar.png")
        if not image_appeared("info.png"):
            if image_appeared("replace.png"):
                image_click("replace.png")
            time_wait(3000)
            image_click("cerrar.png")
        time_wait(10000)

    def get_inventario(self):
        image_click("inventario.png")
        image_click("stock_sugerido.png")
        image_wait("busqueda_boton.png")
        image_click("busqueda_boton.png")
        for x in range(5):
            time_wait(3000)
            if not image_appeared("seleccione_ss.png"):
                image_click("busqueda_boton.png")
            else:
                break
        image_click("seleccione_ss.png")
        time_wait(1000)
        press(DOWN)
        press(ENTER)
        press(TAB)
        time_wait(3000)
        press(ENTER)
        time_wait(1000)
        press(DOWN)
        press(ENTER)
        press(TAB)
        time_wait(3000)
        press(ENTER)
        time_wait(1000)
        press(DOWN)
        press(ENTER)
        image_click("excel_extendido.png")
        image_wait("dlprompt.png")
        filename = "{}_{}_{}_{}_{}_{}_{}_{}_{}".format(RUT_EMPRESA, self._fecha_inventario, self._fecha_inventario, NOMBRE_EMPRESA, self.PORTAL, "B2B", "DIA", "INV", "BRUTO")
        type(get_download_directory() + filename)
        press(ENTER)
        time_wait(20000)
        send_action_simple(4, 0, get_downloads_count())
        tcp_send("SNDFIL" + str(get_downloads_count()) +"   '" + filename + ".xls'")
        tcp_send("FINISH0")
        close_explorer()

    def run(self):
        if not self.login_verify:
            self.login()
            self.go_to_mantenedor()
            if not matrix_get("SSHOT_1"):
                self.screenshot()
            if not matrix_get("SSHOT_2"):
                self.screenshot()
            self.get_file_dashboard()
            for x in range (get_downloads_count(),7):
                self.get_file(x)
            self.get_inventario()
        else:
            self.login_only()
