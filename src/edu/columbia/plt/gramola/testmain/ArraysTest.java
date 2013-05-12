package edu.columbia.plt.gramola.testmain;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;


public class ArraysTest {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		List a = Arrays.asList("abc", 5);		
		
		for (int i = 0 ; i < a.size(); i++) {
			System.out.println("Test: " + a.get(i).getClass().getName());
			System.out.println("Test: " + a.get(i));
		}
		
		ArrayList b = new ArrayList();
		b.add(7);
		System.out.println("Test add: " + b.get(0));
	}

}
