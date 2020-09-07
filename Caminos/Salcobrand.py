load_template("/Sikulix/ESB.py")

set_imagepath("/Sikulix/Imgs/Salcobrand/")
set_download_directory("/home/seluser/Downloads/")
set_screenshot_directory("/home/seluser/Screenshots/")
set_min_similarity(0.8)

def mantenedor_procedure_img():
    if EXTRA != "none":
        img_name = "salcobrand_" + EXTRA + ".png"
        image_wait(img_name)
        image_click(img_name)
    else:
        image_wait("salcobrand_consumo.png")
        image_click("salcobrand_consumo.png")

obj = ESB()
obj.PORTAL = "Salcobrand"
obj.mantenedor_procedure = mantenedor_procedure_img
obj.run()
