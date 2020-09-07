exec open_read("/Sikulix/BBR.py")

set_imagepath("/Sikulix/Imgs/Construmart/")
set_download_directory("/home/seluser/Downloads/")
set_screenshot_directory("/home/seluser/Screenshots/")


obj = BBR()
obj.passid = "password"
obj.PORTAL = "CONSTRUMART"
obj.login_verify = True
obj.run()
