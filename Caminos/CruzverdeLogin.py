load_template("/Sikulix/BBR.py")

set_imagepath("/Sikulix/Imgs/Cruzverde/")
set_download_directory("/home/seluser/Downloads/")
set_screenshot_directory("/home/seluser/Screenshots/")

def account_special(): 
    if image_appeared("bloqueado.png") == True:
        send_action_simple(1,15)
        sname = "{}_{}".format("LOGINBLQ", "CRUZVERDE")
        log_sshot = "{}_{}".format("PRELOGIN", "CRUZVERDE")
        screenshot_save(sname)
        tcp_send("SNDPIC1 /home/seluser/Screenshots/" + sname + ".png")
        tcp_send("SNDPIC1 /home/seluser/Screenshots/" + log_sshot + ".png")
        tcp_send("FINISH15")
        manual_finish()
    else:
        pass 

obj = BBR()
obj.PORTAL = "CRUZVERDE"
obj.passid = "password"
obj.login_verify = True
obj.enable_newBBR = True
# obj.enable_recaptcha = True
# obj.site_key = "6Le6POkUAAAAAPrhWc5b14fntw6TCU1tRgEKaLnk"
obj.account_procedure = account_special
obj.run()
