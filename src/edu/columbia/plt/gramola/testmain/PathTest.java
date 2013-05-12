package edu.columbia.plt.gramola.testmain;

import java.util.ArrayList;
import java.util.HashMap;
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
		
		HashMap<String, Object> varMap = new HashMap<String, Object>();
		
		varMap.put("name", "a");
		Node a = g.Node(varMap);
		
		varMap = new HashMap<String, Object>();
		varMap.put("name", "b");
		Node b = g.Node(varMap);
		
		varMap = new HashMap<String, Object>();
		varMap.put("name", "c");
		Node c = g.Node(varMap);
		
		varMap = new HashMap<String, Object>();
		varMap.put("name", "d");
		Node d = g.Node(varMap);
		
		varMap = new HashMap<String, Object>();
		varMap.put("name", "e");
		Node e = g.Node(varMap);
		
		varMap = new HashMap<String, Object>();
		varMap.put("type", "test");
		Edge ab = g.Edge(a, b, varMap);
		Edge bd = g.Edge(b, d, varMap);
		Edge de = g.Edge(d, e, varMap);
		
		Edge ac = g.Edge(a, c, varMap);
		Edge cb = g.Edge(c, b, varMap);
		Edge cd = g.Edge(c, d, varMap);
		
		ArrayList<String> vars = new ArrayList<String>();
		ArrayList<Object> vals = new ArrayList<Object>();
		vars.add("type");
		vals.add("test");
		ArrayList<ArrayList<Edge>> paths = g.getPaths(a, e, vars, vals);
		
		System.out.println("Total paths: " + paths.size());
		
		for (ArrayList<Edge> tmp: paths) {
			printPath(tmp, "name", "type");
		}
		
		ArrayList<Edge> shortestPath = g.getShortestPath(a, e, vars, vals);
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
