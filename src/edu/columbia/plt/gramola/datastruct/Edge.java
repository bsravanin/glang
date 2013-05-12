package edu.columbia.plt.gramola.datastruct;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Set;

import edu.columbia.plt.gramola.abstractdata.GraphElement;

/**
 * Edge represents the connection between two Nodes
 * @author Fang-Hsiang Su, Gramola, 2013 Spring PLT
 *
 */
public class Edge extends GraphElement{
	
	private int id = -1;
	
	private Node start;
	
	private Node end;
	
	private HashSet<Edge> pathParent = new HashSet<Edge>();
	
	private HashMap<String, String> variableMap;
	
	public Edge(Node start, Node end, HashMap<String, String> variableMap, int id) {
		this.start = start;
		this.end = end;
		this.variableMap = variableMap;
		this.id = id;
	}


	public Edge(Node start, Node end, HashMap<String, String> variableMap) {
		this.start = start;
		this.end = end;
		this.variableMap = variableMap;
	}

	/**
	 * Set Edge id
	 */
	public synchronized void setId(int id) {
		this.id = id;
	}
	
	/**
	 * Get Edge id
	 */
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
	
	/**
	 * Get all variables for describing Edge
	 */
	public Set<String> getVariables() {
		return this.variableMap.keySet();
	}
	
	/**
	 * Get the variable map containing <varName, varValue> values
	 * of Edge
	 */
	public HashMap<String, String> getVariableMap() {
		return this.variableMap;
	}
	
	/**
	 * Get the value for a specific variable
	 */
	public String getVariableValue(String variable) {
		return this.variableMap.get(variable);
	}
	
	/**
	 * Set the value for a specific variable
	 */
	public synchronized void setVariableValue(String variable, String value) {
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
	
	/**
	 * Return string containing start node id, edge id and end node id
	 */
	@Override
	public String toString() {
		return this.start.getId() + " =(" + this.id + ")=> " + this.end.getId(); 
	}
	
	/**
	 * Check if two Edge have the same id.
	 */
	@Override
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
