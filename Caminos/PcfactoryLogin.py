set_imagepath("/Sikulix/Imgs/PCFactory/")
set_download_directory("/home/seluser/Downloads/")
set_screenshot_directory("/home/seluser/Screenshots/")

def make_filename(*args, **kwargs):
	kwargs.setdefault("separator", "_")
	result = ""
	for arg in args:
		result += arg + kwargs["separator"]
	return result[:-1]


def pcfactory_generic_login(**kwargs):
	def internal_dec(func):
		def inner(*inargs, **inkwargs):
			res = func(*inargs, **inkwargs)
			result = image_wait_multiple(kwargs["incorrect"], kwargs["correct"])
			if result == kwargs["incorrect"]:
				#Caso de bad login
				send_action_simple(1, 1)
				sname = make_filename("ERROR", "LOGIN", kwargs["portal"])
				screenshot_save(sname)
				tcp_send("SNDPIC1 /home/seluser/Screenshots/" + sname + ".png")
				tcp_send("FINISH1")
				manual_finish()
			elif result == kwargs["correct"]:
				#Caso de login OK
				send_action_simple(1, 0) 
				tcp_send("FINISH0")
				manual_finish()
			else:
				#Caso de timeout
				send_action_simple(9, 3)
                                screenshot_save("Portal_didnt_load.png")
                                tcp_send("SNDPIC1 /home/seluser/Screenshots/Portal_didnt_load.png")
                                tcp_send("FINISH3")
                                manual_finish() 
			return res
		return inner
	return internal_dec

portal = "PCFACTORY"

@pcfactory_generic_login(incorrect="badlogin.png", correct="ventas.png", portal=portal)
def login():
	image_click("loguser.png")
	type(USERNAME)
	press(TAB)
	type(PASSWORD)
	press(ENTER)


open_explorer(URL_PORTAL)
login()
close_explorer()
