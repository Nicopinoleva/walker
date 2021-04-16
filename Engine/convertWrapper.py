#convertWrapper  V1.00.00
#define VERSION V1.00.00

import os
import csv
import sys
from datetime import datetime, timedelta
from operator import itemgetter
from decimal import *
import re
from shutil import copyfile
import xlrd # pip install xlrd==1.2.0

# Variables globales
max_date = '1000-01-01'
min_date = '3000-01-01'
max_date = datetime.strptime(max_date, "%Y-%m-%d")
min_date = datetime.strptime(min_date, "%Y-%m-%d")
#getcontext().prec = 7

# Funcion Principal
def convertFile (headers, encode, tipo_archivo, 
				formato_archivo, orden_columna,
				delimitador, header, formato_fecha, ruta,
				conversion_un, decimal_un, conversion_mon, 
				decimal_mon, nombre_archivo):

	# Caso especial solo copiar archivos y terminar programa
	if(tipo_archivo == "CP"):
		copyfile ( ruta + nombre_archivo, ruta + "Z" + nombre_archivo )
		return (str("["+ str(datetime.now().strftime("%H:%M:%S"))+"]"+"[INFO]"+"Convertido;0 - Ejecutado exitosamente (Copiado)"))

	columnas, siglaLoc = splitList (orden_columna) # Crea lista de listas con información de orden de columnas (ej. 7 listas de orden de columna para archivos semanales de TRIO)

	# Data para posiciones en archivos TRIO
	posDatosTrio = orden_columna.split(",")
	datosTrio_VENTA_UNIDADES = int (posDatosTrio[7]) - 1
	datosTrio_VENTA_PESOS = int (posDatosTrio[7])
	datosTrio_STOCK_CONTABLE_FISICO = int (posDatosTrio[7]) + 1

	# Verificación de archivos en ruta
	resultado = verifyFilesInFolder (ruta)
	if(resultado != 0):
		return resultado

	# Creacion de csv auxiliares para ciertos archivos b2b
	try:
		nombre_archivo, formato_archivo = convertXlsHtml (tipo_archivo, formato_archivo, nombre_archivo, ruta) # Crea archivo csv desde uno html de extension xls
		nombre_archivo, formato_archivo = csvFromXlsx (tipo_archivo, formato_archivo, nombre_archivo, ruta) # Crea archivo csv desde uno xlsx
	except Exception as excep:
		resultado = exceptionDefinition(excep, 80) # Error en creacion de archivos csv auxiliares
		return resultado 

	try:
		rangoFechas = getFileDateNames (nombre_archivo)
	except Exception as excep:
		resultado = exceptionDefinition(excep, 90) # Error en obtencion de fechas desde archivo B2B
		return resultado 

	nameOut = []
	nameIn = ruta + nombre_archivo # Archivo de entrada
	nameOut.append(useExtensionCsv (ruta + 'Z'+ nombre_archivo))# Archivo de salida
	deleteOldFiles (nameOut[0])
	deleteOldFiles (nameOut[0].replace ('Z','SORTEDZOLBIT', 1))

	daysInFile = 1
	if(tipo_archivo == 'ST'):
		daysInFile = 7
		nameOutAux = ["" for x in range(7)]
		for rep in range(0,7):
			auxName = nombre_archivo.split("_")
			auxName[1] = rangoFechas[rep]
			auxName[2] = rangoFechas[rep]
			auxName[3] = ""
			nameOutAux[rep] = useExtensionCsv (ruta + 'Z'+ '_'.join(auxName).replace("__","_"))

		nameOut = nameOutAux
	
	retailer = getRetailerNombreArchivo(nombre_archivo) # Obtiene retailer desde nombre de archivo
	ventaInventario = getVentaInventario(nombre_archivo) # 	

	
	files = os.listdir(ruta)
	dia = 0
	newRow = []
	while(dia < daysInFile):
		for name in files: # Busca archivo en lista de archivos disponibles
			if(nombre_archivo == name):
				try:
					deleteOldFiles (nameOut[dia])
					deleteOldFiles (nameOut[dia].replace ('Z','SORTEDZOLBIT', 1))
					#print("--",nameOut[dia])
					with open (nameOut[dia], 'w', newline = '', encoding = encode) as f_out, open (nameIn, "r", newline = '', encoding = encode) as f_in: # Open in and out files
						#print("2--",nameOut[dia], nameIn)
						writeHeader = csv.DictWriter (f_out, fieldnames = headers) # Escritura de headers
						writeHeader.writeheader ( ) # Escritura de headers
						csv_read = checkDelimiter (f_in, delimitador) #Fix \t delimiter, reader function
						writeFile = csv.writer (f_out, delimiter = ',') # Define delimitador de archivo Zolbit
						checkHeader (header, csv_read) # Skip header if exist
						try:
							for row in csv_read: # Escritura de filas
								#print(row)
								if(not row):
									continue
								for col in columnas[dia]:
									if (col == -1):
										newRow.append ('null')
									else:
										row[col] = stripSpacesStartEnd (row[col]) # Elimina espacios al inicio y fin
										newRow.append (row[col])
								
								#if (newRow[0] == ''): # Elimina filas cuyas fechas sean caracter vacio (Lider)
								#	newRow.clear ( )
								#	continue
								if (cleanNoUnitRow (newRow) == 1): # Elimina filas con ventas e inventarios vacios
									newRow.clear ( )
									continue
								newRow = conversionVentaVariosDias (newRow, row, tipo_archivo, datosTrio_VENTA_UNIDADES) # Conversion de venta para archivos del TRIO,  17 = vta_unidades
								newRow = modificaInvTrio (newRow, daysInFile, dia, tipo_archivo, row, datosTrio_VENTA_UNIDADES, datosTrio_VENTA_PESOS, datosTrio_STOCK_CONTABLE_FISICO) # Elimina las row de inventarios, a no ser que sea ultimo archivo trio
								
								if (cleanNoUnitRow (newRow) == 1): # Segunda eliminacion de filas con valores vacios (se realiza especialmente para archivos TRIO)
									newRow.clear ( )
									continue

								newRow = conversionUnMon (newRow, conversion_un, decimal_un, conversion_mon, decimal_mon) # Conviente un y mon
								newRow = useDate (newRow, formato_fecha, nameOut[dia]) # Formatea fecha, si fila no tiene fecha, da la de nombre de archivo final

								newRow = putSiglaLocal (newRow, row, retailer, ventaInventario, siglaLoc) # Inserta sigla de retailer a codigo local (para diferenciar locales, ej: En SMU, diferenciar unimarc con ok market)

								writeFile.writerow (newRow) # Escribe nueva fila
								maxMinDate (newRow, nombre_archivo) # Obtiene fecha max y min de fila
								newRow.clear ( ) # Limpia newRow
						except Exception as excep:
							resultado = exceptionDefinition(excep, 40)
							return resultado # Problema con post procesado de filas
				except Exception as excep:
					resultado = exceptionDefinition(excep, 20)
					return resultado # Problema con apertura de archivos
				try:
					#newNameOut = renameDate (nameOut[dia], daysInFile) # Obtiene nombre de archivo con fechas reales
					#os.replace (nameOut[dia], newNameOut) # Renombra con fechas reales
					
					newNameOut = nameOut[dia]
					sortedZolbit (newNameOut, headers, encode) # Ordena archivo Zolbit

					resetMinMaxDate ( ) # Reset de fechas min y max
					reduceNameDates (newNameOut) # Elimina tercera fecha en nombre en caso de existir
					if(dia + 1 == daysInFile):
						deleteInterFiles (tipo_archivo, ruta + nombre_archivo)
						return (str("["+ str(datetime.now().strftime("%H:%M:%S"))+"]"+"[INFO]"+"Convertido;0 - Ejecutado exitosamente"))
							#return filanizado # Archivo procesado correctamente
				except Exception as excep:
					resultado = exceptionDefinition(excep, 30)
					return (resultado) # Problema generacion de archivo
		dia += 1
	noEsta = str("["+ str(datetime.now().strftime("%H:%M:%S"))+"]"+"[ERR]"+"Error;"+ "70"+" - No se encuentra archivo")
	return(noEsta)

def exceptionDefinition (excep, errCode):

	exc_type, exc_obj, exc_tb = sys.exc_info( )
	fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
	resultadoExcept = "["+str(datetime.now().strftime("%H:%M:%S"))+"]"+"[ERR]"+"Error;"+ str(errCode)+" - "+ str(excep)+ " Modulo: "+ str(fname)+ " Linea: "+ str(exc_tb.tb_lineno)
	return(resultadoExcept)

def onlyCopyFile(tipo_archivo, ruta, nombre_archivo):
	if(tipo_archivo == "CP"):
		copyfile ( ruta + nombre_archivo, ruta + "Z" + nombre_archivo )

def conversionVentaVariosDias (newRow, row, tipo_archivo, datosTrio_VENTA_UNIDADES):

	if (tipo_archivo == "ST"):
		unidadesPeriodo = row[datosTrio_VENTA_UNIDADES]
		try:
			ventaDia = ( float(newRow[7]) / (int(unidadesPeriodo)) * float(newRow[6]) )
		except:
			ventaDia = 0 
		newRow[7] = float(ventaDia)

	if (tipo_archivo == "DT"):
		unidadesPeriodo = row[datosTrio_VENTA_UNIDADES]
		try:
			ventaDia = ( float(newRow[7]) / (int(unidadesPeriodo)) * float(newRow[6]) )
		except:
			ventaDia = 0 
		newRow[7] = float (ventaDia)
	return (newRow)

def getRetailerNombreArchivo(nombre_archivo):

	retailer = re.findall(r"_[0-9]{8}_[0-9]{8}_[A-Z]{2}_(.*?)_", nombre_archivo)[0]
	#print(retailer)
	return retailer

def getVentaInventario (nombre_archivo):

	ventaInventario = re.split('[_.]', nombre_archivo)[-2]
	if ("INV" in ventaInventario):
		return ventaInventario
	elif ("CSV" in ventaInventario):
		return ventaInventario
	elif ("DIA" in ventaInventario):
		return ventaInventario
	

def modificaInvTrio (newRow, daysInFile, dia, tipo_archivo, row, datosTrio_VENTA_UNIDADES, datosTrio_VENTA_PESOS, datosTrio_STOCK_CONTABLE_FISICO):

	if (tipo_archivo == "ST" and dia + 1 == daysInFile):
		vta_unid = row[datosTrio_VENTA_UNIDADES]
		vta_pesos = row[datosTrio_VENTA_PESOS]
		stock = row[datosTrio_STOCK_CONTABLE_FISICO]
		try:
			totalStockDia = (int(float(vta_pesos)) / (float(vta_unid)) * int(stock))
		except:
			totalStockDia = 0
		newRow[10] = totalStockDia

	if (tipo_archivo == "DT"):
		vta_unid = row[datosTrio_VENTA_UNIDADES]
		vta_pesos = row[datosTrio_VENTA_PESOS]
		stock = row[datosTrio_STOCK_CONTABLE_FISICO]
		try:
			totalStockDia = (int(float(vta_pesos)) / (float(vta_unid)) * int(stock))
		except:
			totalStockDia = 0
		newRow[10] = totalStockDia

	elif ((tipo_archivo == "ST") and dia + 1 < daysInFile):
		newRow[9] = "null"
		newRow[10] = "null"

	return newRow

def conversionUnMon (newRow, conversion_un, decimal_un, conversion_mon, decimal_mon):

	getcontext().prec = 7
	for i in range (0, len (newRow)):
		if (newRow[i] == 'null' or newRow[i] == ''):
			continue

		if (i in [7,8,10,11]): # Montos
			#print(newRow[i], type(newRow[i]))
			newRow[i] = (float(newRow[i]) * int(conversion_mon)) / (pow (10, int(decimal_mon)))

		elif (i in [6,9]): # Unidades
			#print(newRow[i], type(newRow[i]))
			newRow[i] = (float(newRow[i]) * int(conversion_un)) / (pow (10, int(decimal_un)))

	return (newRow)

def getFileDateNames (nombre_archivo):

    fechaInicio = datetime.strptime (nombre_archivo.split("_")[1], "%Y%m%d")
    fechaFinal = datetime.strptime (nombre_archivo.split("_")[2], "%Y%m%d")
    delta = fechaFinal - fechaInicio
    rangoFechas = []
    for day in range(delta.days + 1):
        fecha = str((fechaInicio + timedelta(days=day)).date()).replace('-', '')
        rangoFechas.append(fecha)
    return (rangoFechas)

def reduceNameDates (nameOut):
	#print(nameOut)
	cadena = nameOut.split("_")
	uno = re.findall(r"\b(\d{8})\b", cadena[3])

	if (uno):
		cadena.pop(3)
		newNameOut = ("_".join(cadena))
		#print(newNameOut)
		os.replace (nameOut, newNameOut)

def deleteOldFiles (nameOut):
	try:
		#print("Eliminando ", nameOut)
		os.remove (nameOut)
	except:
		pass

def verifyFilesInFolder (ruta):

	try:
		files = os.listdir(ruta)
	except Exception as excep:
		resultado = exceptionDefinition(excep, 50)
		return resultado # Problema con ruta de archivo
	if not files:	# Comprobacion de existencia de archivos
		noExist = str("["+ str(datetime.now().strftime("%H:%M:%S"))+"]"+"[ERR]"+"Error;"+ "60"+" - No existen archivos en carpeta")
		return noExist
	return 0

def splitList (orden):
	
	#print(orden)
	columnas = orden.split(',')
	# Obtener posicion sigla local (elemento con *) y popear elemento
	siglaLoc = -1

	for element in range(0,len(columnas)):
		if "*" in columnas[element]:
			siglaLoc = int(columnas.pop(element).replace("*",""))
			break;

	columnasDias = []

	for indice in range(0, len(columnas)):
		if ("+" in columnas[indice]):
			dias = columnas[indice].split('+')
			valor = 0
			for elemento in dias:
				columnasDias.append((columnas[:]))
				columnasDias[valor][indice] = elemento
				columnasDias[valor] = list (map (int, columnasDias[valor]))
				valor +=1

	if(columnasDias):
		return columnasDias, siglaLoc
	else:
		columnasDias.append((list (map (int, columnas[:]))))
		return columnasDias, siglaLoc

def useExtensionCsv (name):

	return name.replace ('.txt','.csv')

def checkHeader (header, csv_read):

	if (header == '1'):
		return next (csv_read)
	else:
		pass

def stripSpacesStartEnd (value):

	value = value.strip()
	return (value)


def checkDelimiter (f_in, delimitador):

	if (delimitador == 'St'):
		csv_read = csv.reader (f_in, delimiter = '\t') #Fix \t delimiter
		return csv_read
	elif (delimitador == 'S1'):
		csv_read = csv.reader (f_in, delimiter = ',')
		return csv_read
	elif (delimitador == 'S2'):
		csv_read = csv.reader (f_in, delimiter = '|')
		return csv_read
	elif (delimitador == 'S3'):
		csv_read = csv.reader (f_in, delimiter = ';')
		return csv_read
	else:
		csv_read = csv.reader (f_in, delimiter = delimitador)
		return csv_read

def useDate (newRow, formato_fecha, nameOut):

	if (newRow[0] in ['null', ''] or newRow[1] in ['null', '']): # Caso lider, si fila no tiene fecha, le da la del ultimo dia (util para archivo inventario)
		newRow[0] = newRow[1] = str(datetime.strptime (nameOut.split("_")[2], "%Y%m%d").date())
		#newRow[1] = str(datetime.strptime (nameOut.split("_")[2], "%Y%m%d").date())
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
	elif (formato_fecha == 'dd-mm-yyyy'):
		dateRowIni = newRow[0].split (delimita)
		dateRowFin = newRow[1].split (delimita)
		newRow[0] = dateRowIni[2] + '-' + dateRowIni[1] + '-' + dateRowIni[0]
		newRow[1] = dateRowFin[2] + '-' + dateRowFin[1] + '-' + dateRowFin[0]
		return newRow
	elif(formato_fecha == 'yyyy-mm-dd-al-yyyy-mm-dd'):
		dateRowIni = (newRow[0].split (' al '))[0].split (delimita)
		dateRowFin = (newRow[1].split (' al '))[1].split (delimita)
		newRow[0] = dateRowIni[0] + '-' + dateRowIni[1] + '-' + dateRowIni[2]
		newRow[1] = dateRowFin[0] + '-' + dateRowFin[1] + '-' + dateRowFin[2]
		return newRow
	elif (formato_fecha == 'dd-MES-yyyy'):
		dateRowIni = newRow[0].split (delimita)
		dateRowFin = newRow[1].split (delimita)
		dateRowIni = mmFromMes (dateRowIni)
		dateRowFin = mmFromMes (dateRowFin) 
		newRow[0] = dateRowIni[2] + '-' + dateRowIni[1] + '-' + dateRowIni[0]
		newRow[1] = dateRowFin[2] + '-' + dateRowFin[1] + '-' + dateRowFin[0]
		return newRow
	else:
		return newRow

def mmFromMes (fecha):

	if(fecha[1] == "ENE"):
		fecha[1] = "01"
		return fecha
	if(fecha[1] == "FEB"):
		fecha[1] = "02"
		return fecha
	if(fecha[1] == "MAR"):
		fecha[1] = "03"
		return fecha
	if(fecha[1] == "ABR"):
		fecha[1] = "04"
		return fecha
	if(fecha[1] == "MAY"):
		fecha[1] = "05"
		return fecha
	if(fecha[1] == "JUN"):
		fecha[1] = "06"
		return fecha
	if(fecha[1] == "JUL"):
		fecha[1] = "07"
		return fecha
	if(fecha[1] == "AGO"):
		fecha[1] = "08"
		return fecha
	if(fecha[1] == "SEP"):
		fecha[1] = "09"
		return fecha
	if(fecha[1] == "OCT"):
		fecha[1] = "10"
		return fecha
	if(fecha[1] == "NOV"):
		fecha[1] = "11"
		return fecha
	if(fecha[1] == "DIC"):
		fecha[1] = "12"
		return fecha

def cleanNoUnitRow (newRow):

	if(newRow[6] in ["0", "0.0", "0.000000", "null", 0] and newRow[7] in ["0", "0.0", "0.000000", "null", 0] and 
		newRow[9] in ["0", "0.0", "0.000000", "null", 0] and newRow[10] in ["0", "0.0", "0.000000", "null", 0]):
		return 1
	else:
		return 0

def maxMinDate (newRow, nombre_archivo):
	
	if (newRow[0] in ["0.000000", "null"] and newRow[1] in ["0.000000", "null"]):
		fecha_ini = datetime.strptime (nombre_archivo.split("_")[1], "%Y%m%d")
		fecha_fin = datetime.strptime (nombre_archivo.split("_")[2], "%Y%m%d")

	else:
		fecha_ini = datetime.strptime(newRow[0], "%Y-%m-%d")
		fecha_fin = datetime.strptime(newRow[1], "%Y-%m-%d")

	global min_date, max_date
	fecha_aux = fecha_ini

	if (fecha_ini > fecha_fin): # Remoto caso de fechas invertidas
		fecha_ini = fecha_fin
		fecha_fin = fecha_aux
	if(fecha_ini < min_date):
		min_date = fecha_ini
	if(fecha_fin > max_date):
		max_date = fecha_fin	

def renameDate (nameOut, daysInFile):
	if(daysInFile == 1):
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
	else:
		return (nameOut)

def resetMinMaxDate ( ):
	global max_date, min_date
	max_date = '1000-01-01'
	min_date  = '3000-01-01'
	max_date = datetime.strptime (max_date, "%Y-%m-%d")
	min_date = datetime.strptime (min_date, "%Y-%m-%d")

def convertXlsHtml (tipo_archivo, formato_archivo, nombre_archivo, ruta):

	if ((tipo_archivo == "DX" or tipo_archivo == "DY") and formato_archivo == ".xls"):
		#print("Convierte Xls Html: ", ruta + nombre_archivo)
		archivo = open(ruta + nombre_archivo,"r")
		lines = archivo.readlines ( ) # Salta header
		substring = []
		pattern = "<td>(.*?)\</td>"
		for linea in lines:
			substringFound = re.findall(r"<td>(.*?)\</td>", linea)
			substring.extend(substringFound)
		cod_local = []
		desc_local = []
		cod_plu = []
		desc_plu = []
		mon = []
		unid = []
		fecha = []
		if (tipo_archivo == "DX"):
			while(substring):
				cod_local.append(substring.pop(0))
				desc_local.append(substring.pop(0))
				cod_plu.append(substring.pop(0))
				desc_plu.append(substring.pop(0))
				mon.append(substring.pop(0))
				unid.append(substring.pop(0))
				fecha.append(substring.pop(0))
		if (tipo_archivo == "DY"):
			while(substring):
				cod_plu.append(substring.pop(0))
				desc_plu.append(substring.pop(0))
				cod_local.append(substring.pop(0))
				desc_local.append(substring.pop(0))
				mon.append(substring.pop(0))
				unid.append(substring.pop(0))

		formato_archivo_v2 = ".csv"
		nombre_archivo_v2 = nombre_archivo.replace(formato_archivo, formato_archivo_v2)
		newPathFile = ruta + nombre_archivo_v2

		with open(newPathFile, 'w') as the_file:
			if (tipo_archivo == "DX"):
				while(mon):
					the_file.write(fecha.pop(0))
					the_file.write(",")
					the_file.write(cod_local.pop(0))
					the_file.write(",")
					the_file.write(cod_plu.pop(0))
					the_file.write(",")
					the_file.write(desc_plu.pop(0))
					the_file.write(",")
					the_file.write(desc_local.pop(0))
					the_file.write(",")
					the_file.write(unid.pop(0).replace(".", ""))
					the_file.write(",")
					the_file.write(mon.pop(0).replace("$", "").replace(".", ""))
					the_file.write("\n")
			if (tipo_archivo == "DY"):
				while(mon):
					the_file.write(cod_local.pop(0))
					the_file.write(",")
					the_file.write(cod_plu.pop(0))
					the_file.write(",")
					the_file.write(desc_plu.pop(0))
					the_file.write(",")
					the_file.write(desc_local.pop(0))
					the_file.write(",")
					the_file.write(unid.pop(0).replace(".", ""))
					the_file.write(",")
					the_file.write(mon.pop(0).replace("$", "").replace(".", ""))
					the_file.write("\n")

		return(nombre_archivo_v2, formato_archivo_v2)

	return(nombre_archivo, formato_archivo)

def deleteInterFiles (tipo_archivo, nombre_archivo):
	if(tipo_archivo in ["DX", "DY", "DP", "DF", "MH"]): # Elimina archivos intermedios (SB, PR, PF)
		#print(nombre_archivo)
		deleteOldFiles (nombre_archivo)

def csvFromXlsx(tipo_archivo, formato_archivo, nombre_archivo, ruta):
	#(tipo_archivo, formato_archivo, nombre_archivo, ruta):
	if (formato_archivo == ".xlsx"):
		formato_archivo_v2 = ".csv"
		nombre_archivo_v2 = nombre_archivo.replace(formato_archivo, formato_archivo_v2)
		wb = xlrd.open_workbook(ruta + nombre_archivo)

		# AGREGAR MAS CONDICIONES SI APARECEN MAS ARCHIVOS
		if (tipo_archivo == "DP" and formato_archivo == ".xlsx"):
			sh = wb.sheet_by_name('B2B') 	# Nombre de la hoja xlsx
			skipNoData = 3 					# Filas que se salta hasta llegar al header sobre la data
			lenghtColumn = 5				# Cantidad de columnas de archivo xlsx
		elif (tipo_archivo == "DF" and formato_archivo == ".xlsx"):
			sh = wb.sheet_by_name('Informe')
			skipNoData = 0
			lenghtColumn = 8
		elif (tipo_archivo == "MH" and formato_archivo == ".xlsx"):
			sh = wb.sheet_by_name('PARA ARMAR 3°')
			skipNoData = 0
			lenghtColumn = 11
		fileCsv = open(ruta + nombre_archivo_v2, 'w')
		wr = csv.writer(fileCsv, lineterminator='\n')
		noDecimalValue = []

		for rowNum in range(sh.nrows):
			if(skipNoData == 0):
				noDecimalValue = sh.row_values(rowNum)
				for indice in range(0, lenghtColumn):
					if(sh.row(rowNum)[indice].ctype == 2):
						noDecimalValue[indice] = str(int(sh.row_values(rowNum)[indice]))
				wr.writerow(noDecimalValue)
			else:
				skipNoData -= 1
		fileCsv.close()
		return (nombre_archivo_v2, formato_archivo_v2)

	return(nombre_archivo, formato_archivo)

def sortedZolbit (nameOut, headers, encode):
	#fix caso cruz verde (por la z en la carpeta que esta antes del nombre)
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


### Parametrizacion de siglas para cod de locales (ordenadas por cod de cadena)###

def putSiglaLocal (newRow, row, retailer, ventaInventario, siglaLoc):
	# Parametrizar la posicion de los indices en un nuevo argumento

	# Cadenas con diferentes retailers
	if (retailer == "JUMBO"):
		if (ventaInventario == "DIA"):
			if ("N" in row[siglaLoc] and siglaLoc != -1):
				newRow[2] += "SI"
			else:
				newRow[2] += "JU"
		elif (ventaInventario == "INV"):
			if ("N" in row[siglaLoc] and siglaLoc != -1):
				newRow[2] += "SI"
			else:
				newRow[2] += "JU"
		
	elif (retailer == "PARIS"):
		if (row[siglaLoc] in "JOHNSON" and siglaLoc != -1):
			newRow[2] += "JO"
		else:
			newRow[2] += "PA"

	elif (retailer == "UNIMARC"):
		if ("ALVI " in row[siglaLoc] and siglaLoc != -1):
			newRow[2] += "AV"
		elif ("M10 " in row[siglaLoc] and siglaLoc != -1):
			newRow[2] += "MD"
		elif ("OKM " in row[siglaLoc] and siglaLoc != -1):
			newRow[2] += "OK"
		else:
			newRow[2] += "UN"
	
	elif (retailer == "LIDER"):
		if ("SBA " in row[siglaLoc] and siglaLoc != -1):
			newRow[2] += "AC"
		elif ("EK " in row[siglaLoc] and siglaLoc != -1):
			newRow[2] += "EK"
		else:
			newRow[2] += "LI"
	
	# Cadenas con retailers unicos
	elif (retailer == "HIPERUNICO"):
		newRow[2] += "HU"

	elif (retailer == "MONTECARLO"):
		newRow[2] += "MO"
	
	elif (retailer == "TUCAPEL"):
		newRow[2] += "TP"
	
	elif (retailer == "SUPERMERCADOS"):
		newRow[2] += "SS"

	elif (retailer == "TOTTUS"):
		newRow[2] += "TT"

	elif (retailer == "CHEDRAUI"):
		newRow[2] += "CH"
	
	elif (retailer == "COMERCIAL MEXICANA"):
		newRow[2] += "CC"
	
	#elif (retailer == "WALMART"):
	#	newRow[2] += "WL"
	
	elif (retailer == "SORIANA"):
		newRow[2] += "SR"
	
	elif (retailer == "MAYORISTAS"):
		newRow[2] += "MY"
	
	elif (retailer == "WALMART"):
		newRow[2] += "WM"
	
	elif (retailer == "CENCOSUD"):
		newRow[2] += "CN"
	
	elif (retailer == "DIA"):
		newRow[2] += "DI"
	
	elif (retailer == "HEB"):
		newRow[2] += "HE"
	
	elif (retailer == "CARREFOUR"):
		newRow[2] += "CA"
	
	elif (retailer == "LAANONIMA"):
		newRow[2] += "LA"
	
	elif (retailer == "CALIMAX"):
		newRow[2] += "CL"
	
	elif (retailer == "FALABELLA"):
		newRow[2] += "FA"
	
	elif (retailer == "RIPLEY"):
		newRow[2] += "RI"
	
	elif (retailer == "LAPOLAR"):
		newRow[2] += "PO"
	
	elif (retailer == "CORONA"):
		newRow[2] += "CO"
	
	elif (retailer == "HITES"):
		newRow[2] += "HI"
	
	elif (retailer == "PREUNIC"):
		newRow[2] += "PR"
	
	elif (retailer == "ABCDIN"):
		newRow[2] += "DN"
	
	elif (retailer == "MAICAO"):
		newRow[2] += "MA"
	
	elif (retailer == "TRICOT"):
		newRow[2] += "TR"
	
	elif (retailer == "PCFACTORY"):
		newRow[2] += "PF"
	
	elif (retailer == "LIVERPOOL"):
		newRow[2] += "LP"

	elif (retailer == "PALACIO"):
		newRow[2] += "PH"
	
	elif (retailer == "SEARS"):
		newRow[2] += "SA"
	
	elif (retailer == "CIMACO"):
		newRow[2] += "CI"
	
	elif (retailer == "PRICE"):
		newRow[2] += "PS"
	
	elif (retailer == "SANBORNS"):
		newRow[2] += "SN"
	
	elif (retailer == "SODIMAC"):
		newRow[2] += "HS"
	
	elif (retailer == "CONSTRUMART"):
		newRow[2] += "CM"
	
	elif (retailer == "EASY"):
		newRow[2] += "EA"
	
	elif (retailer == "FASA"):
		newRow[2] += "AH"
	
	elif (retailer == "CRUZVERDE"):
		newRow[2] += "CV"
	
	elif (retailer == "SALCO"):
		newRow[2] += "SB"
	
	elif (retailer == "PETROBRAS"):
		newRow[2] += "PB"
	
	elif (retailer == "PRONTO"):
		newRow[2] += "PC"
	
	elif (retailer == "SHELL"):
		newRow[2] += "SH"
	
	elif (retailer == "TUA"):
		newRow[2] += "TU"
	
	elif (retailer == "GLAM"):
		newRow[2] += "GL"
	
	elif (retailer == "CANONTEX"):
		newRow[2] += "CT"
	
	elif (retailer == "MULTICENTRO"):
		newRow[2] += "MC"
	
	elif (retailer == "MULTIHOGAR"):
		newRow[2] += "MH"
	
	elif (retailer == "CASA"):
		newRow[2] += "CX"
	
	elif (retailer == "EMILIOSANDOVAL"):
		newRow[2] += "ES"
	
	#elif (retailer == "LAELEGANTE"):
	#	newRow[2] += "LE"
	
	elif (retailer == "CASAROYAL"):
		newRow[2] += "RY"
	
	elif (retailer == "DIMARSA"):
		newRow[2] += "DM"
	
	elif (retailer == "SELLIN"):
		newRow[2] += "SD"
	
	elif (retailer == "7VEINTE"):
		newRow[2] += "SV"
	
	elif (retailer == "AZALEIA"):
		newRow[2] += "AZ"
	
	elif (retailer == "BILLABONG"):
		newRow[2] += "BG"
	
	elif (retailer == "CATERPILLAR"):
		newRow[2] += "CP"
	
	elif (retailer == "COLUMBIA"):
		newRow[2] += "CB"
	
	elif (retailer == "DISCOUNTHOUSE"):
		newRow[2] += "DH"
	
	elif (retailer == "ECOMMERCE"):
		newRow[2] += "EC"
	
	elif (retailer == "FUNSPORT"):
		newRow[2] += "FS"

	elif (retailer == "HUSHPUPPIES"):
		newRow[2] += "HP"
	
	elif (retailer == "HUSHPUPPIESKIDS"):
		newRow[2] += "HK"

	elif (retailer == "MERRELL"):
		newRow[2] += "MR"

	elif (retailer == "NINEWEST"):
		newRow[2] += "NW"

	elif (retailer == "ROCKFORD"):
		newRow[2] += "RF"

	elif (retailer == "SHOEEXPRESS"):
		newRow[2] += "SE"

	elif (retailer == "WELOVESHOES"):
		newRow[2] += "WS"

	elif (retailer == "KAYSERTIENDAS"):
		newRow[2] += "KY"

	elif (retailer == "LAEUROPEA"):
		newRow[2] += "EU"

	elif (retailer == "MASKOTA"):
		newRow[2] += "MK"

	elif (retailer == "LAJUANA"):
		newRow[2] += "LJ"

	elif (retailer == "LAPIZLOPEZ"):
		newRow[2] += "LZ"

	elif (retailer == "HPSTORE"):
		newRow[2] += "HH"

	return newRow