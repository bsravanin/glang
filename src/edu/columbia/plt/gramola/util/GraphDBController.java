package edu.columbia.plt.gramola.util;

import java.io.File;
import java.io.IOException;
import java.util.HashMap;
import java.util.Iterator;

import org.neo4j.graphdb.DynamicRelationshipType;
import org.neo4j.graphdb.GraphDatabaseService;
import org.neo4j.graphdb.Node;
import org.neo4j.graphdb.Relationship;
import org.neo4j.graphdb.Transaction;
import org.neo4j.graphdb.index.Index;
import org.neo4j.graphdb.index.IndexManager;
import org.neo4j.kernel.EmbeddedGraphDatabase;
import org.neo4j.tooling.GlobalGraphOperations;

import edu.columbia.plt.gramola.datastruct.Graph;

public class GraphDBController {
	
	private static DynamicRelationshipType connect = 
			DynamicRelationshipType.withName("connectTo");
	
	/*For storing node/edge index in neo4j*/
	private static String nodeIdxString = "nodes";
	
	private static String edgeIdxString = "edges";
	
	private String neo4jPath;

	private GraphDatabaseService graphDB;
	
	/**
	 * Each GraphDBController is only responsible for one neo4j DB.
	 * A Neo4j DB is for only one Graph object in Gramola.
	 * @param dbPath
	 */
	public GraphDBController(String dbPath) {
		this.neo4jPath = dbPath;
	}
	
	/**
	 * Create directory for neo4j DB
	 */
	public void createDB() {
		File graphDBFile = new File(this.neo4jPath);
		
		if (graphDBFile.exists()) {
			GInformer.printMessage("Find existing graph db");
			this.deleteDBDir(graphDBFile);
			GInformer.printMessage("Delete existing graph db");
		}
		graphDBFile.mkdir();
	}
	
	/**
	 * Initialize neo4j graph database
	 */
	public void initDB() {
		this.graphDB = new EmbeddedGraphDatabase(neo4jPath);
		registerShutdownHook(graphDB);
	}
	
	/**
	 * Delete directory for neo4j DB
	 * @param graphDBFile
	 */
	public void deleteDBDir(File graphDBFile) {
		if (graphDBFile.isDirectory()) {
			File[] dirFiles = graphDBFile.listFiles();
			
			for (int i = 0; i < dirFiles.length; i++) {
				deleteDBDir(dirFiles[i]);
			}
		} else if (graphDBFile.isFile()) {
			graphDBFile.delete();
		}
	}
	
	/**
	 * Get the path of graph DB controlled by this congroller
	 * @return graph DB path
	 */
	public String getGraphDBDir() {
		File graphDBFile = new File(this.neo4jPath);
		String path;
		try {
			path = graphDBFile.getCanonicalPath();
			return path;
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return null;
	}
	
	public void dump(Graph g) {
		dump(g, "id", "id");
	}
	
	/**
	 * Store Graph object of Gramola into neo4j DB
	 * Node==>Node
	 * Edge==>Relationship
	 * @param g
	 * @param nodeIdx
	 * @param edgeIdx
	 */
	public void dump(Graph g, String nodeIdx, String edgeIdx) {
		Transaction trans = this.graphDB.beginTx();
		try {
			IndexManager index = this.graphDB.index();
			Index<Node> nodes = index.forNodes(nodeIdxString);
			Index<Relationship> relations = index.forRelationships(edgeIdxString);

			Iterator<edu.columbia.plt.gramola.datastruct.Edge> eIT = g.getAllEdges().iterator();
			edu.columbia.plt.gramola.datastruct.Edge tmpEdge;
			edu.columbia.plt.gramola.datastruct.Node tmpStart;
			edu.columbia.plt.gramola.datastruct.Node tmpEnd;
			Node startDBNode;
			Node endDBNode;
			Relationship relation;
			while(eIT.hasNext()) {
				tmpEdge = eIT.next();
				tmpStart = tmpEdge.inV();
				tmpEnd = tmpEdge.outV();
				
				startDBNode = dumpNode(tmpStart);
				nodes.add(startDBNode, nodeIdx, startDBNode.getProperty(nodeIdx));
				
				endDBNode = dumpNode(tmpEnd);
				nodes.add(endDBNode, nodeIdx, endDBNode.getProperty(nodeIdx));
				
				relation = dumpRelation(startDBNode, endDBNode, tmpEdge);
				relations.add(relation, edgeIdx, relation.getProperty(edgeIdx));
				
			}
			trans.success();
			GInformer.printMessage("Graph dumping succeeds " + this.neo4jPath);
		} finally {
			trans.finish();
		}
	}
	
	/**
	 * Helper method for "dump" to dump Node
	 * @param mNode Node object in Gramola
	 * @return Node object in neo4j DB
	 */
	private Node dumpNode(edu.columbia.plt.gramola.datastruct.Node mNode) {
		Node dbNode = graphDB.createNode();
		Iterator<String> vIT = mNode.getVariables().iterator();
		String vName;
		String vValue;
		
		while(vIT.hasNext()) {
			vName = vIT.next();
			vValue = mNode.getVariableValue(vName).toString();
			dbNode.setProperty(vName, vValue);
		}
		dbNode.setProperty("id", mNode.getId());
		return dbNode;
	}
	
	/**
	 * Helper method for "dump" to dump Edge
	 * @param startDBNode startNode in neo4j DB
	 * @param endDBNode endNode in neo4j DB
	 * @param edge Edge object in Gramola
	 * @return Relationship object in neo4j
	 */
	private Relationship dumpRelation(Node startDBNode, Node endDBNode,
			edu.columbia.plt.gramola.datastruct.Edge edge) {
		Relationship relation = startDBNode.createRelationshipTo(endDBNode, connect);
		
		Iterator<String> edvIT = edge.getVariables().iterator();
		String edvName;
		String edvValue;
		
		while(edvIT.hasNext()) {
			edvName = edvIT.next();
			edvValue = edge.getVariableValue(edvName).toString();
			relation.setProperty(edvName, edvValue);
		}
		relation.setProperty("id", edge.getId());
		
		return relation;
	}
	
	/**
	 * Load Nodes and Relationships from neo4j to Gramola
	 * @return Graph object in Gramola
	 */
	public Graph load() {
		Graph g = new Graph();
		Transaction trans = this.graphDB.beginTx();
		
		try {
			Iterator<Relationship> allRelations =
					GlobalGraphOperations.at(this.graphDB).getAllRelationships().iterator();
			Relationship tmpRelation;
			Node startDBNode;
			Node endDBNode;
			edu.columbia.plt.gramola.datastruct.Node startNode;
			edu.columbia.plt.gramola.datastruct.Node endNode;
			edu.columbia.plt.gramola.datastruct.Edge edge;
			
			while(allRelations.hasNext()) {
				tmpRelation = allRelations.next();
				startDBNode = tmpRelation.getStartNode();
				endDBNode = tmpRelation.getEndNode();
				
				startNode = this.reproNode(startDBNode);
				if (!g.getAllNodes().contains(startNode))
					g.addNode(startNode);
				
				endNode = this.reproNode(endDBNode);
				if (!g.getAllNodes().contains(endNode))
					g.addNode(endNode);
				
				edge = this.reproEdge(tmpRelation, startNode, endNode);
				g.addEdge(edge);
			}
			GInformer.printMessage("Loading Graph succeeds " + this.neo4jPath);
		} finally {
			trans.finish();
		}
		
		return g;
	}
	
	/**
	 * Reconstruct Node object in Gramola from new4j DB
	 * @param dbNode
	 * @return Node object in Gramola
	 */
	private edu.columbia.plt.gramola.datastruct.Node reproNode(Node dbNode) {
		Iterator<String> pKeys = dbNode.getPropertyKeys().iterator();
		String propertyKey;
		String propertyVal;
		int idVal = - 1;
		HashMap<String, Object> variableMap = new HashMap<String, Object>();
		while(pKeys.hasNext()) {
			propertyKey = pKeys.next();
			propertyVal = dbNode.getProperty(propertyKey).toString();
			
			if (propertyKey.equals("id")) {
				idVal = Integer.parseInt(propertyVal.toString());
				continue;
			}
			variableMap.put(propertyKey, propertyVal);
		}
		edu.columbia.plt.gramola.datastruct.Node repoNode = 
				new edu.columbia.plt.gramola.datastruct.Node(variableMap, idVal);
		return repoNode;
	}
	
	/**
	 * Reconstruct Edge object in Gramola from neo4j DB
	 * @param dbRelation Relationship in neo4j
	 * @param startNode Node object in Gramola
	 * @param endNode Node object in Gramola
	 * @return Edge object in Gramola
	 */
	private edu.columbia.plt.gramola.datastruct.Edge reproEdge(Relationship dbRelation,
			edu.columbia.plt.gramola.datastruct.Node startNode,
			edu.columbia.plt.gramola.datastruct.Node endNode) {
		Iterator<String> pKeys = dbRelation.getPropertyKeys().iterator();
		String propertyKey;
		String propertyVal;
		int idVal = - 1;
		HashMap<String, Object> variableMap = new HashMap<String, Object>();
		while(pKeys.hasNext()) {
			propertyKey = pKeys.next();
			propertyVal = dbRelation.getProperty(propertyKey).toString();
			
			if (propertyKey.equals("id")) {
				idVal = Integer.parseInt(propertyVal.toString());
				continue;
			}
			variableMap.put(propertyKey, propertyVal);
		}
		edu.columbia.plt.gramola.datastruct.Edge repoEdge = 
				new edu.columbia.plt.gramola.datastruct.Edge(startNode, endNode, variableMap, idVal);
		return repoEdge;
	}
	
	/**
	 * Helper method for ensuring neo4j DB is shutdown after program terminates
	 * @param graphDB
	 */
	public static void registerShutdownHook (final GraphDatabaseService graphDB) {
		Runtime.getRuntime().addShutdownHook (new Thread() {
			public void run() {
				graphDB.shutdown();
			}
		});
		
	}

}
