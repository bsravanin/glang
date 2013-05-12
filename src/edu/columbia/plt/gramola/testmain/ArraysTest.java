package edu.columbia.plt.gramola.testmain;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import edu.columbia.plt.gramola.datastruct.Node;
import edu.columbia.plt.gramola.util.GraphUtil;


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
		ArrayList<String> var = new ArrayList<String>();
		var.add("Name");
		ArrayList<String> value = new ArrayList<String>();
		value.add("Tim");
		Node n = new Node(GraphUtil.createVarMap(var, value));
		System.out.println("Test node: " + n.getVariableValue("Name"));
	}

}
