package edu.columbia.plt.gramola.testmain;

import java.util.ArrayList;
import java.util.HashMap;

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
		
		HashMap<String, Object> varMap = new HashMap<String, Object>();
		varMap.put("name", "marko");
		Node marko = g.Node(varMap);
		marko.setVariableValue("age", "29");
		
		varMap = new HashMap<String, Object>();
		varMap.put("name", "vadas");
		varMap.put("age", "27");
		Node vadas = g.Node(varMap);
		
		varMap = new HashMap<String, Object>();
		varMap.put("type", "knows");
		Edge e = g.Edge(marko, vadas, varMap);
		e.setVariableValue("weight", "0.5");
		
		varMap = new HashMap<String, Object>();
		varMap.put("name", "john");
		varMap.put("age", "32");
		Node john = g.Node(varMap);
		varMap = new HashMap<String, Object>();
		varMap.put("type", "admires");
		Edge jEdge = g.Edge(marko, john, varMap);
		
		varMap = new HashMap<String, Object>();
		varMap.put("name", "joseph");
		varMap.put("age", "22");
		Node joseph = g.Node(varMap);
		varMap = new HashMap<String, Object>();
		varMap.put("type", "hates");
		Edge joEdge = g.Edge(marko, joseph, varMap);
		
		varMap = new HashMap<String, Object>();
		varMap.put("name", "mary");
		varMap.put("age", "22");
		Node mary = g.Node(varMap);
		varMap = new HashMap<String, Object>();
		varMap.put("type", "loves");
		Edge mEdge = g.Edge(mary, marko, varMap);
		
		varMap = new HashMap<String, Object>();
		varMap.put("name", "lisa");
		varMap.put("age", "32");
		Node lisa = g.Node(varMap);
		varMap = new HashMap<String, Object>();
		varMap.put("type", "hates");
		Edge lEdge = g.Edge(lisa, marko, varMap);
		
		// Dump
		String dbPath = "/Users/mikefhsu/javaws/Gramola/neo4jdbs/mike2";
		GraphDBController gc = new GraphDBController(dbPath);
		System.out.println("Graph before dumping");
		ArrayList<Node> allNodes = g.getAllNodes();
		for (Node n: allNodes) {
			System.out.println(n.getVariableValue("name") + " " + n.getId());
		}
		
		gc.dump(g, "id", "id");
		
		//Load graph back
		Graph reload = gc.load();
		System.out.println("Graph after relading");
		allNodes = reload.getAllNodes();
		for (Node n: allNodes) {
			System.out.println(n.getVariableValue("name") + " " + n.getId());
		}
		
		//Draw
		GraphVisualizer gv = new GraphVisualizer(reload, "name", "type");
		gv.draw();
		

	}

}
