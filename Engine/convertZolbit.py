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
		encode = sys.argv[1]
		tipo_archivo = sys.argv[2]
		formato_archivo = sys.argv[3]
		orden_columna = sys.argv[4]
		delimitador = sys.argv[5]
		header = sys.argv[6]
		formato_fecha = sys.argv[7]
		ruta = sys.argv[8]
		conversion_un = sys.argv[9]
		decimal_un = sys.argv[10]
		conversion_mon = sys.argv[11]
		decimal_mon = sys.argv[12]
		nombre_archivo = sys.argv[13]
		
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
