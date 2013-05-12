package edu.columbia.plt.gramola.abstractdata;

import java.util.HashMap;
import java.util.Set;

public abstract class GraphElement {
	
	/**
	 * Set id for GraphElements including Node and Edge
	 * @param id an unique identification number of GraphElement
	 */
	public abstract void setId(int id);
	
	/**
	 * Get id of GraphElements including Node and Edge
	 * @return an unique identification number of GraphElement
	 */
	public abstract int getId();
	
	public abstract Object getVariableValue(String variable);
	
	public abstract void setVariableValue(String variable, Object value);
	
	public abstract Set<String> getVariables();
	
	public abstract HashMap<String, Object> getVariableMap();
}
