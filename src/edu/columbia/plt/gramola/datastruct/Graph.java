package edu.columbia.plt.gramola.datastruct;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Set;

import edu.columbia.plt.gramola.abstractdata.GraphElement;

public class Graph{
	
	private HashMap<Integer, Node> nodeMap;
	
	private ArrayList<Node> nodeList;
	
	private int nodeId = 0;
	
	public void createNode(HashMap<String, Object> variableMap) {
		Node node = new Node(variableMap, nodeId++);
		this.addNode(node);
	}
	
	public void addNode(Node n) {
		if (n.getId() == -1) {
			n.setId(nodeId++);
		}
		
		//this.nodeMap.put(n.getId(), n);
		this.nodeList.add(n);
	}
	
	public Node getNode(String variable, Object value) {
		Iterator<Node> nIT = this.nodeList.iterator();
		Node tmp;
		HashMap<String, Object> tmpMap;
		Object tmpVal;
		
		while (nIT.hasNext()) {
			tmp = nIT.next();
			tmpVal = tmp.getVariableValue(variable);
			
			if (tmpVal.toString().equals(value.toString())) {
				return tmp;
			}
		}
		
		return null;
	}
	
	public NodeSet getNodes(String variable, Object value) {
		Iterator<Node> nIT = this.nodeList.iterator();
		NodeSet ret = new NodeSet();
		Node tmp;
		HashMap<String, Object> tmpMap;
		Object tmpVal;
		
		while (nIT.hasNext()) {
			tmp = nIT.next();
			tmpVal = tmp.getVariableValue(variable);
			
			if (tmpVal.toString().equals(value.toString())) {
				ret.add(tmp);
			}
		}
		
		if (ret.size() == 0) {
			return null;
		}
		
		return ret;
	}
	
	public Node getNode(int id) {
		return this.nodeList.get(id);
	}	
}
