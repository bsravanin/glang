package edu.columbia.plt.gramola.testmain;

import java.util.ArrayList;

import edu.columbia.plt.gramola.datastruct.Edge;
import edu.columbia.plt.gramola.datastruct.Graph;
import edu.columbia.plt.gramola.datastruct.Node;
import edu.columbia.plt.gramola.util.GraphDBController;
import edu.columbia.plt.gramola.util.GraphUtil;

public class DumpTest {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		Graph g = new Graph();
		
		ArrayList<String> vars = new ArrayList<String>();
		ArrayList<String> values = new ArrayList<String>();
		
		vars.add("name");
		vars.add("age");
		
		values.add("hello");
		values.add("21");
		Node hello = g.Node(GraphUtil.createVarMap(vars, values));
		
		vars = new ArrayList<String>();
		values = new ArrayList<String>();
		
		vars.add("name");
		vars.add("age");
		
		values.add("world");
		values.add("27");
		
		Node world = g.Node(GraphUtil.createVarMap(vars, values));
		
		vars = new ArrayList<String>();
		values = new ArrayList<String>();
		
		vars.add("type");
		values.add("friend");
		
		Edge e = g.Edge(hello, world, GraphUtil.createVarMap(vars, values));
		System.out.println("Test start node: " + hello);
		System.out.println("Test end node: " + world);
		System.out.println("Test edge: " + e);
		
		String dbPath = "/Users/mikefhsu/javaws/Gramola/neo4jdbs/mike";
		GraphDBController dbController = new GraphDBController(dbPath);
		dbController.createDB();
		dbController.initDB();
		System.out.println("Test db path " + dbController.getGraphDBDir());
		
		dbController.dump(g, "id", "id");
	}

}
