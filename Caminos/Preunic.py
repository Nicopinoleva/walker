load_template("/Sikulix/ESB.py")

set_imagepath("/Sikulix/Imgs/Preunic/")
set_download_directory("/home/seluser/Downloads/")
set_screenshot_directory("/home/seluser/Screenshots/")
set_min_similarity(0.8)

def mantenedor_procedure_img():
    image_wait("preunic_consumo.png")
    image_click("preunic_consumo.png")

obj = ESB()
obj.PORTAL = "Preunic"
obj.mantenedor_procedure = mantenedor_procedure_img
obj.run()
