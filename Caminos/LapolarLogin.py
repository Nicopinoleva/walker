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
        tcp_send("SNDPIC1 /home/seluser/Screenshots/" + log_sshot + ".png")
        tcp_send("SNDPIC1 /home/seluser/Screenshots/" + sname + ".png")
        tcp_send("FINISH15")
        manual_finish()
    else:
        pass 

obj = BBR()
obj.PORTAL = "LAPOLAR"
obj.passid = "formLogin:txt_Password"
obj.login_verify = True
obj.account_procedure = account_special
obj.run()
