load_template("/Sikulix/BBR.py")

set_imagepath("/Sikulix/Imgs/LaPolar/")
set_download_directory("/home/seluser/Downloads/")
set_screenshot_directory("/home/seluser/Screenshots/")

def account_special(): 
    if image_appeared("bloqueado.png") == True:
        send_action_simple(1,15)
        sname = "{}_{}".format("LOGINBLQ", "LAPOLAR")
        log_sshot = "{}_{}".format("PRELOGIN", "LAPOLAR")
        screenshot_save(sname)
        tcp_send("SNDPIC1 /home/seluser/Screenshots/" + sname + ".png")
        tcp_send("SNDPIC1 /home/seluser/Screenshots/" + log_sshot + ".png")
        tcp_send("FINISH15")
        abort("Credencial login bloqueada.")
    elif image_appeared("expirado.png") == True:
        send_action_simple(1,7)
        sname = "{}_{}".format("LOGINEXP", "CORONA")
        log_sshot = "{}_{}".format("PRELOGIN", "CORONA")
        screenshot_save(sname)
        tcp_send("SNDPIC1 /home/seluser/Screenshots/" + sname + ".png")
        tcp_send("SNDPIC1 /home/seluser/Screenshots/" + log_sshot + ".png")
        tcp_send("FINISH7")
        abort("Credencial login expirada.")
    else:
        pass  

obj = BBR()
obj.PORTAL = "LAPOLAR"
obj.passid = "formLogin:txt_Password"
obj.enable_newBBR = True
obj.enable_recaptcha = True
obj.site_key = "6Le6POkUAAAAAPrhWc5b14fntw6TCU1tRgEKaLnk"
obj.login_verify = True
obj.account_procedure = account_special
obj.run()
