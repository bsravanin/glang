package edu.columbia.plt.gramola.datastruct;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Set;

import edu.columbia.plt.gramola.abstractdata.GraphElement;

public class Edge extends GraphElement{
	
	private int id = -1;
	
	private Node start;
	
	private Node end;
	
	private HashSet<Edge> pathParent = new HashSet<Edge>();
	
	private HashMap<String, Object> variableMap;
	
	public Edge(Node start, Node end, HashMap<String, Object> variableMap, int id) {
		this.start = start;
		this.end = end;
		this.variableMap = variableMap;
		this.id = id;
	}

	public synchronized void setId(int id) {
		this.id = id;
	}
	
	public int getId() {
		return this.id;
	}
	
	/**
	 * Returns the start Node of the current Edge
	 * @return the Node object in the start position
	 */
	public Node inV() {
		return this.start;
	}
	
	/**
	 * Returns the end Node of the current Edge
	 * @return the Node object in the end position
	 */
	public Node outV() {
		return this.end;
	}
	
	public Set<String> getVariables() {
		return this.variableMap.keySet();
	}
	
	public HashMap<String, Object> getVariableMap() {
		return this.variableMap;
	}
	
	public Object getVariableValue(String variable) {
		return this.variableMap.get(variable);
	}
	
	public synchronized void setVariableValue(String variable, Object value) {
		this.variableMap.put(variable, value);
	}
	
	/**
	 * Set the Edge parent of the current Edge. Mainly for path traversal.
	 * @param pathParent the parent Edge object
	 */
	public synchronized void addParents(Edge pathParent) {
		this.pathParent.add(pathParent);
	}
	
	/**
	 * Retrieve all Edge parents of the current Edge. Mainly for path traveral.
	 * @return all parent Edge objects of the current Edge
	 */
	public HashSet<Edge> getParents() {
		return this.pathParent;
	}
	
	public String toString() {
		return this.start.getId() + " =(" + this.id + ")=> " + this.end.getId(); 
	}
	
	public boolean equals(Object obj) {
		if (obj == null)
			return false;
		
		if (obj == this)
			return true;
		
		if (!(obj instanceof Edge))
			return false;
		
		Edge tmp = (Edge) obj;
		
		if (this.getId() == tmp.getId())
			return true;
		
		return false;
	}
}
