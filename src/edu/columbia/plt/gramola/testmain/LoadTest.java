package edu.columbia.plt.gramola.testmain;

import java.util.ArrayList;

import edu.columbia.plt.gramola.datastruct.Edge;
import edu.columbia.plt.gramola.datastruct.Graph;
import edu.columbia.plt.gramola.datastruct.Node;
import edu.columbia.plt.gramola.util.GraphDBController;

public class LoadTest {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		GraphDBController dbController = new GraphDBController("/Users/mikefhsu/javaws/Gramola/neo4jdbs/mike");
		Graph g = dbController.load();
		
		System.out.println("Test load graph: " + g);
		
		ArrayList<Edge> edgeList = g.getAllEdges();
		Node start;
		Node end;
		
		for (Edge e: edgeList) {
			start = e.inV();
			end = e.outV();
			System.out.println("Test load start node: " + start + " " + start.getVariableValue("name"));
			System.out.println("Test load edge: " + e + " " + e.getVariableValue("type"));
			System.out.println("Test load end node: " + end + " " + end.getVariableValue("name"));
		}
		
		
		
	}

}
