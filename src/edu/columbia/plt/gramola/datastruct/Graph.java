package edu.columbia.plt.gramola.datastruct;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Set;
import java.util.Stack;

import edu.columbia.plt.gramola.abstractdata.GraphElement;

public class Graph{
	
	private ArrayList<Node> nodeList = new ArrayList<Node>();
	
	private ArrayList<Edge> edgeList = new ArrayList<Edge>();
	
	private int nodeId = 0;
	
	private int edgeId = 0;
	
	public Node createNode(Object...vvlist) {
		HashMap<String, Object> variableMap = createVariableMap(vvlist);
		Node node = new Node(variableMap, nodeId++);
		this.addNode(node);
		
		return node;
	}
	
	public Edge createEdge(Node start, Node end, Object...vvlist) {
		HashMap<String, Object> variableMap = createVariableMap(vvlist);
		Edge edge = new Edge(start, end, variableMap, edgeId++);
		start.setOutE(edge);
		end.setInE(edge);
		this.addEdge(edge);
		
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
	
	public ArrayList<Node> getAllNodes() {
		return this.nodeList;
	}

	public void addEdge(Edge e) {
		this.edgeList.add(e);
	}
	
	public ArrayList<Edge> getAllEdges() {
		return this.edgeList;
	}
	
	public ArrayList<Edge> getShortestPath(Node start, Node end, Object...vvlist) {
		int min = Integer.MAX_VALUE;
		ArrayList<Edge> shortest = null;
		ArrayList<ArrayList<Edge>> allPaths = this.getPaths(start, end, vvlist);
		
		for (ArrayList<Edge> tmp: allPaths) {
			if (tmp.size() < min) {
				shortest = tmp;
			}
		}
		
		return shortest;
	}

	public ArrayList<ArrayList<Edge>> getPaths(Node start, Node end, Object...vvlist) {
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
		
		ArrayList<ArrayList<Edge>> ret = new ArrayList<ArrayList<Edge>>();
		HashSet<Edge> lastEdges = this.getPathImpl(start, end, variableMap, length);
		Iterator<Edge> lastIT = lastEdges.iterator();
		Edge tmpLast;
		
		while(lastIT.hasNext()) {
			tmpLast = lastIT.next();
			ret.addAll(constructPath(start, tmpLast));
		}

		return ret;
	}

	private HashSet<Edge> getPathImpl(Node start, Node end,
			HashMap<String, Object> variableMap, int length) {
		
		if (length == 0)
			return null;
		
		EdgeSet startSet = start.outE();
		
		if (startSet == null) {
			return null;
		}

		Iterator<Edge> sIT = startSet.iterator();
		Edge tmpEdge;
		HashSet<Edge> lastEdgeSet = new HashSet<Edge>();
		while(sIT.hasNext()) {
			tmpEdge = sIT.next();

			if (!this.checkEdgeValidity(tmpEdge, variableMap))
				continue;
			
			if (tmpEdge.outV() == end) {
				lastEdgeSet.add(tmpEdge);
			} else {
				this.setPathParent(tmpEdge, tmpEdge.outV().outE());
				lastEdgeSet.addAll(getPathImpl(tmpEdge.outV(), end, variableMap, length - 1));
			}
		}
		return lastEdgeSet;
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
			cIT.next().addParents(parent);
		}
	}
	
	private ArrayList<ArrayList<Edge>> constructPath(Node start, Edge e) {
		ArrayList<ArrayList<Edge>> paths = new ArrayList<ArrayList<Edge>>();
		/*System.out.println("Test edge " + e.inV().getVariableValue("name") + " " 
				+ e.getVariableValue("type") + " " + e.outV().getVariableValue("name"));*/
		
		if (e.inV() == start) {
			ArrayList<Edge> pathList = new ArrayList<Edge>();
			pathList.add(0, e);
			paths.add(pathList);
		}
		
		HashSet<Edge> parents = e.getParents();
		/*System.out.println("Test parent size: " + parents.size());*/
		ArrayList<ArrayList<Edge>> subPaths;
		
		for (Edge tmp: parents) {
			/*System.out.println("Test parent: " + tmp.inV().getVariableValue("name") + " "
					+ tmp.outV().getVariableValue("name"));*/
			subPaths = constructPath(start, tmp);
			Iterator<ArrayList<Edge>> subPathIT = subPaths.iterator();
			ArrayList<Edge> tmpList;
			
			while(subPathIT.hasNext()) {
				ArrayList<Edge> pathList = new ArrayList<Edge>();
				pathList.add(0, e);
				
				tmpList = subPathIT.next();
				pathList.addAll(0, tmpList);
				paths.add(pathList);
			}	
		}
		return paths;
	}
}
