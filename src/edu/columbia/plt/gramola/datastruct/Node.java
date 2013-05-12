package edu.columbia.plt.gramola.datastruct;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Set;

import edu.columbia.plt.gramola.abstractdata.GraphElement;

public class Node<K, V>  extends GraphElement {
		
	int id = -1;
	
	private HashMap<K, V> variableMap;
	
	private EdgeSet<K,V> incoming = new EdgeSet<K,V>();
	
	private EdgeSet<K,V> outgoing = new EdgeSet<K,V>();
		
	public Node(HashMap<K, V> variableMap, int id) {
		this.variableMap = variableMap;
		this.setId(id);
	}
	
	public Node(HashMap<K, V> variableMap) {
		this.variableMap = variableMap;
	}

	/**
	 * Set id for Node
	 */
	public synchronized void setId(int id) {
		this.id = id;
	}
	
	/**
	 * Get id of Node
	 */
	public int getId() {
		return this.id;
	}
		
	/**
	 * Get value for specific variable
	 */
	public V getVariableValue(K variable) {
		return this.variableMap.get(variable);
	}
	
	/**
	 * Set value for specific variable
	 */
	public synchronized void setVariableValue(K variable, V value) {
		this.variableMap.put(variable, value);
	}
	
	/**
	 * Get all variables describing Node
	 */
	public Set<K> getVariables() {
		return this.variableMap.keySet();
	}
	
	/**
	 * Get the variable map containing <varName, varValue> pairs
	 */
	public HashMap<K, V> getVariableMap() {
		return this.variableMap;
	}
	
	/**
	 * Set incoming Edge of the current Node
	 * @param e incoming Edge object
	 */
	public synchronized void setInE(Edge<K,V> e) {
		this.incoming.add(e);
	}
	
	/**
	 * Set outgoing Edge from the current Node
	 * @param e outgoing Edge object
	 */
	public synchronized void setOutE(Edge<K,V> e) {
		this.outgoing.add(e);
	}
	
	/**
	 * Get outgoing Edge(s) from the current Node
	 * @return an EdgeSet containing all outgoing Edge objects
	 */
	public EdgeSet<K,V> outE() {
		return this.outgoing;
	}
	
	/**
	 * Get incoming Edge(s) of the current Node
	 * @return an EdgeSet containing all incoming Edge objects
	 */
	public EdgeSet<K,V> inE() {
		return this.incoming;
	}
	
	/**
	 * Get all Nodes on the start side of incoming Edges
	 * Current Node is on the end side
	 * @return a NodeSet containing all Nodes on the start side of incoming Edges
	 */
	public NodeSet<K,V> inNeighbors() {
		NodeSet<K,V> ret = new NodeSet<K,V>();
		Iterator<Edge<K,V>> eIT = this.incoming.iterator();
		
		while(eIT.hasNext()) {
			ret.add(eIT.next().inV());
		}
		
		return ret;
	}
	
	/**
	 * Get all Nodes on the end side of outgoing Edges
	 * Current Node is on the start side
	 * @return a NodeSet containing all Nodes on the end side of outgoing Edges
	 */
	public NodeSet<K,V> outNeighbors() {
		NodeSet<K,V> ret = new NodeSet<K,V>();
		Iterator<Edge<K,V>> eIT = this.outgoing.iterator();
		
		while(eIT.hasNext()) {
			ret.add(eIT.next().outV());
		}
		
		return ret;
	}
	
	/**
	 * Update the value of a specific variable within the current Node
	 * @param variable the name of the specific variable
	 * @param newValue the new value of the specific variable
	 */
	public synchronized void update(K variable, V newValue) {		
		this.variableMap.put(variable, newValue);
	}
	
	@Override
	public String toString() {
		return String.valueOf(this.id);
	}
	
	/**
	 * If two Node have the same id, they are the same
	 */
	@Override
	public boolean equals(Object obj) {
		if (obj == null)
			return false;
		
		if (obj == this)
			return true;
		
		if (!(obj instanceof Node))
			return false;
		
		Node<K,V> tmp = (Node<K,V>) obj;
		
		if (this.getId() == tmp.getId())
			return true;
		
		return false;
	}
}
