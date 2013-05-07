package edu.columbia.plt.gramola.util;

import java.util.HashMap;

import edu.columbia.plt.gramola.datastruct.Graph;

public class GraphUtil {
	
	public static String graphDBRoot = "/Users/mikefhsu/javaws/Gramola/neo4jdbs/";
	
	public static void dump(Graph g, String dir) {
		GraphDBController gc = new GraphDBController(graphDBRoot + dir);
		gc.dump(g);
	}
	
	public static void draw(Graph g, String nodeVar, String edgeVar) {
		GraphVisualizer gv = new GraphVisualizer(g, nodeVar, edgeVar);
		gv.draw();
	}

	/**
	 * Helper method to convert var-value array into a variable map
	 * @param vvlist a var-value array with undetermined size
	 * @return a map containing <var, value> pairs
	 */
	public static HashMap<String, Object> createVariableMap(Object vvlist[]) {
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
	}

}
