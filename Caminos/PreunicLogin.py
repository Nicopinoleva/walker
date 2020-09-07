load_template("/Sikulix/ESB.py")

set_imagepath("/Sikulix/Imgs/Preunic/")
set_download_directory("/home/seluser/Downloads/")
set_screenshot_directory("/home/seluser/Screenshots/")
set_min_similarity(0.8)

obj = ESB()
obj.PORTAL = "Preunic"
obj.login_verify = True
obj.run()
