package edu.columbia.plt.gramola.datastruct;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Set;

import edu.columbia.plt.gramola.abstractdata.GraphElement;

public class Graph{
	
	private ArrayList<Node> nodeList = new ArrayList<Node>();
	
	private int nodeId = 0;
	
	public Node createNode(Object...vvlist) {
		HashMap<String, Object> variableMap = createVariableMap(vvlist);
		Node node = new Node(variableMap, nodeId++);
		this.addNode(node);
		
		return node;
	}
	
	public Edge createEdge(Node start, Node end, Object...vvlist) {
		HashMap<String, Object> variableMap = createVariableMap(vvlist);
		Edge edge = new Edge(start, end, variableMap);
		start.setOutE(edge);
		end.setInE(edge);
		
		return edge;
	}
	
	private HashMap<String, Object> createVariableMap(Object vvlist[]) {
		if (vvlist.length%2 != 0)
			return null;
		
		HashMap<String, Object> variableMap = new HashMap<String, Object>();
		String variable;
		Object value;
		for (int i = 0; i < vvlist.length; i += 2) {
			variable = (String)vvlist[i];
			value = vvlist[i + 1];
			
			variableMap.put(variable, value);
		}
		
		return variableMap;
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
