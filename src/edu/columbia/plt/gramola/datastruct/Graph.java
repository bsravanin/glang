package edu.columbia.plt.gramola.datastruct;

import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Set;
import java.util.Stack;

import edu.columbia.plt.gramola.abstractdata.GraphElement;
import edu.columbia.plt.gramola.util.GraphUtil;

public class Graph<V, K>{

	private ArrayList<Node<K,V>> nodeList = new ArrayList<Node<K,V>>();
	
	private ArrayList<Edge<K,V>> edgeList = new ArrayList<Edge<K,V>>();
	
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
	
	public synchronized Node<K,V> Node(HashMap<K, V> variableMap) {
		Node<K,V> node = new Node<K,V>(variableMap, this.generateNodeId());
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
	
	public synchronized Edge<K,V> Edge(Node<K,V> start, Node<K,V> end, HashMap<K, V> variableMap) {
		Edge<K,V> edge = new Edge<K,V>(start, end, variableMap, this.generateEdgeId());
		start.setOutE(edge);
		end.setInE(edge);
		this.addEdge(edge);
		
		return edge;
	}
	
	/**
	 * Inserting Node into the Graph, if the Node is created by new Node()
	 * @param n a Node object that has not registered to any Graph
	 */
	public synchronized void addNode(Node<K,V> n) {
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
	public Node<K,V> getNode(K variable, V value) {
		Iterator<Node<K,V>> nIT = this.nodeList.iterator();
		Node<K,V> tmp;
		V tmpVal;
		
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
	public NodeSet<K,V> getNodes(K variable, V value) {
		Iterator<Node<K,V>> nIT = this.nodeList.iterator();
		NodeSet<K,V> ret = new NodeSet<K,V>();
		Node<K,V> tmp;
		V tmpVal;
		
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
	public Node<K,V> getNode(int id) {
		return this.nodeList.get(id);
	}
	
	/**
	 * Return the list containing all Nodes in the Graph
	 * @return a list containing all Nodes in the Graph
	 */
	public ArrayList<Node<K,V>> getAllNodes() {
		return this.nodeList;
	}
	
	/**
	 * Helper method for createEdge to register Edge in Graph
	 * @param e the Edge to be registered in Graph
	 */
	public synchronized void addEdge(Edge<K,V> e) {
		if (e.getId() == -1) {
			e.setId(this.generateEdgeId());
		}
		this.edgeList.add(e);
	}
	
	/**
	 * Get all Edges of a Graph
	 * @return a list containing all Edges in a Graph
	 */
	public ArrayList<Edge<K,V>> getAllEdges() {
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
	public ArrayList<Edge<K,V>> getShortestPath(Node<K,V> start, Node<K,V> end, ArrayList<K> var, ArrayList<V> val) {
		int min = Integer.MAX_VALUE;
		ArrayList<Edge<K,V>> shortest = null;
		//ArrayList<ArrayList<Edge<K,V>>> allPaths = this.getPaths(start, end, vvlist);
		ArrayList<ArrayList<Edge<K,V>>> allPaths = this.getPaths(start, end, var, val);
		
		for (ArrayList<Edge<K,V>> tmp: allPaths) {
			if (tmp.size() < min) {
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
	public ArrayList<ArrayList<Edge<K,V>>> getPaths(Node<K,V> start, Node<K,V> end, ArrayList<K> var, ArrayList<V> val) {
		if (start.getId() == -1 || end.getId() == -1)
			return null;
		
		if (!this.nodeList.contains(start) || !this.nodeList.contains(end))
			return null;
		
		//HashMap<K, V> variableMap = GraphUtil.createVariableMap(vvlist);
		HashMap<K,V> variableMap = GraphUtil.createVarMap(var, val);
		
		int length;
		
		Set<K> keys = variableMap.keySet();
		
		if (keys.contains("length")) {
			length = Integer.valueOf(variableMap.get("length").toString()); 
			variableMap.remove("length");
		} else {
			length = Integer.MAX_VALUE;
		}
		
		if (length == 0) {
			return null;
		}
		
		ArrayList<ArrayList<Edge<K,V>>> ret = new ArrayList<ArrayList<Edge<K,V>>>();
		HashSet<Edge<K,V>> lastEdges = this.getPathImpl(start, end, variableMap, length);
		Iterator<Edge<K,V>> lastIT = lastEdges.iterator();
		Edge<K,V> tmpLast;
		
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
	private HashSet<Edge<K,V>> getPathImpl(Node<K,V> start, Node<K,V> end,
			HashMap<K, V> variableMap, int length) {
		
		if (length == 0)
			return null;
		
		EdgeSet<K,V> startSet = start.outE();
		
		if (startSet == null) {
			return null;
		}

		Iterator<Edge<K,V>> sIT = startSet.iterator();
		Edge<K,V> tmpEdge;
		HashSet<Edge<K,V>> lastEdgeSet = new HashSet<Edge<K,V>>();
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
	private boolean checkEdgeValidity(Edge<K,V> e, HashMap<K, V> variableMap) {
		Iterator<K> mapIT = variableMap.keySet().iterator();
		
		K variableName = null;
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
	private void setPathParent(Edge<K,V> parent, EdgeSet<K,V> childSet) {
		Iterator<Edge<K,V>> cIT = childSet.iterator();
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
	private ArrayList<ArrayList<Edge<K,V>>> constructPath(Node<K,V> start, Edge<K,V> e) {
		ArrayList<ArrayList<Edge<K,V>>> paths = new ArrayList<ArrayList<Edge<K,V>>>();
		/*System.out.println("Test edge " + e.inV().getVariableValue("name") + " " 
				+ e.getVariableValue("type") + " " + e.outV().getVariableValue("name"));*/
		
		if (e.inV() == start) {
			ArrayList<Edge<K,V>> pathList = new ArrayList<Edge<K,V>>();
			pathList.add(0, e);
			paths.add(pathList);
		}
		
		HashSet<Edge<K,V>> parents = e.getParents();
		/*System.out.println("Test parent size: " + parents.size());*/
		ArrayList<ArrayList<Edge<K,V>>> subPaths;
		
		for (Edge<K,V> tmp: parents) {
			/*System.out.println("Test parent: " + tmp.inV().getVariableValue("name") + " "
					+ tmp.outV().getVariableValue("name"));*/
			subPaths = constructPath(start, tmp);
			Iterator<ArrayList<Edge<K,V>>> subPathIT = subPaths.iterator();
			ArrayList<Edge<K,V>> tmpList;
			
			while(subPathIT.hasNext()) {
				ArrayList<Edge<K,V>> pathList = new ArrayList<Edge<K,V>>();
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
