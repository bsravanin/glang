package edu.columbia.plt.gramola.testmain;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Stack;

import edu.columbia.plt.gramola.datastruct.Edge;
import edu.columbia.plt.gramola.datastruct.EdgeSet;
import edu.columbia.plt.gramola.datastruct.Graph;
import edu.columbia.plt.gramola.datastruct.Node;
import edu.columbia.plt.gramola.datastruct.NodeSet;

public class GraphApp {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		Graph g = new Graph();
		
		HashMap<String, Object> varMap = new HashMap<String, Object>();
		varMap.put("name", "marko");
		Node marko = g.Node(varMap);
		marko.setVariableValue("age", "29");
		
		/*Two nodes that marko connects to*/
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
		
		
		/*Two nodes connect to marko*/
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
		
		/*Test marko node in graph*/
		Node test = g.getNode("name", "marko");
		System.out.println("Test node " + 
				test.getVariableValue("name").toString() + " " +
				test.getVariableValue("age").toString());
		
		/*Test EdgeSet outE of marko*/
		EdgeSet outSet = test.outE();
		Iterator<Edge> oIT = outSet.iterator();
		Edge tmpEdge;
		while(oIT.hasNext()) {
			tmpEdge = oIT.next();
			System.out.println("inV: " + tmpEdge.inV().getVariableValue("name").toString());
			System.out.println("Edge attribute: " + tmpEdge.getVariableValue("type"));
			System.out.println("outV: " + tmpEdge.outV().getVariableValue("name").toString());
			System.out.println("");
		}
		
		/*Test EdgeSet inE of marko*/
		EdgeSet inSet = test.inE();
		Iterator<Edge> iIT = inSet.iterator();
		while(iIT.hasNext()) {
			tmpEdge = iIT.next();
			System.out.println("inV: " + tmpEdge.inV().getVariableValue("name").toString());
			System.out.println("Edge attribute: " + tmpEdge.getVariableValue("type"));
			System.out.println("outV: " + tmpEdge.outV().getVariableValue("name").toString());
			System.out.println("");
		}
		
		/*Test NodeSet outV of marko*/
		NodeSet outN = test.outNeighbors();
		Iterator<Node> outNeighbors = outN.iterator();
		Node tmpNode;
		
		System.out.println(test.getVariableValue("name").toString() + "'s outgoing neighbors");
		while(outNeighbors.hasNext()) {
			tmpNode = outNeighbors.next();
			System.out.println("Neighbor: " + tmpNode.getVariableValue("name"));
			System.out.println("");
		}
		
		/*Test filter*/
		System.out.println("Test filter: use type = admires");
		EdgeSet filterSet = outSet.filter("type", "admires");
		Iterator<Edge> fIT = filterSet.iterator();
		while(fIT.hasNext()) {
			tmpEdge = fIT.next();
			System.out.println("Edge attribute, value: " + "type " + tmpEdge.getVariableValue("type"));
			tmpNode = tmpEdge.outV();
			System.out.println("outV of filter result: " + tmpNode.getVariableValue("name"));
			System.out.println("");
		}
	}

}
