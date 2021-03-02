import os
from bisect import bisect_left
import re
from datetime import datetime, timedelta
import csv
from operator import itemgetter
import sys

def binarySearch (values, element): 
	index = bisect_left(values, element)
	if (index != len (values) and values[index] == element):
		# print ("Elemento ", element, " presente en indice: ", str (index))
		return 0
	else:
		#print ("Elemento", element, "sin su par")
		return -1

def listToString (lista, delim):
    str1 = "" 
    for ele in lista:
        str1 += ele + delim 
    # return string
    if (delim != ""):
        str1 = str1[:-1]
    return str1

def getLocal (nombre_archivo):
    return re.findall (r"_[0-9]{8}_[0-9]{8}_[0-9]{8}_(.*?)_[A-Z]{1}_", nombre_archivo)[0]

def namefileOut (nombre_archivo):
    nombre_archivo = nombre_archivo.split("_")
    nombre_archivo.pop(4)
    nombre_archivo.pop(4)
    nombre_archivo[4], nombre_archivo[5] = nombre_archivo[5], nombre_archivo[4]

    nombre_archivo_final = ""
    for elemento in nombre_archivo:
        nombre_archivo_final += elemento + "_"
    nombre_archivo_final = nombre_archivo_final.replace ("___","_")
    nombre_archivo_final = nombre_archivo_final[:-1]
    return  "Z" + nombre_archivo_final

def getFileDates (files):
    #print(files)
    fecha_ini = 99999999
    fecha_fin = 0
    for elemento in files:
        try:
            cadena = elemento.split ("_")
            fecha_ini_cadena = re.findall (r"\b(\d{8})\b", cadena[1])[0]
            fecha_fin_cadena  = re.findall (r"\b(\d{8})\b", cadena[2])[0]
            if (int (fecha_ini_cadena) < fecha_ini):
                fecha_ini = int (fecha_ini_cadena)
            if (int (fecha_fin_cadena) > fecha_fin):
                fecha_fin = int (fecha_fin_cadena)
        except:
            continue
    fecha_ini2 = datetime.strptime (str(fecha_ini), "%Y%m%d")
    fecha_ini = datetime.strptime (str(fecha_ini), "%Y%m%d").date()
    fecha_fin = datetime.strptime (str(fecha_fin), "%Y%m%d").date()

    delta = fecha_fin - fecha_ini
    rangoFechas = []
    for day in range (delta.days + 1):
        fecha = str ((fecha_ini2 + timedelta (days=day)).date ())
        rangoFechas.append (fecha)
    #print(fecha_ini, type(fecha_ini))
    #print(fecha_fin, type(fecha_fin))
    #print(rangoFechas)
    return fecha_ini, fecha_fin, rangoFechas

def deleteFiles (file_name):
    #print("====DELETING:",file_name)
    try:
        #print("Eliminando ", nameOut)
        os.remove (file_name)
    except:
        pass

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


def finalFileName (ruta, exampleName, rangoFechas):
    name = exampleName.split("_")
    name.pop(3)
    name[1] = rangoFechas[0].replace("-","")
    name[2] = rangoFechas[-1].replace("-","")
    return ruta + listToString (name, "_")

def moveToBackup (ruta, files):
    respaldo = ruta + "RESP_TRIO/"
    if not os.path.exists(respaldo):
        os.makedirs(respaldo)
    for file in files:
        deleteFiles (respaldo + file)
        os.rename (ruta + file, respaldo + file)

def deleteIfEmpty (rutaZolbit, encode):
    fileZolbit =  open (rutaZolbit, "r", encoding = encode)
    secondLine = fileZolbit.readline ()
    secondLine = fileZolbit.readline ()
    fileZolbit.close ()
    if len (secondLine) < 2:
        #print("Deleting", rutaZolbit)
        deleteFiles (rutaZolbit)

######################### Funcion principal #########################

def unifyConvertZolbit (ruta):
    encode = "ISO-8859-1"
    files_aux = sorted (os.listdir(ruta))
    files = []
    #print(len(files))
    montoDia = [0, 0, 0, 0, 0, 0, 0]
    unidadDia = [0, 0, 0, 0, 0, 0, 0]

    # Asigna headers a utilizar
    headers = ["fecha_inicio","fecha_termino",
	"codigo_local","codigo_plu","descripcion_producto",
	"descripcion_local","venta_unidad","venta_monto",
	"venta_costo","inventario_unidad",
	"inventario_monto","contribucion"]

    head = listToString (headers, ",")
    
    # Obtiene todos los nombres de los archivos pareados, descarta los que no tienen su par
    for element in files_aux:
        parMonto = element.replace ("_M_", "_U_")
        parUnidad = element.replace ("_U_", "_M_")
        if ("_M_" in element):
            result = binarySearch (files_aux, parMonto) # Realiza búsqueda binaria de parMonto en files
        elif ("_U_" in element):
            result = binarySearch (files_aux, parUnidad) # Realiza búsqueda binaria de parUnidad en files
        else:
            result = -1
        if (result != -1):
            files.append (element)

    # Termina el programa si no hay archivos nuevos
    if (not files):
        print((str("["+ str(datetime.now().strftime("%H:%M:%S"))+"]"+"[INFO]"+"Sin Conversion;100 - No existen archivos a convertir")))
        return -1

    # Obtiene rango de fechas de todos los archivos en la carpeta, para nombrar archivo final
    fecha_ini, fecha_fin, rangoFechas = getFileDates (files)

    # Concatena nombre y ruta para nombrar archivo final donde se ingresaran los datos
    finalPathNameFile = finalFileName (ruta, namefileOut (files[0]), rangoFechas)
    #print(finalPathNameFile)

    # Elimina los archivos zolbit generados anteriormente para generar los nuevos
    for index_name in range (0, len (files)):
        deleteFiles (ruta + namefileOut (files[index_name]))
    deleteFiles (finalPathNameFile)

    # Crea y/o abre archivo zolbit
    fileZolbit =  open (finalPathNameFile, "a+")

    # Rellena headers a fileZolbit
    fileZolbit.write (head + "\n")

    # Empieza a procesar cada archivo junto a su par
    file_index = 0
    while (file_index < len (files) - 1):
        # Obtiene rango de fechas de archivo a procesar, para determinar que fechas poner en que filas
        aux_file = []
        aux_file.append (files[file_index])
        fecha_ini, fecha_fin, rangoFechas = getFileDates (aux_file)

        #print(file_index)
        #print("PROCESANDO: ", files[file_index])
        cod_local = -1
        rutaFileMon = ruta + files[file_index]
        rutaFileUni = ruta + files[file_index + 1]

        # Abre archivo monto y unidad
        monto = open (rutaFileMon, "r", encoding = encode) # Archivo monto
        unidad = open (rutaFileUni, "r", encoding = encode) # Archivo unidad

        # Deja en estas variables los textos de cada archivo
        lineMonto = monto.readlines ( )
        lineUnidad = unidad.readlines ( )

        # Obtiene el codigo de local (nombre)
        for element in lineMonto:
            if ("Tienda," in element):
                index_loc = element.split (",").index ("Tienda")
                cod_local = element.split (",")[index_loc + 1]
                break
        
        # SI NO ENCUENTRA EL COD LOCAL, USAR EL DEL NOMBRE
        if(cod_local == -1):
            cod_local = getLocal (files[file_index])
            
        # Archivo con ese nombre esta malo
        if(cod_local == "(ADM) ADMINISTRATIVO"):
            file_index += 2
            continue
        
        # Recorre las lineas del archivo para el llenado de datos
        for index in range(0, len (lineMonto)):

            # Obtiene el codigo y descripcion de producto, luego los valores
            if("V.ANT" in lineMonto[index] and "V.ACT" in lineMonto[index + 1]):

                cod_prod = lineMonto[index].split (",")[0]
                index_prod = lineMonto[index + 1].split (",").index ("V.ACT")
                desc_prod = lineMonto[index + 1].split (",")[:index_prod]

                desc_prod = listToString (desc_prod, "")

                # Cambia las comas por puntos en valores numericos en linea de archivo de unidades, por incompatibilidad con delimitador coma
                lineUnidad[index + 1] = re.sub ('\"\d+(?:,\d+)?\"', lambda x:x.group(0).replace(',','.'), lineUnidad[index + 1])

                montoInv = lineMonto[index + 1].split (",")[index_prod + 10].replace ('\n', '')
                unidadInv = lineUnidad[index + 1].split (",")[index_prod + 10].replace ('"', '').replace ('\n', '')
                #print(unidadInv)

                # Guarda los valores de cada dia en sus respectivas listas

                ################ RANGO DE FECHAS DEBE CORRESPONDER AL DE ARCHIVO A PROCESAR
                for dia in range (0, len (rangoFechas)):
                    #print(montoDia)
                    montoDia[dia] = lineMonto[index + 1].split (",")[index_prod + dia + 1].replace ('.', '')
                    unidadDia[dia] = lineUnidad[index + 1].split (",")[index_prod + dia + 1].replace ('"', '')

                    # Comprobar si campo tiene datos para cargar
                    if ((dia != 6 and float (montoDia[dia]) == float (montoDia[dia]) == 0) or (dia == 6 and float (montoDia[dia]) == float (montoDia[dia]) == unidadInv == montoInv == 0 )):
                        continue
                    
                    # AÑADIR DIA DE NOMBRE
                    fileZolbit.write(rangoFechas[dia] + "," + rangoFechas[dia] + ",")

                    if(dia == len (rangoFechas) - 1):
                        fileZolbit.write (cod_local + "," + cod_prod + "," + desc_prod + "," + cod_local + "," + unidadDia[dia] + "," + montoDia[dia] + ",null," + unidadInv + "," + montoInv + ",null\n")
                    else:
                        fileZolbit.write (cod_local + "," + cod_prod + "," + desc_prod + "," + cod_local + "," + unidadDia[dia] + "," + montoDia[dia] + ",null,null,null,null\n")

                # print(montoDia)
                # print(unidadDia)

                index += 2
        file_index += 2
        #print(cod_local)
    
    # Cerrando archivos
    fileZolbit.close()
    monto.close()
    unidad.close()

    sortedZolbit (finalPathNameFile, headers, encode) # Ordena archivo Zolbit
    deleteIfEmpty (finalPathNameFile, encode) # Elimina archivo zolbit si no se insertaron filas a parte del header
    print (str("["+ str(datetime.now().strftime("%H:%M:%S"))+"]"+"[INFO]"+"Convertidos;0 - Ejecutado exitosamente"))
    #moveToBackup (ruta, files) # Mueve archivos utilizados a carpeta backup


# ruta = "D:/Documents/rpro/ProyectoOpAuto/Codes/Validador/FALABELLA2/"
#ruta = "D:/Documents/rpro/ProyectoOpAuto/Codes/Validador/FALABELLA2/"
# ruta = "D:/Documents/rpro/ProyectoOpAuto/Codes/Validador/SODIMAC2/"
ruta = sys.argv[1]

run = unifyConvertZolbit (ruta)