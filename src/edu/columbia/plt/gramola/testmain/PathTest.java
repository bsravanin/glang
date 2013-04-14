package edu.columbia.plt.gramola.testmain;

import java.util.ArrayList;
import java.util.Stack;

import edu.columbia.plt.gramola.datastruct.Edge;
import edu.columbia.plt.gramola.datastruct.Graph;
import edu.columbia.plt.gramola.datastruct.Node;

public class PathTest {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		Graph g = new Graph();
		Node a = g.createNode("name", "a");
		Node b = g.createNode("name", "b");
		Node c = g.createNode("name", "c");
		Node d = g.createNode("name", "d");
		Node e = g.createNode("name", "e");
		
		Edge ab = g.createEdge(a, b, "type", "test");
		Edge bd = g.createEdge(b, d, "type", "test");
		Edge de = g.createEdge(d, e, "type", "test");
		
		Edge ac = g.createEdge(a, c, "type", "test");
		Edge cb = g.createEdge(c, b, "type", "test");
		Edge cd = g.createEdge(c, d, "type", "test");
		
		ArrayList<ArrayList<Edge>> paths = g.getPaths(a, e, "type", "test");
		
		System.out.println("Total paths: " + paths.size());
		
		for (ArrayList<Edge> tmp: paths) {
			printPath(tmp, "name", "type");
		}
		
		ArrayList<Edge> shortestPath = g.getShortestPath(a, e, "type", "test");
		System.out.println("Shortest path: " + shortestPath.size());
		printPath(shortestPath, "name", "type");
	}
	
	public static void printPath(ArrayList<Edge> pathList, String nodeAttr, String edgeAttr) {
		Edge tmpEdge;
		while (!pathList.isEmpty()) {
			tmpEdge = pathList.remove(0);
			System.out.println(tmpEdge.inV().getVariableValue(nodeAttr) + " " 
					+ tmpEdge.getVariableValue(edgeAttr) + " "
					+ tmpEdge.outV().getVariableValue(nodeAttr));
		}
		System.out.println(" ");
	}
}
