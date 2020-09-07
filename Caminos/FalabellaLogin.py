load_template("/Sikulix/TRIO.py")

set_imagepath("/Sikulix/Imgs/Falabella/")
set_download_directory("/home/seluser/Downloads/")
set_screenshot_directory("/home/seluser/Screenshots/")

obj = TRIO()
obj.PORTAL = "FALABELLA"
obj.login_verify = True
if '+' in RUT_EMPRESA:
    obj.rut = RUT_EMPRESA.split("+")
else:
    obj.rut = RUT_EMPRESA
obj.pop_up = True
obj.run()
