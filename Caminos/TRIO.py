class TRIO:
    def __init__(self):
        self.PORTAL = "UNDEFINED"
        self.special_download = "UNDEFINED"
        self.pop_up = False
        self.login_verify = False
        self.jerarquia_procedure = self.jerarquia_procedure_method
        self.tiendas = []
        self.imgs_tiendas = []
        self.rut = []
        self.sku_num = 0
        self.fecha1 = "00000000"
        self.fecha2 = "00000000"

    def jerarquia_procedure_method(self):
        pass

    def login(self):
        open_explorer(URL_PORTAL)
        image_click("B2b.png")
        press(DOWN)
        press(ENTER)
        time_wait(2000)
        press(TAB)
        if isinstance(self.rut, basestring):
            type(self.rut)
        else:
            if self.rut[1] == 'nones':
                type(self.rut[0])
            else:
                type(self.rut[1])
        time_wait(5000)
        press(TAB)
        type(USERNAME)
        time_wait(5000)
        press(TAB)
        type(PASSWORD)
        for x in range(2):
            press(TAB)
        press(ENTER)
        time_wait(5000)
        if self.pop_up:
            result = image_wait_multiple("Credenciales.png", "Expirado.png", "Pop_up_kill.png", "Expirado2.png", "Pop_up_kill2.png", "Pop_up_kill3.png")
        else:
            result = image_wait_multiple("Credenciales.png", "Expirado.png", "Expirado2.png", "Cuenta.png")
        if result == "Credenciales.png":
            send_action_simple(1,1)
            sname = "{}_{}".format("LOGIN", self.PORTAL)
            screenshot_save(sname)
            tcp_send("SNDPIC1 /home/seluser/Screenshots/" + sname + ".png")
            tcp_send("FINISH1")
            close_explorer()
            abort("Credenciales erroneas")
        elif result in ["Expirado.png", "Expirado2.png"]:
            send_action_simple(1,7)
            sname = "{}_{}".format("LOGIN", self.PORTAL)
            screenshot_save(sname)
            tcp_send("SNDPIC1 /home/seluser/Screenshots/" + sname + ".png")
            tcp_send("FINISH7")
            close_explorer()
            abort("Credenciales expiradas")
        elif result in ["Pop_up_kill.png", "Cuenta.png", "Pop_up_kill2.png", "Pop_up_kill3.png"]:
            if not matrix_get("LOGIN_CORRECT"):
                send_action_simple(1,0)
                matrix_set("LOGIN_CORRECT", True)

    def login_only(self):
        open_explorer(URL_PORTAL)
        image_click("B2b.png")
        press(DOWN)
        press(ENTER)
        time_wait(2000)
        press(TAB)
        if isinstance(self.rut, basestring):
            type(self.rut)
        else:
            type(self.rut[1])
        press(TAB)
        type(USERNAME)
        press(TAB)
        type(PASSWORD)
        for x in range(2):
            press(TAB)
        press(ENTER)
        time_wait(1500)
        if self.pop_up:
            result = image_wait_multiple("Credenciales.png", "Expirado.png", "Pop_up_kill.png", "Expirado2.png", "Pop_up_kill2.png", "Pop_up_kill3.png")
        else:
            result = image_wait_multiple("Credenciales.png", "Expirado.png", "Cuenta.png", "Expirado2.png")
        if result == "Credenciales.png":
            send_action_simple(1,1)
            sname = "{}_{}".format("LOGIN", self.PORTAL)
            screenshot_save(sname)
            tcp_send("SNDPIC1 /home/seluser/Screenshots/" + sname + ".png")
            tcp_send("FINISH1")
            close_explorer()
            abort("Credenciales erroneas")
        elif result in ["Expirado.png","Expirado2.png"]:
            send_action_simple(1,7)
            sname = "{}_{}".format("LOGIN", self.PORTAL)
            screenshot_save(sname)
            tcp_send("SNDPIC1 /home/seluser/Screenshots/" + sname + ".png")
            tcp_send("FINISH7")
            close_explorer()
            abort("Credenciales expiradas")
        elif result in ["Pop_up_kill.png", "Cuenta.png", "Pop_up_kill2.png", "Pop_up_kill3.png"]:
            send_action_simple(1,0)
            tcp_send("FINISH0")
        else:
            send_action_simple(9,3)
            screenshot_save("Portal_didnt_load")
            tcp_send("SNDPIC1 /home/seluser/Screenshots/Portal_didnt_load.png")
            tcp_send("FINISH3")
            close_explorer()
            manual_finish()

    def get_to_dashboard(self):
        if self.pop_up:
            result = image_wait_multiple("Pop_up_kill.png", "Pop_up_kill2.png", "Pop_up_kill3.png")
            image_hover(result)
            mouse_move(0,50)
            click()
        send_action_simple(9,0)
        image_hover("Ventas.png")
        if self.special_download == "UNDEFINED": 
            image_click("Analisis.png")
        else:
            image_click("Informe_venta.png")
        if self.pop_up:
            time_wait(2000)
            result = image_wait_multiple("Pop_up_kill.png", "Pop_up_kill2.png", "Pop_up_kill3.png")
            image_hover(result)
            mouse_move(0,50)
            click()
        time_wait(1500)

    def dashboard(self):
        self.jerarquia_procedure()
        image_click("Ordenar.png")
        for x in range(self.sku_num):
            press(DOWN)
        press(ENTER)
        if get_weekday_as_int() == 0:
            image_click("Semana.png")
            press(DOWN)
            press(ENTER)

    def change_units(self):
        image_click("Unidades.png")
        for x in range(2):
            press(DOWN)
        press(ENTER)

    def change_store(self,store):
        image_click(imgs_tiendas[store])
        time_wait(1000)
        press(DOWN)
        time_wait(1000)
        press(ENTER)
        image_click("Consultar.png")

    def download(self):
        time_wait(2500)
        image_gone_wait("Waiting.png", timeout = int(TIMEOUT)*3)
        if self.pop_up:
            image_click("Pop_up_kill_dashboard.png")
        press(PAGE_DOWN)
        image_click("Csv.png")

    def file_rename(self,files_downloaded,U_M):
        if isinstance(self.rut, basestring):
            filename = "{}_{}_{}_{}_{}_{}_{}_{}_{}_{}_{}".format(self.rut,self.fecha1,self.fecha2,self.fecha2,tiendas[files_downloaded],U_M,self.PORTAL,NOMBRE_EMPRESA,"B2B","DIA","INV")
        else:
            filename = "{}_{}_{}_{}_{}_{}_{}_{}_{}_{}_{}".format(self.rut[0],self.fecha1,self.fecha2,self.fecha2,tiendas[files_downloaded],U_M,self.PORTAL,NOMBRE_EMPRESA,"B2B","DIA","INV")
        image_wait("Save.png")
        type(filename)
        image_click("Save.png")
        time_wait(2000)
        tcp_send("SNDFIL" + str(get_downloads_count()) +"   '" + filename + ".csv'")
        # matrix_set("DOWNLOAD_COUNT",matrix_get("DOWNLOAD_COUNT")+1)

    def screenshots(self):
        if matrix_get("SSHOT_1"):
            self.change_units()
        image_click("Consultar.png")
        image_gone_wait("Waiting.png")
        if self.pop_up:
            image_click("Pop_up_kill_dashboard.png")
        time_wait(2500)
        if not matrix_get("SSHOT_1"):
            if isinstance(self.rut, basestring):
                filename = "{}_{}_{}_{}_{}_{}_{}_{}_{}_{}".format(self.rut,self.fecha1,self.fecha2,self.fecha2,"U",self.PORTAL,NOMBRE_EMPRESA,"B2B","DIA","INV")
            else:
                filename = "{}_{}_{}_{}_{}_{}_{}_{}_{}_{}".format(self.rut[0],self.fecha1,self.fecha2,self.fecha2,"U",self.PORTAL,NOMBRE_EMPRESA,"B2B","DIA","INV")
            screenshot_save_crop(filename,0,0,1360,1020)
            tcp_send("SNDSHO1 " + str(get_downloads_count()) + "     " + filename + ".png")
            matrix_set("SSHOT_1", True)
        elif not matrix_get("SSHOT_2"):
            if isinstance(self.rut, basestring):
                filename = "{}_{}_{}_{}_{}_{}_{}_{}_{}_{}".format(self.rut,self.fecha1,self.fecha2,self.fecha2,"M",self.PORTAL,NOMBRE_EMPRESA,"B2B","DIA","INV")
            else:
                filename = "{}_{}_{}_{}_{}_{}_{}_{}_{}_{}".format(self.rut[0],self.fecha1,self.fecha2,self.fecha2,"M",self.PORTAL,NOMBRE_EMPRESA,"B2B","DIA","INV")
            screenshot_save_crop(filename,0,0,1360,1020)
            tcp_send("SNDSHO2 " + str(get_downloads_count()) + "     " + filename + ".png")
            matrix_set("SSHOT_2", True)

    def get_to_store(self,start,files_downloaded):
        image_click("Tienda.png")
        for x in range(start+files_downloaded):
            press(DOWN)
        press(ENTER)
        time_wait(1500)

    def cycle(self,start,files_downloaded,num_stores,U_M):
        for x in range (start + files_downloaded, start + num_stores):
            self.change_store(x)
            self.download()
            self.file_rename(x,U_M)
            if get_downloads_count() % int(OPTION_TRACE_EVERY) == 0:
                send_action_simple(4,0,get_downloads_count())

    def get_files(self,start,files_downloaded,num_stores):
        if not matrix_get("DOWNLOAD_STARTED"):
            send_action_simple(3,0)
            matrix_set("DOWNLOAD_STARTED",True)
        if files_downloaded >=0 and files_downloaded < num_stores :
            if start !=0:
                self.get_to_store(start,files_downloaded)
            elif get_downloads_count() !=0:
                self.get_to_store(start,files_downloaded)
            self.cycle(start,files_downloaded,num_stores,"U")
            self.get_to_dashboard()
            self.dashboard()
            self.change_units()
            self.get_to_store(start,0)
            self.cycle(start,0,num_stores,"M")
        elif files_downloaded >= num_stores:
            self.change_units()
            files_downloaded -= num_stores
            self.get_to_store(start,files_downloaded)
            self.cycle(start,files_downloaded,num_stores,"M")
        matrix_set("DOWNLOAD_STARTED",False)

    def get_files_special(self,file_num):
        image_click("Documentos.png")
        for x in range(0,file_num+1):
            press(TAB)
        press(ENTER)
        image_wait("Save.png")
        time_wait(2000)
        fecha1 = date_to_string(subtract_days(today(),file_num+1),"%Y%m%d")
        fecha2 = date_to_string(subtract_days(today(),7),"%Y%m%d")
        if self.special_download == "DAILY":
            if isinstance(self.rut, basestring):
                filename = "{}_{}_{}_{}_{}_{}_{}_{}".format(self.rut,fecha1,fecha1,fecha1,NOMBRE_EMPRESA,self.PORTAL,"B2B","INV")
            else:
                filename = "{}_{}_{}_{}_{}_{}_{}_{}".format(self.rut[0],fecha1,fecha1,fecha1,NOMBRE_EMPRESA,self.PORTAL,"B2B","INV")
        else:
            fecha1 = date_to_string(subtract_days(today(),file_num+1+get_weekday_as_int()),"%Y%m%d")
            fecha2 = date_to_string(subtract_days(today(),7+get_weekday_as_int()),"%Y%m%d")
            if isinstance(self.rut, basestring):
                filename = "{}_{}_{}_{}_{}_{}_{}_{}".format(self.rut,fecha2,fecha1,fecha1,NOMBRE_EMPRESA,self.PORTAL,"B2B","INV")
            else:
                filename = "{}_{}_{}_{}_{}_{}_{}_{}".format(self.rut[0],fecha2,fecha1,fecha1,NOMBRE_EMPRESA,self.PORTAL,"B2B","INV")
        type(filename)
        image_click("Save.png")
        time_wait(5000)
        matrix_set("DOWNLOAD_COUNT",file_num+1)
        data=get_zolbit_format(ENCODING, FILE_TYPE[:2], SALES_FILE_FORMAT, SALES_ORDER, SALES_DELIMITATOR, SALES_HEADER, SALES_DATE_FORMAT, get_download_directory(), 
                SALES_UNITS_CONVERSION, SALES_UNITS_DECIMAL, SALES_AMOUNT_CONVERSION, SALES_AMOUNT_DECIMAL, filename+SALES_FILE_FORMAT)
        print(data)
        temp=data.split(';')
        print(temp[1][:2])
        time_wait(5000)
        zipper(filename,filename+SALES_FILE_FORMAT)
        if self.special_download == "DAILY":
            if isinstance(self.rut, basestring):
                filenamezip = "{}_{}_{}_{}_{}_{}_{}".format(self.rut,fecha1,fecha1,NOMBRE_EMPRESA,self.PORTAL,"B2B","INV")
            else:
                filenamezip = "{}_{}_{}_{}_{}_{}_{}".format(self.rut[0],fecha1,fecha1,NOMBRE_EMPRESA,self.PORTAL,"B2B","INV")
            zipper('Z'+filename,'Z'+filenamezip+".csv")
            tcp_send("SNDFIL" + str(matrix_get("DOWNLOAD_COUNT")) +"   '" + filename + ".txt'")
        else:
            if isinstance(self.rut, basestring):
                filelist = ["Z{}_{}_{}_{}_{}_{}_{}{}".format(self.rut,fecha1,fecha1,NOMBRE_EMPRESA,self.PORTAL,"B2B","INV",".csv"),
                "Z{}_{}_{}_{}_{}_{}_{}{}".format(self.rut,date_to_string(subtract_days(today(),2+get_weekday_as_int()),"%Y%m%d"),
                    date_to_string(subtract_days(today(),2+get_weekday_as_int()),"%Y%m%d"),NOMBRE_EMPRESA,self.PORTAL,"B2B","INV",".csv"),
                "Z{}_{}_{}_{}_{}_{}_{}{}".format(self.rut,date_to_string(subtract_days(today(),3+get_weekday_as_int()),"%Y%m%d"),
                    date_to_string(subtract_days(today(),3+get_weekday_as_int()),"%Y%m%d"),NOMBRE_EMPRESA,self.PORTAL,"B2B","INV",".csv"),
                "Z{}_{}_{}_{}_{}_{}_{}{}".format(self.rut,date_to_string(subtract_days(today(),4+get_weekday_as_int()),"%Y%m%d"),
                    date_to_string(subtract_days(today(),4+get_weekday_as_int()),"%Y%m%d"),NOMBRE_EMPRESA,self.PORTAL,"B2B","INV",".csv"),
                "Z{}_{}_{}_{}_{}_{}_{}{}".format(self.rut,date_to_string(subtract_days(today(),5+get_weekday_as_int()),"%Y%m%d"),
                    date_to_string(subtract_days(today(),5+get_weekday_as_int()),"%Y%m%d"),NOMBRE_EMPRESA,self.PORTAL,"B2B","INV",".csv"),
                "Z{}_{}_{}_{}_{}_{}_{}{}".format(self.rut,date_to_string(subtract_days(today(),6+get_weekday_as_int()),"%Y%m%d"),
                    date_to_string(subtract_days(today(),6+get_weekday_as_int()),"%Y%m%d"),NOMBRE_EMPRESA,self.PORTAL,"B2B","INV",".csv"),
                "Z{}_{}_{}_{}_{}_{}_{}{}".format(self.rut,date_to_string(subtract_days(today(),7+get_weekday_as_int()),"%Y%m%d"),
                    date_to_string(subtract_days(today(),7+get_weekday_as_int()),"%Y%m%d"),NOMBRE_EMPRESA,self.PORTAL,"B2B","INV",".csv")]
            else:
                filelist = ["Z{}_{}_{}_{}_{}_{}_{}{}".format(self.rut[0],fecha1,fecha1,NOMBRE_EMPRESA,self.PORTAL,"B2B","INV",".csv"),
                "Z{}_{}_{}_{}_{}_{}_{}{}".format(self.rut[0],date_to_string(subtract_days(today(),2+get_weekday_as_int()),"%Y%m%d"),
                    date_to_string(subtract_days(today(),2+get_weekday_as_int()),"%Y%m%d"),NOMBRE_EMPRESA,self.PORTAL,"B2B","INV",".csv"),
                "Z{}_{}_{}_{}_{}_{}_{}{}".format(self.rut[0],date_to_string(subtract_days(today(),3+get_weekday_as_int()),"%Y%m%d"),
                    date_to_string(subtract_days(today(),3+get_weekday_as_int()),"%Y%m%d"),NOMBRE_EMPRESA,self.PORTAL,"B2B","INV",".csv"),
                "Z{}_{}_{}_{}_{}_{}_{}{}".format(self.rut[0],date_to_string(subtract_days(today(),4+get_weekday_as_int()),"%Y%m%d"),
                    date_to_string(subtract_days(today(),4+get_weekday_as_int()),"%Y%m%d"),NOMBRE_EMPRESA,self.PORTAL,"B2B","INV",".csv"),
                "Z{}_{}_{}_{}_{}_{}_{}{}".format(self.rut[0],date_to_string(subtract_days(today(),5+get_weekday_as_int()),"%Y%m%d"),
                    date_to_string(subtract_days(today(),5+get_weekday_as_int()),"%Y%m%d"),NOMBRE_EMPRESA,self.PORTAL,"B2B","INV",".csv"),
                "Z{}_{}_{}_{}_{}_{}_{}{}".format(self.rut[0],date_to_string(subtract_days(today(),6+get_weekday_as_int()),"%Y%m%d"),
                    date_to_string(subtract_days(today(),6+get_weekday_as_int()),"%Y%m%d"),NOMBRE_EMPRESA,self.PORTAL,"B2B","INV",".csv"),
                "Z{}_{}_{}_{}_{}_{}_{}{}".format(self.rut[0],date_to_string(subtract_days(today(),7+get_weekday_as_int()),"%Y%m%d"),
                    date_to_string(subtract_days(today(),7+get_weekday_as_int()),"%Y%m%d"),NOMBRE_EMPRESA,self.PORTAL,"B2B","INV",".csv")]
            zipper('Z'+filename,'Z'+filename+".csv",filelist)
            tcp_send("SNDFIL" + str(matrix_get("DOWNLOAD_COUNT")) +"   '" + filename + ".zip'" + " " + temp[1][:2])

    def run(self):
        if not self.login_verify:
            self.login()
            self.get_to_dashboard()
            if self.special_download == "DAILY":
                file_num = matrix_get("DOWNLOAD_COUNT")
                for x in range(file_num,7):
                    self.get_files_special(x)
            elif self.special_download == "WEEKLY":
                self.get_files_special(0)
            else:
                self.dashboard()
                if not matrix_get("SSHOT_1"):
                    self.screenshots()
                if not matrix_get("SSHOT_2"):
                    self.screenshots()
                if not matrix_get("DOWNLOAD_STARTED"):
                    self.get_to_dashboard()
                    self.dashboard()
                self.get_files(0,get_downloads_count(),int(NUM_LOCALES))
            tcp_send("FINISH0")
            close_explorer()
        else:
            self.login_only()
            close_explorer()
            manual_finish()
