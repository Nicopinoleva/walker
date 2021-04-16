/* cargaVenta2  V1.00.00 */
#define VERSION V1.00.00

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define ROW_SIZE 600
#define KEY_SIZE 300

char *getValues (char *ptrIni)
{ //Retorna puntero hacia values de fila
  int delimitador;
  char *ptrValues = ptrIni;

  for (delimitador = 0; delimitador <= 5; delimitador ++)
    ptrValues = strchr (ptrValues, ',') + 1;

  return (ptrValues);
}

char *getKeys (char *fila)
{ //Retorna string con Keys
  int tk;
  char filaTok [ROW_SIZE], *ptrKeys, *token;
  static char keys [KEY_SIZE];
  *keys = 0;
  ptrKeys = strcpy (filaTok, fila);
  token = strtok (ptrKeys, ",");
  for (tk = 0; tk < 4; tk ++)
  { strcat (keys, token);
    token = strtok (NULL, ",");
  }
  return (keys);
}

int main ( )
{ int siguienteZolbit, siguienteBdd, NULLZolbit, NULLBdd, scmp;
  char filaZolbit [ROW_SIZE], filaBdd [ROW_SIZE], 
    keysZolbit [KEY_SIZE], keysBdd [KEY_SIZE],//////////////////////////////////TESTING
    *ptrIniZolbit, *ptrValuesZolbit,// *keysZolbit,
    *ptrIniBdd, *ptrValuesBdd;// *keysBdd;
  FILE *fzolbitptr, *fbddptr;

  //Apertura de archivos Zolbit y BDD
  if (!(fzolbitptr = fopen ("JUMBOZOLBIT.csv", "rb")))
  { perror ("Error opening Zolbit file ");
    return (-1);
  }

  if (!(fbddptr = fopen ("JUMBOBDD.csv", "rb")))
  { perror ("Error opening BDD file ");
    return (-1);
  }

  //Inicializacion de variables a ocupar
  *filaZolbit = *filaBdd = *keysZolbit = *keysBdd = 0;
  siguienteZolbit = siguienteBdd = 1;
  NULLZolbit = NULLBdd = 0;

  //Flag de inicio
  while (1)
  { if (siguienteZolbit == 1  &&  NULLZolbit == 0)
    { if (fgets(filaZolbit, sizeof (filaZolbit), fzolbitptr))
      { ptrIniZolbit = filaZolbit;  //Puntero a nueva fila Zolbit
        ptrValuesZolbit = getValues (ptrIniZolbit);
        //keysZolbit = getKeys (filaZolbit);
        strcpy (keysZolbit, getKeys (filaZolbit));
      }
      else //No hay mas filas Zolbit
        NULLZolbit = 1;
    }

    if (siguienteBdd == 1  &&  NULLBdd == 0)
    { if (fgets (filaBdd, sizeof (filaBdd), fbddptr))
      { ptrIniBdd = filaBdd;  //Puntero de referencia a nueva fila Bdd  
        ptrValuesBdd = getValues(ptrIniBdd);
        //keysBdd = getKeys(filaBdd);
        strcpy (keysBdd, getKeys (filaBdd));
      }
      else //No hay mas filas Bdd
        NULLBdd = 1;
    }

    siguienteZolbit = siguienteBdd = 0;
  
    /*
    printf("Zolbit: %s\nBDD   : %s\n", ptrIniZolbit, ptrIniBdd);
    printf("Fila Zolbit: %i\nFila BDD   : %i\n", filaZolbit, filaBdd);
    printf("NULL Zolbit: %i\nNULL BDD   : %i\n", NULLZolbit, NULLBdd);
    printf("Keys   :");
    puts(keysZolbit);
    printf("KeysBdd:");
    puts(keysBdd);
    printf("Values   :");
    puts(ptrValuesZolbit);
    printf("ValuesBdd:");
    puts(ptrValuesBdd);
    */

    if (NULLZolbit == 0  &&  NULLBdd == 0)
    { //Caso de ambos con filas sin comparar 
      if ((scmp = strcmp (keysZolbit, keysBdd)) == 0)
      { //Si Keys son iguales...
        if (strcmp (ptrValuesZolbit, ptrValuesBdd) == 0)
        { //...y values son iguales
          printf ("======IGUALES SIGUIENTE=====\n");
          puts (ptrIniZolbit);
          puts (ptrIniBdd);
        }
        else
        { //...y values son diferentes (UPDATE)
          printf ("==================Fila a actualizar\n");
          puts (ptrIniZolbit);
        }

        siguienteZolbit = siguienteBdd = 1;
      }

      else if (scmp < 0)
      { //Si key Zolbit es menor que key Bdd (INSERT)
        printf ("==================Fila a insertar\n");
        puts (ptrIniZolbit);
        siguienteZolbit = 1;
      }

      else
      { //Si key Zolbit es mayor que key Bdd (DELETE)
        printf ("==================Fila a eliminar\n");
        puts (ptrIniBdd);
        siguienteBdd = 1;
      }
    }

    else if (NULLZolbit == 0  &&  NULLBdd == 1)
    { //Caso archivo Bdd comparado completamente
      printf ("==================Fila a insertar\n");
      puts (ptrIniZolbit); //Se inserta Zolbit (INSERT)
      siguienteZolbit = 1;
    }

    else if (NULLZolbit == 1  &&  NULLBdd == 0)
    { //Caso archivo Zolbit comparado completamente
      printf("==================Fila a eliminar\n");
      puts (ptrIniBdd);    //Se elimina fila Bdd (DELETE)
      siguienteBdd = 1;
    }

    else if (NULLZolbit == 1  &&  NULLBdd == 1)
    { //Caso ambos comparados completamente
      break;
    }
  }

  printf ("======FINALIZANDO=====\n");
  fclose (fbddptr);  fclose (fzolbitptr);
  return (0);
}
