package edu.columbia.plt.gramola.datastruct;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Set;

import edu.columbia.plt.gramola.abstractdata.GraphElement;

public class Edge implements GraphElement{
	
	private int id = -1;
	
	private Node start;
	
	private Node end;
	
	private HashMap<String, Object> variableMap;
	
	public Edge(Node start, Node end, HashMap<String, Object> variableMap) {
		this.start = start;
		this.end = end;
		this.variableMap = variableMap;
	}
	
	public void setId(int id) {
		this.id = id;
	}
	
	public int getId() {
		return this.id;
	}
	
	public Node inV() {
		return this.start;
	}
	
	public Node outV() {
		return this.end;
	}
	
	public Set<String> getVariables() {
		return this.variableMap.keySet();
	}
	
	public Object getVariableValue(String variable) {
		return this.variableMap.get(variable);
	}
	
	public void setVariableValue(String variable, Object value) {
		this.variableMap.put(variable, value);
	}
}
