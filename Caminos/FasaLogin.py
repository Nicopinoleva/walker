set_imagepath("/Sikulix/Imgs/Farmaciasahumada/")
set_download_directory("/home/seluser/Downloads/")
set_screenshot_directory("/home/seluser/Screenshots/")

PORTAL="FASA"

def make_filename(*args, **kwargs):
    kwargs.setdefault("separator", "_")
    result = ""
    for arg in args:
        result += arg + kwargs["separator"]
    return result[:-1]

def login():
    log_sshot = "{}_{}".format("PRELOGIN", PORTAL) 
    image_click("loguser.png")
    press(TAB)
    time_wait(5000)
    type(USERNAME)
    press(TAB)
    time_wait(5000)
    type(PASSWORD)
    pre_login_screenshot(log_sshot)
    image_click("ingresar.png")
    time_wait(2000)
    result = image_wait_multiple("badlogin.png", "comercial.png", "baduser.png")
    if result == "badlogin.png":
        #Caso de bad login
        send_action_simple(1, 1)
        sname = make_filename("ERROR", "LOGIN", PORTAL)
        screenshot_save(sname)
        tcp_send("SNDPIC1 /home/seluser/Screenshots/" + sname + ".png")
        tcp_send("SNDPIC1 /home/seluser/Screenshots/" + log_sshot + ".png")
        tcp_send("FINISH1")
        abort("Credenciales de login erroneas.")
    elif result == "comercial.png":
        #Caso de login OK
        send_action_simple(1, 0)
        matrix_set("LOGIN_CORRECT",True)
        tcp_send("FINISH0")
    elif result == "baduser.png":
        send_action_simple(1, 15)
        sname = make_filename("ERROR", "LOGIN", PORTAL)
        screenshot_save(sname)
        tcp_send("SNDPIC1 /home/seluser/Screenshots/" + sname + ".png")
        tcp_send("SNDPIC1 /home/seluser/Screenshots/" + log_sshot + ".png")
        tcp_send("FINISH15")
        abort("Credenciales de login erroneas.")
    else:
        #Caso de timeout
        send_action_simple(9, 3)
        raise ImageNotPresentException("portalcheck.png")


open_explorer(URL_PORTAL)
login()
close_explorer()