# ==== VERSION 1.0.0 ==


# ==== ARGUMENT LOAD ====

def abort(message=""):
	raise AbortedException

def manual_finish(message=""):
	raise ManualFinishException

def value_or_zero(lst, index):
	if len(lst) > index:
		return lst[index]
	return "0"

if len(OPTION_ARGS) < 10:
	raise TooFewArgumentsException("Tiene que enviar al menos 10 argumentos.")
OPTION_FILENAME = OPTION_ARGS[0]
RUT_EMPRESA = OPTION_ARGS[1]
USERNAME = OPTION_ARGS[2]
PASSWORD = OPTION_ARGS[3]
NOMBRE_EMPRESA = OPTION_ARGS[4]
URL_PORTAL = OPTION_ARGS[5]
OPTION_HOST = OPTION_ARGS[6]
OPTION_LOG_ID = OPTION_ARGS[7]
OPTION_RETRIES = int(OPTION_ARGS[8])
TIMEOUT = OPTION_ARGS[9]
NUM_LOCALES = value_or_zero(OPTION_ARGS, 10)
AVANZAR = value_or_zero(OPTION_ARGS, 11)
OPTION_TRACE_EVERY  = value_or_zero(OPTION_ARGS, 12)
if OPTION_TRACE_EVERY == 0:
	OPTION_TRACE_EVERY = 10
EXTRA = OPTION_ARGS[13]
NUM_SSHOTS = OPTION_ARGS[14]
DATE = OPTION_ARGS[15]
MATRIX = [str(char) for char in OPTION_ARGS[16]]

IMAGE_BASED_FUNCTIONS_TIMEOUT = int(TIMEOUT) #Timeout hook

print "Username:", USERNAME
print "Password:", PASSWORD
# ==== MATRIX FUNCTIONS ====

MATRIX_KEYWORD_DICT = {}

def matrix_register(key):
    if len(MATRIX_KEYWORD_DICT) > 20:
        raise Exception("No se pueden registrar mas de 20 llaves en la matriz.")
    if "COUNT" in key:
        res = [val for keys, val in MATRIX_KEYWORD_DICT.items() if "COUNT" in keys]
        MATRIX_KEYWORD_DICT[key] = 5 + len(res) + len(MATRIX_KEYWORD_DICT)
    else:
        MATRIX_KEYWORD_DICT[key] = len(MATRIX_KEYWORD_DICT)

def matrix_set(key, bol):
    global MATRIX
    if bol == True:
            MATRIX[MATRIX_KEYWORD_DICT[key]] = '1'
    elif bol == False:
            MATRIX[MATRIX_KEYWORD_DICT[key]] = '0'
    else:
        if int(bol) <= 9:
            MATRIX[MATRIX_KEYWORD_DICT[key]] = str(bol)
        else:
            MATRIX[MATRIX_KEYWORD_DICT[key]] = list(str(bol))[0]
            letter = chr(int(list(str(bol))[1])+97)
            MATRIX[MATRIX_KEYWORD_DICT[key]+1] = letter
    tcp_send("MATRIX" + "".join(MATRIX))

def matrix_get(key):
    if "COUNT" in key:
        if MATRIX[MATRIX_KEYWORD_DICT[key]+1] != '0':
            num = []
            num.append(MATRIX[MATRIX_KEYWORD_DICT[key]])
            num.append(str(ord(MATRIX[MATRIX_KEYWORD_DICT[key]+1]) - 97))
            return int(''.join(num))
        else:
            return int(MATRIX[MATRIX_KEYWORD_DICT[key]])
    else:
        return int(MATRIX[MATRIX_KEYWORD_DICT[key]])

# ==== RETROCOMPATIBILITY ====

def hover(img):
	return image_hover(img)

# ==== ACTIONS ====

def send_action(action):
	def placeholder():
		pass
	func = action(placeholder)
	return func()

def send_action_simple(action, status, num_files=0, info=0):
	if info==0:
                if action==1 and status==0:
                    tcp_send("LOGOKA into log (log_id, acc_id, stat_id, num_files) values ("+OPTION_LOG_ID+", "+str(action)+", "+str(status)+", "+str(num_files)+");")
                elif action==1 and (status==1 or status==7 or status==15 or status==16):
                    tcp_send("LOGERR into log (log_id, acc_id, stat_id, num_files) values ("+OPTION_LOG_ID+", "+str(action)+", "+str(status)+", "+str(num_files)+");")
                else:
		    tcp_send("INSERT into log (log_id, acc_id, stat_id, num_files) values ("+OPTION_LOG_ID+", "+str(action)+", "+str(status)+", "+str(num_files)+");")
	else:
		tcp_send("INSERT into log (log_id, acc_id, stat_id, num_files, info) values ("+OPTION_LOG_ID+", "+str(action)+", "+str(status)+", "+str(num_files)+", "+str(info)+");")

#File tracker
#def _DOWNLOAD_TRACKER_start():
	#import threading
	#def _DOWNLOAD_TRACKER():
		#log("DEBUG", "_DOWNLOAD_TRACKER ha empezado.")
		#count_record = 0
		#while _DOWNLOAD_TRACKER:
			##Revisa los archivos cada 1 segundo
			#time_wait(1 * SECONDS)
			#count = get_downloads_count()
			#if (count - count_record) / OPTION_TRACE_EVERY >= 1:
				#count_record = count
				#send_action(action_nuevo_archivo)
		#log("DEBUG", "_DOWNLOAD_TRACKER ha terminado.")
	#threading.Thread(target=_DOWNLOAD_TRACKER).start()
##Action decorators
##Private actions
#def _action_simple(func, action_code, status_code, num_files=0):
	#def inner(*args, **kwargs):
		#func(*args, **kwargs)
		#tcp_send("INSERT into log (log_id, acc_id, stat_id, num_files) values ("+OPTION_LOG_ID+", "+str(action_code)+", "+str(status_code)+", "+str(num_files)+");")
		#log("INFO", "SENT ACTION " + str(action_code))
    	#return inner
#def _action_files_reporter(func, action_code, error_code):
	#def inner(*args, **kwargs): 
		##try:
		#func(*args, **kwargs)
		#tcp_send("INSERT into log (log_id, acc_id, stat_id, num_files) values (" + OPTION_LOG_ID + ", "+str(action_code)+", "+str(error_code)+", "+str(get_downloads_count(_walker.DEFAULT_DOWNLOAD_DIRECTORY))+");")
		#log("INFO", "SENT ACTION " + str(action_code))
		##except Exception as e:
		##	tcp_send("INSERT into log values (" + OPTION_LOG_ID + ", "+str(action_code)+", "+str(error_code)+", "+str(get_files_count(_walker.DEFAULT_DOWNLOAD_DIRECTORY))+");")
		##	tcp_send("FINISH")
		##	close_explorer()
		##	global _DOWNLOAD_TRACKER
		##	_DOWNLOAD_TRACKER = False
		##	log("ERROR", "No se ha podido completar la acción " + str(action_code))
		##	raise Exception(e)
    	#return inner
#Public actions
#def action_init(func):
	#return _action_simple(func, 0, 0)
#def action_login(func):
	#def _action_login(func):
		#return _action_simple(func, 1, 0)
	#def _action_login_failed(func):
		#return _action_simple(func, 1, 1)
	#def inner(*args, **kwargs):
		#try:
			#func(*args, **kwargs)
			#send_action(_action_login)
		#except Exception as e:
			#log("DEBUG", "Dentro de action_login except")
			#log("ERROR", str(e))
			#send_action(_action_login_failed)
			#tcp_send("FINISH")
			#abort(str(e))
	#return inner
#def action_screenshot_1(func):
	#return _action_simple(func, 2, 0)
#def action_screenshot_2(func):
	#return _action_simple(func, 3, 0)
#def action_inicio_descarga(func):
	##Esta acción ACTIVA al file tracker!
	#global _DOWNLOAD_TRACKER
	#if not _DOWNLOAD_TRACKER:
		#_DOWNLOAD_TRACKER = True
		#_DOWNLOAD_TRACKER_start()
	#return _action_simple(func, 4, 0)
#def action_nuevo_archivo(func):
	#return _action_files_reporter(func, 5, 0)
#def action_ciclo_descarga(func):
	#return _action_files_reporter(func, 6, 0)
#def action_fin_descarga(func):
	#def _action_fin_descarga(func):
		#return _action_files_reporter(func, 7, 0)
	#def inner(*args, **kwargs):
		#func(*args, **kwargs)
		##Esta acción DESACTIVA al file tracker!
		#global _DOWNLOAD_TRACKER
		#_DOWNLOAD_TRACKER = False
		#result = send_action(_action_fin_descarga)
		#log("DEBUG", "FINISH enviado")
		#tcp_send("FINISH")
		#return result
	#return inner

#def generic_login_extended(**kwargs):
	#def internal_dec(func):
		#def inner(*inargs, **inkwargs):
			#res = func(*inargs, **inkwargs)
			#iwargs = kwargs["incorrect"] + kwargs["correct"]
			#result = image_wait_multiple(*iwargs)
			#if result in kwargs["incorrect"]:
				##Caso de bad login
				#send_action_simple(1, 1)
				#sname = "{}_{}".format("LOGIN", kwargs["portal"])
				#screenshot_save(sname)
				#tcp_send("SNDPIC1  /home/seluser/Screenshots/" + sname + ".png")
				#tcp_send("FINISH1")
				#abort("Credenciales de login erroneas.")
			#elif result in kwargs["correct"]:
				##Caso de login OK
				#if not matrix_get("LOGIN_CORRECT"):
					#send_action_simple(1, 0)
					#matrix_set("LOGIN_CORRECT", True)
			#else:
				##Caso de timeout
				#send_action_simple(9, 3)
				#raise ImageNotPresentException(str(iwargs))
			#return res
		#return inner
	#return internal_dec

def generic_login(**kwargs):
	def internal_dec(func):
		def inner(*inargs, **inkwargs):
			res = func(*inargs, **inkwargs)
			result = image_wait_multiple(kwargs["incorrect"], kwargs["correct"])
			if result == kwargs["incorrect"]:
				#Caso de bad login
				send_action_simple(1, 1)
				sname = "{}_{}".format("LOGIN", kwargs["portal"])
				screenshot_save(sname)
				tcp_send("SNDPIC1 /home/seluser/Screenshots/" + sname + ".png")
				tcp_send("FINISH1")
				abort("Credenciales de login erroneas.")
			elif result == kwargs["correct"]:
				#Caso de login OK
                                send_action_simple(1, 0)
                                if not "Login" in OPTION_FILENAME:
                                    if not matrix_get("LOGIN_CORRECT"):
                                        matrix_set("LOGIN_CORRECT", True)
                        else:
				#Caso de timeout
				send_action_simple(9, 3)
				raise ImageNotPresentException(kwargs["correct"])
			return res
		return inner
	return internal_dec

# ==== FINAL PRE-CAMINO PROCEDURE ====

SUCCESS = False

def common_abort_procedure():
	global _DOWNLOAD_TRACKER
	_DOWNLOAD_TRACKER = False
	if _EXPLORER_OPENED:
		close_explorer()

CUSTOM_IMAGE_MISSING_HANDLER = None

def default_image_missing_handler(e):
	log("ERROR", "Imagen no aparecio en pantalla: " + str(e))
	filename = str(e)[:-4]
	screenshot_save(filename)
	time_wait(1500)
	tcp_send("SNDPIC2 /home/seluser/Screenshots/" + filename + ".png")
        num_files = get_downloads_count()
	if i == OPTION_RETRIES - 1:
		#Lo que ocurre cuando se acaban los soft resets.
		action = 7
		status = 5
		tcp_send("INSERT into log (log_id, acc_id, stat_id, num_files, img) values ("+OPTION_LOG_ID+", "+str(action)+", "+str(status)+", "+str(num_files)+", '"+filename+".png')")
		tcp_send("FAILED")
	else:
		action = 7
		status = 6
		tcp_send("INSERT into log (log_id, acc_id, stat_id, num_files, img) values ("+OPTION_LOG_ID+", "+str(action)+", "+str(status)+", "+str(num_files)+", '"+filename+".png')")
		tcp_send("DUERMO"+ str(get_downloads_count()))
	common_abort_procedure()

tcp_connect(OPTION_HOST.encode("utf-8"))

if not "Login" in OPTION_FILENAME:
#Registro variables guardas en el agente
    if OPTION_FILENAME == "/Sikulix/Walmart.py":
        matrix_register("INICIADO")
        matrix_register("LOGIN_CORRECT")
        matrix_register("FILE_1_RUNNING")
        matrix_register("FILE_2_RUNNING")
        matrix_register("FILE_3_RUNNING")
        matrix_register("FILE_4_RUNNING")
        matrix_register("FILE_5_RUNNING")
        matrix_register("FILE_1_DOWNLOADED")
        matrix_register("FILE_2_DOWNLOADED")
        matrix_register("FILE_3_DOWNLOADED")
        matrix_register("FILE_4_DOWNLOADED")
        matrix_register("FILE_5_DOWNLOADED")
        matrix_register("ALL_RUNNING")
        matrix_register("FILES_DOWNLOADED")

    else:
        matrix_register("INICIADO")
        matrix_register("LOGIN_CORRECT")
        matrix_register("SSHOT_1")
        matrix_register("SSHOT_2")
        matrix_register("DOWNLOAD_STARTED")
        matrix_register("DOWNLOAD_COUNT")
        matrix_register("CYCLE_COUNT")
        matrix_register("IN_CYCLE_COUNT")

# Inicio proceso

    if not matrix_get("INICIADO"):
        send_action_simple(0, 0)
        matrix_set("INICIADO", True)
        # Update cuelogs
        if EXTRA == 'DAILY' or EXTRA == 'WEEKLY' or OPTION_FILENAME == '/Sikulix/Pcfactory.py':
            tcp_send("UPDATE cuelogs set files = "+str(NUM_LOCALES)+" where log_id = "+OPTION_LOG_ID+";")
        else:
            tcp_send("UPDATE cuelogs set files = "+str(int(NUM_LOCALES)+int(NUM_SSHOTS))+" where log_id = "+OPTION_LOG_ID+";")

else:
    send_action_simple(0, 0)

# Camino launch

for i in range(OPTION_RETRIES):
	log("INFO", "Intento " + str(i + 1) + "/ " + str(OPTION_RETRIES))
	try:
		exec(_preprocess(open(OPTION_FILENAME).read()))
		log("INFO", "Camino finalizado correctamente.")
		_DOWNLOAD_TRACKER = False
		SUCCESS = True
		break
	except ImageNotPresentException as e:
		#Este es el unico caso que permite un soft reset.
		if CUSTOM_IMAGE_MISSING_HANDLER != None:
			CUSTOM_IMAGE_MISSING_HANDLER(e)
		else:
			default_image_missing_handler(e)
	except ImageNotFoundException as e:
		log("ERROR", "Archivo no existe: " + str(e))
		common_abort_procedure()
		break
	except AbortedException as e:
		log("ERROR", "Aborted")
		common_abort_procedure()
		break
	except ManualFinishException as e:
		log("INFO", "Camino finalizado correctamente.")
		common_abort_procedure()
		break
	except Exception as e:
		log("ERROR", "Error desconocido. ")
		traceback.print_exc()
		common_abort_procedure()
		break
