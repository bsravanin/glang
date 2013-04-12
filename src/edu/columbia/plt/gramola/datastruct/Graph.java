package edu.columbia.plt.gramola.datastruct;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Set;
import java.util.Stack;

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
	
	/*Only return the first path we find*/
	public Stack<Edge> getPath(Node start, Node end, Object...vvlist) {
		if (start.getId() == -1 || end.getId() == -1)
			return null;
		
		if (!this.nodeList.contains(start) || !this.nodeList.contains(end))
			return null;
		
		HashMap<String, Object> variableMap = this.createVariableMap(vvlist);
		
		int length;
		
		Set<String> keys = variableMap.keySet();
		
		if (keys.contains("length")) {
			length = Integer.valueOf(variableMap.get("length").toString()); 
			variableMap.remove("length");
		} else {
			length = Integer.MAX_VALUE;
		}
		
		if (length == 0) {
			return null;
		}
		
		Edge lastEdge = this.getPathImpl(start, end, variableMap, length);
		Stack<Edge> pathStack = null;
		if ( lastEdge != null) {
			pathStack = this.constructPath(start, lastEdge);
		}

		return pathStack;
	}

	/*DFS*/
	private Edge getPathImpl(Node start, Node end,
			HashMap<String, Object> variableMap, int length) {
		
		EdgeSet startSet = start.outE();
		
		if (startSet == null) {
			return null;
		}
		
		/*Traverse EdgeSet of start Node*/
		Iterator<Edge> sIT = startSet.iterator();
		Edge tmpEdge;
		while(sIT.hasNext()) {
			tmpEdge = sIT.next();

			if (!this.checkEdgeValidity(tmpEdge, variableMap))
				continue;
			
			if (tmpEdge.outV() == end) {
				return tmpEdge;
			} else {
				this.setPathParent(tmpEdge, tmpEdge.outV().outE());
				return getPathImpl(tmpEdge.outV(), end, variableMap, length - 1);
			}
		}
		return null;
	}
	
	private boolean checkEdgeValidity(Edge e, HashMap<String, Object> variableMap) {
		Iterator<String> mapIT = variableMap.keySet().iterator();
		
		String variableName = null;
		while (mapIT.hasNext()) {
			variableName = mapIT.next().toString();
			if (e.getVariableValue(variableName) == null)
				return false;
			
			if (!e.getVariableValue(variableName).equals(variableMap.get(variableName)))
				return false;
		}
		
		return true;
	}
	
	private void setPathParent(Edge parent, EdgeSet childSet) {
		Iterator<Edge> cIT = childSet.iterator();
		while(cIT.hasNext()) {
			cIT.next().setParent(parent);
		}
	}
	
	private Stack<Edge> constructPath(Node start, Edge e) {
		Stack<Edge> pathStack = new Stack<Edge>();
		pathStack.push(e);
		
		Node tmpNode = e.inV();
		EdgeSet tmpSet;
		while(tmpNode != start) {
			/*System.out.println("tmpNode name: " + tmpNode.getVariableValue("name"));*/
			tmpSet = tmpNode.inE();
			
			Iterator<Edge> tmpEIT = tmpSet.iterator();
			Edge tmpEdge;
			while(tmpEIT.hasNext()) {
				tmpEdge = tmpEIT.next();
				/*System.out.println("Node name: " + tmpEdge.inV().getVariableValue("name"));
				System.out.println("Test tmpEdge: " + tmpEdge);
				System.out.println("Test e parent: " + e.getParent());*/
				if (tmpEdge == e.getParent()) {
					pathStack.push(tmpEdge);
					tmpNode = tmpEdge.inV();
					break;
				}
			}
		}
		return pathStack;
	}
}
