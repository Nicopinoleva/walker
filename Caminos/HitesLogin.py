exec open_read("/Sikulix/BBR.py")

set_imagepath("/Sikulix/Imgs/Hites/")
set_download_directory("/home/seluser/Downloads/")
set_screenshot_directory("/home/seluser/Screenshots/")

obj = BBR()
obj.PORTAL = "HITES"
obj.passid = "password"
obj.site_key = "6Le6POkUAAAAAPrhWc5b14fntw6TCU1tRgEKaLnk"
obj.login_verify = True
obj.enable_recaptcha = True
obj.run()
