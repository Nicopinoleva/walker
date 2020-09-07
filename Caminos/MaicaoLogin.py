set_imagepath("/Sikulix/Imgs/Maicao/")
set_download_directory("/home/seluser/Downloads/")
set_screenshot_directory("/home/seluser/Screenshots/")

PORTAL = "MAICAO"

@generic_login(incorrect="1bad_login.png", correct="1descargas.png", portal=PORTAL)
def login():
	image_click("0user.png")
	type(USERNAME)
	press(TAB)
	type(PASSWORD)
	time_wait(1000)
	image_click("0entrar.png")

open_explorer(URL_PORTAL)
login()
tcp_send("FINISH0")
close_explorer()

