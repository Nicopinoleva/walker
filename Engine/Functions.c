// Save as "HelloJNI.c"
#include <jni.h>        // JNI header provided by JDK
#include <stdio.h>      // C Standard IO Header
#include <string.h>
#include "falabella_gino_TCPClient.h"   // Generated

JNIEXPORT jint JNICALL Java_falabella_1gino_TCPClient_conectar(JNIEnv *env, jobject thisObj, jstring ip, jint port) {
   // Step 1: Convert the JNI String (jstring) into C-String (char*)
   const char *IPStr = (*env)->GetStringUTFChars(env, ip, NULL);
 
   // Step 2: Perform its intended operations
   printf("In C, the received string is: %s\n", IPStr);
 
	jint result;
 	result = Connect(IPStr,port);
 //  (*env)->ReleaseStringUTFChars(env, ip, IPStr);  // release resources
   // Returned int to java
   return result;
}
JNIEXPORT jstring JNICALL Java_falabella_1gino_TCPClient_mensaje(JNIEnv *env, jobject thisObj, jstring msj, jint sd){
   // Step 1: Convert the JNI String (jstring) into C-String (char*)
   const char *MSJStr = (*env)->GetStringUTFChars(env, msj, NULL);
   char Respuesta[1000];
   memset (Respuesta, 0, sizeof Respuesta);
   printf("In C, the received message is: %s\n", MSJStr);
   SendRecv(sd, MSJStr, strlen(MSJStr), Respuesta, 1000);
   printf("In C, the answer string is: %s\n", Respuesta);
   return (*env)->NewStringUTF(env, Respuesta);
}
