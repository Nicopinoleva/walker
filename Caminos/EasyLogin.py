load_template("/Sikulix/BBR.py")

set_imagepath("/Sikulix/Imgs/Easy/")
set_download_directory("/home/seluser/Downloads/")
set_screenshot_directory("/home/seluser/Screenshots/")
 
def account_special():
    if image_appeared("bloqueado.png"):
        send_action_simple(1,15)
        sname = "{}_{}".format("LOGINBLQ", "EASY")
        log_sshot = "{}_{}".format("PRELOGIN", "EASY")
        screenshot_save(sname)
        tcp_send("SNDPIC1 /home/seluser/Screenshots/" + sname + ".png")
        tcp_send("SNDPIC1 /home/seluser/Screenshots/" + log_sshot + ".png")
        tcp_send("FINISH15")
        manual_finish()

obj = BBR()
obj.PORTAL = "EASY"
obj.passid = "password"
obj.site_key = "6LcVYtEUAAAAALlg52jHvKf9IM8n2FvJfqHSyqxg"
obj.enable_recaptcha = True
obj.login_verify = True
obj.account_procedure = account_special
obj.run()
