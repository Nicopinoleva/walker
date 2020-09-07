exec open_read("/Sikulix/BBR.py")

set_imagepath("/Sikulix/Imgs/Paris/")
set_download_directory("/home/seluser/Downloads/")
set_screenshot_directory("/home/seluser/Screenshots/")

obj = BBR()
obj.PORTAL = "PARIS"
obj.login_verify = True
obj.passid = "password"
obj.run()
