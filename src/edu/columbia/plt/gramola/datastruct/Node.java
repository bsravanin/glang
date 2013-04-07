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
	
	public void setInE(Edge e) {
		this.incoming.add(e);
	}
	
	public void setOutE(Edge e) {
		this.outgoing.add(e);
	}
	
	public EdgeSet outE() {
		return this.outgoing;
	}
	
	public EdgeSet inE() {
		return this.incoming;
	}
	
	public NodeSet in() {
		NodeSet ret = new NodeSet();
		Iterator<Edge> eIT = this.incoming.iterator();
		
		while(eIT.hasNext()) {
			ret.add(eIT.next().inV());
		}
		
		return ret;
	}
	
	public NodeSet out() {
		NodeSet ret = new NodeSet();
		Iterator<Edge> eIT = this.outgoing.iterator();
		
		while(eIT.hasNext()) {
			ret.add(eIT.next().outV());
		}
		
		return ret;
	}
	
	public void update(String variable, Object newValue) {		
		this.variableMap.put(variable, newValue);
	}
}
