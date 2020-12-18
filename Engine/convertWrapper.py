#convertWrapper  V1.00.00
#define VERSION V1.00.00

import os
import csv
import sys
from datetime import datetime
from operator import itemgetter

# Variables globales
max_date = '1000-01-01'
min_date = '3000-01-01'
max_date = datetime.strptime(max_date, "%Y-%m-%d")
min_date = datetime.strptime(min_date, "%Y-%m-%d")

def convertFile (headers, encode, tipo_archivo, 
				formato_archivo, orden_columna,
				delimitador, header, formato_fecha, ruta,
				conversion_un, decimal_un, conversion_mon, 
				decimal_mon, nombre_archivo):
	columnas = splitList (orden_columna)

	# Manual ruta (definida en parametros)
	# ruta = 'D:/Documents/rpro/ProyectoOpAuto/Codes/Validador/JUMBO/' # Archivo de entrada
	
	# Parametrizar (Carpeta de cliente y nombre del retailer) ruta_in
	try:
		files = os.listdir(ruta)
	except Exception as excep:
		resultado = exceptionDefinition(excep, 50)
		return resultado # Problema con ruta de archivo
	#print(files)
	if not files:	# Comprobacion de existencia de archivos
		noExist = str("["+ str(datetime.now().strftime("%H:%M:%S"))+"]"+"[ERR]"+"Error:"+ "60"+" - No existen archivos en carpeta")
		return noExist
	
	newRow = []

	for name in files: # Parametrizar nombres
		if(nombre_archivo == name):
			nameIn = ruta + name # Archivo de entrada
			nameOut = useExtensionCsv (ruta + 'Z'+ name) # Archivo de salida
			deleteOldFiles (nameOut)
			deleteOldFiles (nameOut.replace ('Z','SORTEDZOLBIT', 1))
			try:
				with open (nameOut, 'w', newline = '', encoding = encode) as f_out, open (nameIn, "r", newline = '', encoding = encode) as f_in: # Open in and out files
					writeHeader = csv.DictWriter (f_out, fieldnames = headers) # Escritura de headers
					writeHeader.writeheader ( ) # Escritura de headers
					csv_read = checkDelimiter (f_in, delimitador) #Fix \t delimiter, reader function
					writeFile = csv.writer (f_out, delimiter = ',')
					checkHeader (header, csv_read) # Skip header if exist

					for row in csv_read: # Escritura de filas
						for col in columnas:
							if (col == -1):
								newRow.append ('null')
							else:
								newRow.append (row[col])
						
						if (newRow[0] == ''): #Especial para lider por fechas vacias
							newRow.clear ( )
							continue
						if (cleanNoUnitRow (newRow) == 1): #Especial para lider por ventas e inventarios vacios
							newRow.clear ( )
							continue
						try:
							newRow = conversionUnMon (newRow, conversion_un, decimal_un, conversion_mon, decimal_mon) # Conviente un y mon
							newRow = useDate (newRow, formato_fecha) # Formatea fecha
							writeFile.writerow (newRow) # Escribe nueva fila
							maxMinDate (newRow) # Obtiene fecha max y min de fila (para nombre final)
							newRow.clear ( ) # Limpia newRow
						except Exception as excep:
							resultado = exceptionDefinition(excep, 40)
							return resultado # Problema con post procesado de filas
			except Exception as excep:
				resultado = exceptionDefinition(excep, 20)
				return resultado # Problema con apertura de archivos
			try:
				newNameOut = renameDate (nameOut) # Obtiene nombre de archivo con fechas reales
				os.replace (nameOut, newNameOut) # Renombra con fechas reales
				sortedZolbit (newNameOut, headers, encode) # Ordena archivo Zolbit
				resetMinMaxDate ( ) # Reset de fechas min y max
				return (str("["+ str(datetime.now().strftime("%H:%M:%S"))+"]"+"[INFO]"+"Convertido:0 - Ejecutado exitosamente"))
				#return filanizado # Archivo procesado correctamente
			except Exception as excep:
				resultado = exceptionDefinition(excep, 30)
				return (resultado) # Problema generacion de archivo
	noEsta = str("["+ str(datetime.now().strftime("%H:%M:%S"))+"]"+"[ERR]"+"Error:"+ "70"+" - No se encuentra archivo")
	return(noEsta)

def exceptionDefinition (excep, errCode):
	exc_type, exc_obj, exc_tb = sys.exc_info()
	fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
	resultadoExcept = "["+str(datetime.now().strftime("%H:%M:%S"))+"]"+"[ERR]"+"Error:"+ str(errCode)+" - "+ str(excep)+ " Modulo: "+ str(fname)+ " Linea: "+ str(exc_tb.tb_lineno)
	return(resultadoExcept)
	
def deleteOldFiles (nameOut):
	try:
		os.remove (nameOut)
	except:
		pass

def splitList (lista):
	columnas = lista.split(',')
	columnas = list (map (int, columnas))
	return columnas

def useExtensionCsv (name):
	return name.replace ('.txt','.csv')

def checkHeader (header, csv_read):
	if (header == '1'):
		return next (csv_read)
	else:
		pass

def checkDelimiter (f_in, delimitador):
	if (delimitador == 'St'):
		csv_read = csv.reader (f_in, delimiter = '\t') #Fix \t delimiter
		return csv_read
	if (delimitador == 'S1'):
		csv_read = csv.reader (f_in, delimiter = ',')
		return csv_read
	if (delimitador == 'S2'):
		csv_read = csv.reader (f_in, delimiter = '|')
		return csv_read
	else:
		csv_read = csv.reader (f_in, delimiter = delimitador)
		return csv_read

def conversionUnMon (newRow, conversion_un, decimal_un, conversion_mon, decimal_mon):
	for i in range (0, len (newRow)):
		if (newRow[i] == 'null' or newRow[i] == ''):
			continue
		if (i in [7,8,10,11]):
			#print(newRow[i], type(newRow[i]))
			newRow[i] = (int(float(newRow[i])) * int(conversion_mon)) / (pow (10, int(decimal_mon)))
		elif (i in [6,9]):
			#print(newRow[i], type(newRow[i]))
			newRow[i] = (int(float(newRow[i])) * int(conversion_un)) / (pow (10, int(decimal_un)))
	return (newRow)

def useDate (newRow, formato_fecha):
	if (newRow[0] in ['null', ''] or newRow[1] in ['null', '']):
		return newRow
	if ('-' in newRow[0]):
		delimita = '-'
	elif ('/' in newRow[0]):
		delimita = '/'
	elif ('\\' in newRow[0]):
		delimita = '\\'
	if (formato_fecha == 'yyyy-mm-dd'):
		dateRowIni = newRow[0].split (delimita)
		dateRowFin = newRow[1].split (delimita)
		newRow[0] = dateRowIni[0] + '-' + dateRowIni[1] + '-' + dateRowIni[2]
		newRow[1] = dateRowFin[0] + '-' + dateRowFin[1] + '-' + dateRowFin[2]
		return newRow
	if (formato_fecha == 'dd-mm-yyyy'):
		dateRowIni = newRow[0].split (delimita)
		dateRowFin = newRow[1].split (delimita)
		newRow[0] = dateRowIni[2] + '-' + dateRowIni[1] + '-' + dateRowIni[0]
		newRow[1] = dateRowFin[2] + '-' + dateRowFin[1] + '-' + dateRowFin[0]
		return newRow
	if(formato_fecha == 'yyyy-mm-dd-al-yyyy-mm-dd'):
		dateRowIni = (newRow[0].split (' al '))[0].split (delimita)
		dateRowFin = (newRow[1].split (' al '))[1].split (delimita)
		newRow[0] = dateRowIni[0] + '-' + dateRowIni[1] + '-' + dateRowIni[2]
		newRow[1] = dateRowFin[0] + '-' + dateRowFin[1] + '-' + dateRowFin[2]
		return newRow
	else:
		return newRow

def cleanNoUnitRow (newRow):
	if(newRow[6] in ["0.000000", "null"] and newRow[7] in ["0.000000", "null"] and 
	   newRow[8] in ["0.000000", "null"] and newRow[9] in ["0.000000", "null"] and 
	   newRow[10] in ["0.000000", "null"] and newRow[11] in ["0.000000", "null"]):
	   return 1
	else:
		return 0

def maxMinDate (newrow):
	fecha_ini = datetime.strptime(newrow[0], "%Y-%m-%d")
	fecha_fin = datetime.strptime(newrow[1], "%Y-%m-%d")
	global min_date, max_date
	fecha_aux = fecha_ini

	if (fecha_ini > fecha_fin): # Remoto caso de fechas invertidas
		fecha_ini = fecha_fin
		fecha_fin = fecha_aux
	if(fecha_ini < min_date):
		min_date = fecha_ini
	if(fecha_fin > max_date):
		max_date = fecha_fin

def renameDate (nameOut):
	global max_date, min_date
	fecha_min = min_date.strftime ("%Y/%m/%d").replace ('/', '')
	fecha_max = max_date.strftime ("%Y/%m/%d").replace ('/', '')
	nombre_fecha = nameOut.split ("_")
	newNameOut = ""
	
	for element in range(0, len (nombre_fecha)):
		if(element not in (0, 1, 2)):
			newNameOut += "_" + nombre_fecha[element]
		elif(element == 0):
			newNameOut += nombre_fecha[element]
		elif(element == 1):
			newNameOut += "_" + fecha_min
		elif(element == 2):
			newNameOut += "_" + fecha_max
	return (newNameOut)

def resetMinMaxDate ( ):
	global max_date, min_date
	max_date = '1000-01-01'
	min_date  = '3000-01-01'
	max_date = datetime.strptime (max_date, "%Y-%m-%d")
	min_date = datetime.strptime (min_date, "%Y-%m-%d")

def sortedZolbit (nameOut, headers, encode):
	with open (nameOut, 'r', newline='', encoding = encode) as csvOut, open (nameOut.replace ('Z','SORTEDZOLBIT', 1),'w', newline='', encoding = encode) as csvSorted:
		readerOut = csv.reader (csvOut, delimiter=",")
		readerOut = sorted (readerOut, key = itemgetter (0,2,3))# Ordena en 3, 2, 0, codigo_plu, codigo_local, fecha_inicio
		writerSorted = csv.writer (csvSorted)
		writeHeader = csv.DictWriter (csvSorted, fieldnames = headers) # Escribe headers
		writeHeader.writeheader ( ) # Escribe headers
		for sorted_row in readerOut: # Escribe filas ordenadas
			if (sorted_row == headers):
				continue
			writerSorted.writerow (sorted_row)
	os.replace (nameOut.replace ('Z','SORTEDZOLBIT', 1), nameOut)