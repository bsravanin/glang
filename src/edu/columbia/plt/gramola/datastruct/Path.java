package edu.columbia.plt.gramola.datastruct;

import java.util.ArrayList;

import edu.columbia.plt.gramola.abstractdata.GraphElement;

public class Path {
	
	private Node start;
	
	private Node end;
	
	public Path(Node start, Node end) {
		this.start = start;
		this.end = end;
	}
	
	/*TODO*/
	public void constructPath() {
		
	}
	
	/*TODO*/
	public void calShortestPath() {
		
	} 
	
	public ArrayList<? extends GraphElement> getPath() {
		ArrayList<GraphElement> pathList = new ArrayList<GraphElement>();
		return pathList;
	}

}
