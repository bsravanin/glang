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
		
		Node marko = g.Node("name", "marko");
		marko.setVariableValue("age", 29);
		
		/*Two nodes that marko connects to*/
		Node vadas = g.Node("name", "vadas", "age", 27);
		Edge e = g.Edge(marko, vadas, "type", "knows");
		e.setVariableValue("weight", 0.5);
		
		Node john = g.Node("name", "john", "age", 32);
		Edge jEdge = g.Edge(marko, john, "type", "admires");
		
		Node joseph = g.Node("name", "joseph", "age", 22);
		Edge joEdge = g.Edge(marko, joseph, "type", "hates");
		
		
		/*Two nodes connect to marko*/
		Node mary = g.Node("name", "mary", "age", 22);
		Edge mEdge = g.Edge(mary, marko, "type", "loves");
		
		Node lisa = g.Node("name", "lisa", "age", 32);
		Edge lEdge = g.Edge(lisa, marko, "type", "hates");
		
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
		NodeSet outN = test.out();
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
