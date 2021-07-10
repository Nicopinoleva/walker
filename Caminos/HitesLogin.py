exec open_read("/Sikulix/BBR.py")

set_imagepath("/Sikulix/Imgs/Hites/")
set_download_directory("/home/seluser/Downloads/")
set_screenshot_directory("/home/seluser/Screenshots/")

def account_special(): 
    if image_appeared("expirado.png") == True:
        send_action_simple(1,7)
        sname = "{}_{}".format("LOGINEXP", "HITES")
        log_sshot = "{}_{}".format("PRELOGIN", "HITES")
        screenshot_save(sname)
        tcp_send("SNDPIC1 /home/seluser/Screenshots/" + sname + ".png")
        tcp_send("SNDPIC1 /home/seluser/Screenshots/" + log_sshot + ".png")
        tcp_send("FINISH7")
        abort("Credencial login expirada.")
    else:
        pass

obj = BBR()
obj.account_procedure = account_special
obj.PORTAL = "HITES"
obj.passid = "password"
obj.site_key = "6Le6POkUAAAAAPrhWc5b14fntw6TCU1tRgEKaLnk"
obj.login_verify = True
obj.enable_recaptcha = True
obj.run()
