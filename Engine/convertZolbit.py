#convertZolbit  V1.00.00
#define VERSION V1.00.00

import sys
from convertWrapper import convertFile

if __name__ == "__main__":
	#Adaptar para cada cliente, entregar como parametro al correr el codigo

	headers = ["fecha_inicio","fecha_termino",
	"codigo_local","codigo_plu","descripcion_producto",
	"descripcion_local","venta_unidad","venta_monto",
	"venta_costo","inventario_unidad",
	"inventario_monto","contribucion"]

	nombre_retailer = sys.argv[1]
	tipo_archivo = sys.argv[2]
	sigla = sys.argv[3]
	formato_archivo = sys.argv[4]
	orden_columna = sys.argv[5]
	delimitador = sys.argv[6]
	header = sys.argv[7]
	formato_fecha = sys.argv[8]
	ruta = sys.argv[9]
	conversion_un = sys.argv[10]
	conversion_mon = sys.argv[11]
	nombre_archivo = sys.argv[12]


	result = convertFile (headers, nombre_retailer, tipo_archivo, 
				sigla, formato_archivo, orden_columna, 
				delimitador, header, formato_fecha, ruta, 
				conversion_un, conversion_mon, nombre_archivo)
	print(result)
