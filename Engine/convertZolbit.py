#convertZolbit  V1.00.00
#define VERSION V1.00.00

import sys
from convertWrapper import convertFile, exceptionDefinition
from datetime import datetime

if __name__ == "__main__":
	#Adaptar para cada cliente, entregar como parametro al correr el codigo

	headers = ["fecha_inicio","fecha_termino",
	"codigo_local","codigo_plu","descripcion_producto",
	"descripcion_local","venta_unidad","venta_monto",
	"venta_costo","inventario_unidad",
	"inventario_monto","contribucion"]
	try:
		#print(sys.argv)
		encode = sys.argv[1] # Codificacion de archivos
		tipo_archivo = sys.argv[2] # Si es trio falabella, si es preunic, si es pc factory, etc
		formato_archivo = sys.argv[3] # Extension de archivo (.txt .csv)
		orden_columna = sys.argv[4] # Orden de columnas a leer en archivo en bruto (ver en headers orden de archivo zolbit)
		delimitador = sys.argv[5] # Tipo de delimitador de datos (comas, pipes, puntos y comas)
		header = sys.argv[6] # Para saber si tiene headers
		formato_fecha = sys.argv[7] # Como muestra la fecha de venta el archivo en bruto
		ruta = sys.argv[8] # Ruta de archivo a procesar
		conversion_un = sys.argv[9] # Conversiones (numero de decimales y multiplicadores)
		decimal_un = sys.argv[10]
		conversion_mon = sys.argv[11]
		decimal_mon = sys.argv[12]
		nombre_archivo = sys.argv[13] # Nombre de archivo a procesar
		
	except Exception as excep:
		exceptionDefinition(excep, 1)
		sys.exit(1)

	result = convertFile (headers, encode, tipo_archivo,
				formato_archivo, orden_columna, delimitador, 
				header, formato_fecha, ruta, 
				conversion_un, decimal_un, conversion_mon, 
				decimal_mon, nombre_archivo)
	print(result)
	sys.exit( )
