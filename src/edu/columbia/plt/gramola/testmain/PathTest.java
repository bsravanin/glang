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
		Node a = g.Node("name", "a");
		Node b = g.Node("name", "b");
		Node c = g.Node("name", "c");
		Node d = g.Node("name", "d");
		Node e = g.Node("name", "e");
		
		Edge ab = g.Edge(a, b, "type", "test");
		Edge bd = g.Edge(b, d, "type", "test");
		Edge de = g.Edge(d, e, "type", "test");
		
		Edge ac = g.Edge(a, c, "type", "test");
		Edge cb = g.Edge(c, b, "type", "test");
		Edge cd = g.Edge(c, d, "type", "test");
		
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
