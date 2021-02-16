exec open_read("/Sikulix/BBR.py")

set_imagepath("/Sikulix/Imgs/Construmart/")
set_download_directory("/home/seluser/Downloads/")
set_screenshot_directory("/home/seluser/Screenshots/")


obj = BBR()
obj.passid = "password"
obj.PORTAL = "CONSTRUMART"
obj.enable_recaptcha = True
obj.enable_newBBR = True
obj.site_key = "6Le6POkUAAAAAPrhWc5b14fntw6TCU1tRgEKaLnk"
obj.login_verify = True
obj.run()
