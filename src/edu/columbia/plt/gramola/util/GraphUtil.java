package edu.columbia.plt.gramola.util;

import java.util.HashMap;
import java.util.HashSet;
import java.util.List;

import edu.columbia.plt.gramola.datastruct.Graph;

public class GraphUtil {
	
  public static String graphDBRoot = "../db/";
	
	public static void dump(Graph g, String dir) {
		GraphDBController gc = new GraphDBController(graphDBRoot + dir);
		gc.createDB();
		gc.initDB();
		gc.dump(g);
	}
	
	public static Graph load(String dir) {
		GraphDBController gc = new GraphDBController(graphDBRoot + dir);
		gc.initDB();
		return gc.load();
	}
	
	public static void draw(Graph g, String nodeVar, String edgeVar) {
		GraphVisualizer gv = new GraphVisualizer(g, nodeVar, edgeVar);
		gv.draw();
	}
	
	public static HashSet<String> union(HashSet<String> ns1, HashSet<String> ns2) {
		HashSet<String> ret = new HashSet<String>(ns1);
		ret.addAll(ns2);

		return ret;
	}
	
	public static Graph getFB(String token) {
		FBManager fbManager = new FBManager(token);
		fbManager.connect();
		fbManager.retrieveMyRelations();
		Graph g = fbManager.convertToGraph();
		return g;
	}
	
	public static Graph getFBFriend(String token) {
		FBManager fbManager = new FBManager(token);
		fbManager.connect();
		fbManager.retrieveMyRelations();
		Graph g = fbManager.convertToFriendGraph();
		return g;
	}
	
	public static Graph getFBFeed(String token) {
		FBManager fbManager = new FBManager(token);
		fbManager.connect();
		fbManager.retrieveMyRelations();
		Graph g = fbManager.convertToFeedGraph();
		return g;
	}
	
	public static Graph getFBPage(String token) {
		FBManager fbManager = new FBManager(token);
		fbManager.connect();
		fbManager.retrieveMyRelations();
		Graph g = fbManager.convertToPageGraph();
		return g;
	}

	/**
	 * Helper method to convert var-value array into a variable map
	 * @param vvlist a var-value array with undetermined size
	 * @return a map containing <var, value> pairs
	 */
	/*public static HashMap<String, Object> createVariableMap(Object vvlist[]) {
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
	
	public static HashMap<String, Object> createVarMap(Object...vvlist) {
		return createVariableMap(vvlist);
	}*/
	
	public static HashMap<String, Object> createVarMap(List<String> var, List<? extends Object> value) {
		
		if (var.size() != value.size()) {
			GInformer.printMessage("Inconsistent var-value.");
			return null;
		}
		
		HashMap<String, Object> variableMap = new HashMap<String, Object>();
		for (int i = 0; i < var.size(); i++) {
			variableMap.put(var.get(i), value.get(i));
		}
		return variableMap;
	}
}
