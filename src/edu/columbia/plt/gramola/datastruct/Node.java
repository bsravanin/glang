package edu.columbia.plt.gramola.datastruct;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Set;

import edu.columbia.plt.gramola.abstractdata.GraphElement;

public class Node extends GraphElement{
		
	int id = -1;
	
	private HashMap<String, Object> variableMap;
	
	private EdgeSet incoming = new EdgeSet();
	
	private EdgeSet outgoing = new EdgeSet();
		
	public Node(HashMap<String, Object> variableMap, int id) {
		this.variableMap = variableMap;
		this.id = id;
	}
	
	public Node(HashMap<String, Object> variableMap) {
		this.variableMap = variableMap;
	}

	public void setId(int id) {
		this.id = id;
	}
	
	public int getId() {
		return this.id;
	}
		
	public Object getVariableValue(String variable) {
		return this.variableMap.get(variable);
	}
	
	public void setVariableValue(String variable, Object value) {
		this.variableMap.put(variable, value);
	}
	
	public Set<String> getVariables() {
		return this.variableMap.keySet();
	}
	
	public HashMap<String, Object> getVariableMap() {
		return this.variableMap;
	}
	
	/**
	 * Set incoming Edge of the current Node
	 * @param e incoming Edge object
	 */
	public void setInE(Edge e) {
		this.incoming.add(e);
	}
	
	/**
	 * Set outgoing Edge from the current Node
	 * @param e outgoing Edge object
	 */
	public void setOutE(Edge e) {
		this.outgoing.add(e);
	}
	
	/**
	 * Get outgoing Edge(s) from the current Node
	 * @return an EdgeSet containing all outgoing Edge objects
	 */
	public EdgeSet outE() {
		return this.outgoing;
	}
	
	/**
	 * Get incoming Edge(s) of the current Node
	 * @return an EdgeSet containing all incoming Edge objects
	 */
	public EdgeSet inE() {
		return this.incoming;
	}
	
	/**
	 * Get all Nodes on the start side of incoming Edges
	 * Current Node is on the end side
	 * @return a NodeSet containing all Nodes on the start side of incoming Edges
	 */
	public NodeSet in() {
		NodeSet ret = new NodeSet();
		Iterator<Edge> eIT = this.incoming.iterator();
		
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
	public NodeSet out() {
		NodeSet ret = new NodeSet();
		Iterator<Edge> eIT = this.outgoing.iterator();
		
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
	public void update(String variable, Object newValue) {		
		this.variableMap.put(variable, newValue);
	}
}
