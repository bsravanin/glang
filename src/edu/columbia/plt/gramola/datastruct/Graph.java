package edu.columbia.plt.gramola.datastruct;

import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Set;

import edu.columbia.plt.gramola.util.GraphUtil;

/**
 * Graph contains Nodes and Edges for representing things and relations among them
 * @author Fang-Hsiang Su, Gramola, 2013 Spring PLT
 *
 */
public class Graph{

	private ArrayList<Node> nodeList = new ArrayList<Node>();
	
	private ArrayList<Edge> edgeList = new ArrayList<Edge>();
	
	private int nodeId = 0;
	
	private int edgeId = 0;
	
	private long graphId = 0;
	
	public Graph() {
		Date now = new Date();
		this.graphId = now.getTime();
	}
	
	/**
	 * Return id of Graph.
	 * Graph id is the long representation of its creation time.
	 * @return
	 */
	public long getGraphId() {
		return this.graphId;
	}
	/**
	 * The regular way to create Node within the Graph
	 * Please note that if a Node is created by new Node()
	 * The id of this Node will be -1, which means that it has not registered to any Graph
	 * @param vvlist the length of vvlist must be even. It contains "var1", "value1", "var2", "value2"..."varN", "valueN"
	 * @return a new Node
	 */
	/*public synchronized Node Node(String...vvlist) {
		HashMap<String, String> variableMap = GraphUtil.createVariableMap(vvlist);
		Node node = new Node(variableMap, this.generateNodeId());
		this.addNode(node);
		
		return node;
	}*/
	
	public synchronized Node Node(HashMap<String, String> variableMap) {
		Node node = new Node(variableMap, this.generateNodeId());
		this.addNode(node);
		
		return node;
	}
	
	/**
	 * The regular way to create Edge within the Graph
	 * Please note that if an Edge is created by new Edge()
	 * The id of this Edge will be -1, which means that it has not registered to any Graph
	 * @param vvlist the length of vvlist must be even. It contains "var1", "value1", "var2", "value2"..."varN", "valueN"
	 * @return a new Edge
	 */
	/*public synchronized Edge Edge(Node start, Node end, String...vvlist) {
		HashMap<String, String> variableMap = GraphUtil.createVariableMap(vvlist);
		Edge edge = new Edge(start, end, variableMap, this.generateEdgeId());
		start.setOutE(edge);
		end.setInE(edge);
		this.addEdge(edge);
		
		return edge;
	}*/
	
	public synchronized Edge Edge(Node start, Node end, HashMap<String, String> variableMap) {
		Edge edge = new Edge(start, end, variableMap, this.generateEdgeId());
		start.setOutE(edge);
		end.setInE(edge);
		this.addEdge(edge);
		
		return edge;
	}
	
	/**
	 * Inserting Node into the Graph, if the Node is created by new Node()
	 * @param n a Node object that has not registered to any Graph
	 */
	public synchronized void addNode(Node n) {
		if (n.getId() == -1) {
			n.setId(this.generateNodeId());
		}
		
		//this.nodeMap.put(n.getId(), n);
		this.nodeList.add(n);
	}
	
	/**
	 * Retrieve a Node that fits the var-value requirement
	 * If multip Nodes fit the requirement, the first Node will be returned
	 * @param variable the name of the variable/attribute
	 * @param value the value of the variable/attribute
	 * @return a Node that fits the var-value requirement
	 */
	public Node getNode(String variable, String value) {
		Iterator<Node> nIT = this.nodeList.iterator();
		Node tmp;
		String tmpVal;
		
		while (nIT.hasNext()) {
			tmp = nIT.next();
			tmpVal = tmp.getVariableValue(variable);
			
			if (tmpVal.toString().equals(value.toString())) {
				return tmp;
			}
		}
		
		return null;
	}
	
	/**
	 * Retrieve all Nodes that fit the var-value requirement
	 * @param variable the name of the variable/attribute
	 * @param value the value of the variable/attribute
	 * @return a NodeSet containing all Nodes that fit the var-value requirement
	 */
	public NodeSet getNodes(String variable, String value) {
		Iterator<Node> nIT = this.nodeList.iterator();
		NodeSet ret = new NodeSet();
		Node tmp;
		String tmpVal;
		
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
	
	/**
	 * Get the Node by its unique ID
	 * @param id
	 * @return the Node with the correct ID
	 */
	public Node getNode(int id) {
		return this.nodeList.get(id);
	}

	public Node getNodeById(int id) {
		return this.nodeList.get(id);
	}

	
	/**
	 * Return the list containing all Nodes in the Graph
	 * @return a list containing all Nodes in the Graph
	 */
	public ArrayList<Node> getAllNodes() {
		return this.nodeList;
	}
	
	/**
	 * Helper method for createEdge to register Edge in Graph
	 * @param e the Edge to be registered in Graph
	 */
	public synchronized void addEdge(Edge e) {
		if (e.getId() == -1) {
			e.setId(this.generateEdgeId());
		}
		this.edgeList.add(e);
	}
	
	/**
	 * Get all Edges of a Graph
	 * @return a list containing all Edges in a Graph
	 */
	public ArrayList<Edge> getAllEdges() {
		return this.edgeList;
	}
	
	/**
	 * Get the path with shortest between two Nodes with Edges that fit the var-value requirement
	 * If more than one path have the same length, the first path will be returned.
	 * @param start the start Node of the path
	 * @param end the end Node of the path
	 * @param vvlist the var-value array
	 * @return a path (list containing all corresponding Edges in sequence) with shortest length
	 */
	public ArrayList<Edge> getShortestPath(Node start, Node end, ArrayList<String> var, ArrayList<String> val) {
		int min = Integer.MAX_VALUE;
		ArrayList<Edge> shortest = null;
		//ArrayList<ArrayList<Edge<K,V>>> allPaths = this.getPaths(start, end, vvlist);
		ArrayList<ArrayList<Edge>> allPaths = this.getPaths(start, end, var, val);
		
		for (ArrayList<Edge> tmp: allPaths) {
			if (tmp.size() < min) {
				min = tmp.size();
				shortest = tmp;
			}
		}
		
		return shortest;
	}

	/**
	 * Get all paths between two Nodes with Edges that fit the var-value requirements
	 * @param start the start Node of the path 
	 * @param end the end Node of the path
	 * @param vvlist the var-value array
	 * @return a list containing all paths with qualified Edges
	 */
	public ArrayList<ArrayList<Edge>> getPaths(Node start, Node end, ArrayList<String> var, ArrayList<String> val) {
		if (start.getId() == -1 || end.getId() == -1)
			return null;
		
		if (!this.nodeList.contains(start) || !this.nodeList.contains(end))
			return null;

		HashMap<String, String> variableMap = GraphUtil.createVarMap(var, val);
		
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

	/**
	 * Helper method to get the corresponding last Edge(s) connecting to the end Node
	 * @param start the start Node
	 * @param end the end node
	 * @param variableMap the var-value map
	 * @param length the length requirement for path
	 * @return a Set of last Edges connecting to the end Node
	 */
	private HashSet<Edge> getPathImpl(Node start, Node end,
			HashMap<String, String> variableMap, int length) {
		
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
	
	/**
	 * Helper method to check if Edge fit var-value requirements
	 * @param e the Edge to be checked
	 * @param variableMap the var-value map defines requirements
	 * @return if Edge is qualified or not
	 */
	private boolean checkEdgeValidity(Edge e, HashMap<String, String> variableMap) {
		Iterator<String> mapIT = variableMap.keySet().iterator();
		
		String variableName = null;
		while (mapIT.hasNext()) {
			variableName = mapIT.next();
			if (e.getVariableValue(variableName) == null)
				return false;
			
			if (!e.getVariableValue(variableName).equals(variableMap.get(variableName)))
				return false;
		}
		
		return true;
	}
	
	/**
	 * Helper method to set parents for Edges
	 * For path traversal
	 * @param parent the parent Edge
	 * @param childSet the child Edge
	 */
	private void setPathParent(Edge parent, EdgeSet childSet) {
		Iterator<Edge> cIT = childSet.iterator();
		while(cIT.hasNext()) {
			cIT.next().addParents(parent);
		}
	}
	
	/**
	 * Based on last Edge(s) to back-trace and construct the correct path
	 * @param start the start Node of the path
	 * @param e the last Edge
	 * @return a path (a list of qualified Edges in sequence)
	 */
	private ArrayList<ArrayList<Edge>> constructPath(Node start, Edge e) {
		ArrayList<ArrayList<Edge>> paths = new ArrayList<ArrayList<Edge>>();
		
		if (e.inV() == start) {
			ArrayList<Edge> pathList = new ArrayList<Edge>();
			pathList.add(0, e);
			paths.add(pathList);
		}
		
		HashSet<Edge> parents = e.getParents();
		ArrayList<ArrayList<Edge>> subPaths;
		
		for (Edge tmp: parents) {
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
	
	/**
	 * Helper method to generate id for Node in this Graph
	 * @return
	 */
	private synchronized int generateNodeId() {
		return this.nodeId++;
	}
	
	/**
	 * Helper method to generate id for Edge in this Graph
	 * @return
	 */
	private synchronized int generateEdgeId() {
		return this.edgeId++;
	}
	
	@Override
	public String toString() {
		return  "Graph " + this.graphId + " contains " + 
				this.nodeList.size() + " nodes and " + 
				this.edgeList.size() + " edges"; 
	}
}
