package com.zolbit;

class TCPClient {
	static {
	      System.loadLibrary("jniwalker"); 
	   }
	private native int conectar(String ip, int Port);
	private native String mensaje(String msj, int sd);
	public static int conecta(String ip, int Port) {
		int result = new TCPClient().conectar(ip,Port);
		System.out.println("In Java, the returned int is: " + result);
		return result;
	}
	public static void enviar_mensaje(String msj, int sd) {
		String result = new TCPClient().mensaje(msj,sd);
		System.out.println("In Java, the returned String is: " + result);
	}
	public static String getArgumentos(int sd) {
		String argumentos =  new TCPClient().mensaje("PARAMS",sd);
		return argumentos;
	}
}