package edu.columbia.plt.gramola.util;

/**
 * GInformer is the central class for printing out messages for Gramola
 * @author Fang-Hsiang Su, Gramola, 2013 Spring PLT
 *
 */
public class GInformer {
	
	private static String gHead = "[Glib]: ";
	
	public static void printMessage(String glibMsg) {
		System.out.println(gHead + glibMsg);
	}

}
