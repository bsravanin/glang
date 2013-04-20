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
	
	private static String nodeIdxString = "nodes";
	
	private static String edgeIdxString = "edges";
	
	private String neo4jPath;

	private GraphDatabaseService graphDB;
	
	public GraphDBController(String dbPath) {
		this.neo4jPath = dbPath;
		this.createDBDir();
		this.graphDB = new EmbeddedGraphDatabase(neo4jPath);
		registerShutdownHook(graphDB);
	}
	
	private void createDBDir() {
		File graphDBFile = new File(this.neo4jPath);
		
		if (!graphDBFile.exists()) {
			graphDBFile.mkdir();
		}
	}
	
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
		} finally {
			trans.finish();
		}
	}
	
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
				g.addNode(startNode);
				
				endNode = this.reproNode(endDBNode);
				g.addNode(endNode);
				
				edge = this.reproEdge(tmpRelation, startNode, endNode);
				g.addEdge(edge);
				
			}
		} finally {
			trans.finish();
		}
		
		return g;
	}
	
	private edu.columbia.plt.gramola.datastruct.Node reproNode(Node dbNode) {
		Iterator<String> pKeys = dbNode.getPropertyKeys().iterator();
		String propertyKey;
		Object propertyVal;
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
	
	private edu.columbia.plt.gramola.datastruct.Edge reproEdge(Relationship dbRelation,
			edu.columbia.plt.gramola.datastruct.Node startNode,
			edu.columbia.plt.gramola.datastruct.Node endNode) {
		Iterator<String> pKeys = dbRelation.getPropertyKeys().iterator();
		String propertyKey;
		Object propertyVal;
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
	
	public static void registerShutdownHook (final GraphDatabaseService graphDB) {
		Runtime.getRuntime().addShutdownHook (new Thread() {
			public void run() {
				graphDB.shutdown();
			}
		});
		
	}

}
