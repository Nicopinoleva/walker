load_template("/Sikulix/BBR.py")

set_imagepath("/Sikulix/Imgs/Farmaciasahumada/")
set_download_directory("/home/seluser/Downloads/")
set_screenshot_directory("/home/seluser/Screenshots/")

def account_special(): 
    if image_appeared("bloqueado.png") == True:
        send_action_simple(1,15)
        sname = "{}_{}".format("LOGINBLQ", "FASA")
        log_sshot = "{}_{}".format("PRELOGIN", "FASA")
        screenshot_save(sname)
        tcp_send("SNDPIC1 /home/seluser/Screenshots/" + sname + ".png")
        tcp_send("SNDPIC1 /home/seluser/Screenshots/" + log_sshot + ".png")
        tcp_send("FINISH15")
        abort("Credencial login bloqueada.")
    else:
        pass 

obj = BBR()
obj.PORTAL = "FASA"
obj.passid = "password"
obj.login_verify = True
obj.account_procedure = account_special
obj.run()
