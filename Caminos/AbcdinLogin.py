exec open_read("/Sikulix/BBR.py")

set_imagepath("/Sikulix/Imgs/ABCDin/")
set_download_directory("/home/seluser/Downloads/")
set_screenshot_directory("/home/seluser/Screenshots/")

def account_special():
    result = image_wait_multiple("bloqueado.png", "desactivado.png")
    if result == "bloqueado.png":
        send_action_simple(1,15)
        sname = "{}_{}".format("LOGINBLQ", "ABCDIN")
        log_sshot = "{}_{}".format("PRELOGIN", "ABCDIN")
        screenshot_save(sname)
        tcp_send("SNDPIC1 /home/seluser/Screenshots/" + sname + ".png")
        tcp_send("SNDPIC1 /home/seluser/Screenshots/" + log_sshot + ".png")
        tcp_send("FINISH15")
        manual_finish()
    elif result == "desactivado.png":
        send_action_simple(1,16)
        sname = "{}_{}".format("LOGINDAC", "ABCDIN")
        log_sshot = "{}_{}".format("PRELOGIN", "ABCDIN")
        screenshot_save(sname)
        tcp_send("SNDPIC1 /home/seluser/Screenshots/" + sname + ".png")
        tcp_send("SNDPIC1 /home/seluser/Screenshots/" + log_sshot + ".png")
        tcp_send("FINISH16")
        manual_finish()

ABCDin = BBR()
ABCDin.PORTAL = "ABCDIN"
ABCDin.passid = "password"
ABCDin.enable_newBBR = True
ABCDin.enable_recaptcha = True
ABCDin.site_key = "6Le6POkUAAAAAPrhWc5b14fntw6TCU1tRgEKaLnk"
ABCDin.login_verify = True
ABCDin.account_procedure = account_special
ABCDin.run()
