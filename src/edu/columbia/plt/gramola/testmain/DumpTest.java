package edu.columbia.plt.gramola.testmain;

import edu.columbia.plt.gramola.datastruct.Edge;
import edu.columbia.plt.gramola.datastruct.Graph;
import edu.columbia.plt.gramola.datastruct.Node;
import edu.columbia.plt.gramola.util.GraphDBController;

public class DumpTest {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		Graph g = new Graph();
		
		Node hello = g.createNode("name", "hello", "age", 21);
		Node world = g.createNode("name", "world", "age", 27);
		Edge e = g.createEdge(hello, world, "type", "friend");
		System.out.println("Test start node: " + hello);
		System.out.println("Test end node: " + world);
		System.out.println("Test edge: " + e);
		
		String dbPath = "/Users/mikefhsu/javaws/Gramola/neo4jdbs/mike";
		GraphDBController dbController = new GraphDBController(dbPath);
		System.out.println("Test db path " + dbController.getGraphDBDir());
		
		dbController.dump(g, "id", "id");
		//System.out.println(Test0419.class.getResource("Test0419.class")); 
	}

}
