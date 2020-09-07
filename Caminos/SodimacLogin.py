load_template("/Sikulix/TRIO.py")

set_imagepath("/Sikulix/Imgs/Sodimac/")
set_download_directory("/home/seluser/Downloads/")
set_screenshot_directory("/home/seluser/Screenshots/")

obj = TRIO()
obj.PORTAL = "Sodimac"
obj.pop_up = False
obj.login_verify = True
if '+' in RUT_EMPRESA:
    obj.rut = RUT_EMPRESA.split("+")
else:
    obj.rut = RUT_EMPRESA
obj.run()
