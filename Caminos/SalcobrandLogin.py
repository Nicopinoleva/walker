load_template("/Sikulix/ESB.py")

set_imagepath("/Sikulix/Imgs/Salcobrand/")
set_download_directory("/home/seluser/Downloads/")
set_screenshot_directory("/home/seluser/Screenshots/")
set_min_similarity(0.8)

obj = ESB()
obj.PORTAL = "Salcobrand"
obj.login_verify = True
obj.run()
