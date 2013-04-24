package edu.columbia.plt.gramola.testmain;

import edu.columbia.plt.gramola.datastruct.Edge;
import edu.columbia.plt.gramola.datastruct.Graph;
import edu.columbia.plt.gramola.datastruct.Node;
import edu.columbia.plt.gramola.util.GraphDBController;
import edu.columbia.plt.gramola.util.GraphVisualizer;

public class OverAllTest {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		//Create graph
		Graph g = new Graph();
		
		Node marko = g.Node("name", "marko");
		marko.setVariableValue("age", 29);
		
		Node vadas = g.Node("name", "vadas", "age", 27);
		Edge e = g.Edge(marko, vadas, "type", "knows");
		e.setVariableValue("weight", 0.5);
		
		Node john = g.Node("name", "john", "age", 32);
		Edge jEdge = g.Edge(marko, john, "type", "admires");
		
		Node joseph = g.Node("name", "joseph", "age", 22);
		Edge joEdge = g.Edge(marko, joseph, "type", "hates");
		
		Node mary = g.Node("name", "mary", "age", 22);
		Edge mEdge = g.Edge(mary, marko, "type", "loves");
		
		Node lisa = g.Node("name", "lisa", "age", 32);
		Edge lEdge = g.Edge(lisa, marko, "type", "hates");
		
		// Dump
		String dbPath = "/Users/mikefhsu/javaws/Gramola/neo4jdbs/mike2";
		GraphDBController gc = new GraphDBController(dbPath);
		System.out.println("Graph before dumping");
		for (Node n: g.getAllNodes()) {
			System.out.println(n.getVariableValue("name") + " " + n.getId());
		}
		
		gc.dump(g, "id", "id");
		
		//Load graph back
		Graph reload = gc.load();
		System.out.println("Graph after relading");
		for (Node n: reload.getAllNodes()) {
			System.out.println(n.getVariableValue("name") + " " + n.getId());
		}
		
		//Draw
		GraphVisualizer gv = new GraphVisualizer(reload, "name", "type");
		gv.draw();
		

	}

}
