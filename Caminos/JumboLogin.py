load_template("/Sikulix/BBR.py")

set_imagepath("/Sikulix/Imgs/Jumbo/")
set_download_directory("/home/seluser/Downloads/")
set_screenshot_directory("/home/seluser/Screenshots/")

def account_special(): 
    if image_appeared("expirada.png") == True:
        send_action_simple(1,7)
        sname = "{}_{}".format("LOGINEXP", "JUMBO")
        log_sshot = "{}_{}".format("PRELOGIN", "JUMBO")
        screenshot_save(sname)
        tcp_send("SNDPIC1 /home/seluser/Screenshots/" + sname + ".png")
        tcp_send("SNDPIC1 /home/seluser/Screenshots/" + log_sshot + ".png")
        tcp_send("FINISH7")
        abort("Credencial login expirada.")
    else:
        pass 

obj = BBR()
obj.PORTAL = "JUMBO_SI"
obj.passid = "password"
obj.enable_error = True
obj.enable_recaptcha = True
obj.login_verify = True
obj.site_key = "6LcVYtEUAAAAALlg52jHvKf9IM8n2FvJfqHSyqxg"
obj.account_procedure = account_special
obj.run()
