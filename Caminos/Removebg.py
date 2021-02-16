set_imagepath("/Sikulix/Imgs/Removebg/")
set_download_directory("/home/seluser/Downloads/")
open_explorer(URL_PORTAL)
site_key = "51a23611-21cb-4c6e-bcbf-84ee5c14d9ad"
while(True):
    newpic = tcp_send_recieve("GETFIL")
    print(newpic)
    if len(newpic<7):
        break
    else:
        temp = newpic.split(" ")
        image_click("upload.png")
        if not image_appeared("preview.png"):
            image_click("directory.png")
        time_wait(5000)
        press_with_ctr("f")
        type(temp[0])
        press(ENTER)
        time_wait(2000)
        if image_appeared("hcaptcha.png"):
            hcaptcha(site_key)
        image_click("download.png")
        image_wait("save.png")
        time_wait(1000)
        type(get_download_directory()+temp[1])
        time_wait(1000)
        type(ENTER)
        image_click("close.png")