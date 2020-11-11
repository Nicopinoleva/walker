set_imagepath("/Sikulix/Imgs/Ripley/")
set_download_directory("/home/seluser/Downloads/")
set_screenshot_directory("/home/seluser/Screenshots/")

portal = "RIPLEY"

def make_filename(*args, **kwargs):
    kwargs.setdefault("separator", "_")
    result = ""
    for arg in args:
        result += arg + kwargs["separator"]
    return result[:-1]

def login():
    image_click("loguser.png")
    press(TAB)
    time_wait(5000)
    type(USERNAME)
    press(TAB)
    time_wait(5000)
    type(PASSWORD)
    image_click("entrar.png")
    time_wait(2000) 
    while(1):
        result = image_wait_multiple("badlogin.png", "portalcheck.png", "elegir_prove.png")
        if result == "badlogin.png":
            #Caso de bad login
            send_action_simple(1, 1)
            sname = make_filename("ERROR", "LOGIN", portal)
            screenshot_save(sname)
            tcp_send("SNDPIC " + sname + ".png")
            tcp_send("FINISH1")
            break
        elif result in ["portalcheck.png","elegir_prove.png"]:
            #Caso de login OK
            send_action_simple(1, 0)
            tcp_send("FINISH0")
            break
        else:
            #Caso de timeout
            send_action_simple(9, 3)
            screenshot_save("Portal_didnt_load")
            tcp_send("SNDPIC /home/seluser/Screenshots/Portal_didnt_load.png")
            tcp_send("FINISH3")
            break

open_explorer(URL_PORTAL)
login()
manual_finish()
close_explorer()
