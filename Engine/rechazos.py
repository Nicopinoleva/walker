#rechazos  V1.00.00
#define VERSION V1.00.00

import sys
from bisect import bisect_left

def binarySearch(values, element): 
	index = bisect_left(values, element)
	if (index != len (values) and values[index] == element):
		#print ("Elemento ", element, " presente en indice: ", str (index))
		return index
	else:
		print ("Elemento ", element, " no existe en BDD")
		return -1

if __name__ == "__main__":
	# Elementos ordenados recibidos por bdd
	# Parametrizar columna para prod o loc
	# Path y apertura de archivo
	nombre_archivo_bdd = 'productos.txt'
	pathBdd = 'D:/Documents/rpro/ProyectoOpAuto/Codes/CargaVenta/testJumbo/' + nombre_archivo_bdd
	nombre_archivo = 'Z766106706_20201222_20201228_JU_JUMBO_SI_B2B_DIA.csv'
	path = 'D:/Documents/rpro/ProyectoOpAuto/Codes/CargaVenta/testJumbo/' + nombre_archivo
	fileZolbit = open (path, "r") # Archivo Zolbit
	fileBdd = open (pathBdd, "r") # Archivo BDD

	if('productos' in nombre_archivo_bdd):
		columna = 3
	elif('locales' in nombre_archivo_bdd):
		columna = 2
	#delimitador = '\n'
	#columna = 3 # 2 para Locales, 3 para productos
	valoresBdd = fileBdd.read ( ).splitlines ( ) # Guarda en memoria (lista)
	
	print(valoresBdd)
	line = fileZolbit.readline ( ) # Salta header
	homologarElemento = []
	while (line := fileZolbit.readline ( )): # Guarda una linea de Zolbit en line
		elemento = line.split (',')[columna] # Almacena producto o local en elemento
		result = binarySearch (valoresBdd, elemento) # Realiza búsqueda binaria de elemento en memoria BDD
		if(result == -1):
			homologarElemento.append(elemento)
	print(homologarElemento)
	fileZolbit.close ( )
