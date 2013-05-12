package edu.columbia.plt.gramola.datastruct;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Set;

import edu.columbia.plt.gramola.abstractdata.GraphElement;

public class Edge<K, V> extends GraphElement{
	
	private int id = -1;
	
	private Node<K,V> start;
	
	private Node<K,V> end;
	
	private HashSet<Edge<K,V>> pathParent = new HashSet<Edge<K,V>>();
	
	private HashMap<K, V> variableMap;
	
	public Edge(Node<K,V> start, Node<K,V> end, HashMap<K, V> variableMap, int id) {
		this.start = start;
		this.end = end;
		this.variableMap = variableMap;
		this.id = id;
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
	public Node<K,V> inV() {
		return this.start;
	}
	
	/**
	 * Returns the end Node of the current Edge
	 * @return the Node object in the end position
	 */
	public Node<K,V> outV() {
		return this.end;
	}
	
	/**
	 * Get all variables for describing Edge
	 */
	public Set<K> getVariables() {
		return this.variableMap.keySet();
	}
	
	/**
	 * Get the variable map containing <varName, varValue> values
	 * of Edge
	 */
	public HashMap<K, V> getVariableMap() {
		return this.variableMap;
	}
	
	/**
	 * Get the value for a specific variable
	 */
	public V getVariableValue(K variable) {
		return this.variableMap.get(variable);
	}
	
	/**
	 * Set the value for a specific variable
	 */
	public synchronized void setVariableValue(K variable, V value) {
		this.variableMap.put(variable, value);
	}
	
	/**
	 * Set the Edge parent of the current Edge. Mainly for path traversal.
	 * @param pathParent the parent Edge object
	 */
	public synchronized void addParents(Edge<K,V> pathParent) {
		this.pathParent.add(pathParent);
	}
	
	/**
	 * Retrieve all Edge parents of the current Edge. Mainly for path traveral.
	 * @return all parent Edge objects of the current Edge
	 */
	public HashSet<Edge<K,V>> getParents() {
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
		
		Edge<K,V> tmp = (Edge<K,V>) obj;
		
		if (this.getId() == tmp.getId())
			return true;
		
		return false;
	}
}
