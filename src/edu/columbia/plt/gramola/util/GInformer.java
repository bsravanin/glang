package edu.columbia.plt.gramola.util;

public class GInformer {
	
	private static String gHead = "[Glib]: ";
	
	public static void printMessage(String glibMsg) {
		System.out.println(gHead + glibMsg);
	}

}
