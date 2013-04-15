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
	
	/**
	 * Get all variables (attributes) of GraphElement
	 * @return a Set of all variables/attributes belongs to GraphElement
	 */
	public abstract Set<String> getVariables();
	
	/**
	 * Get the map of GraphElement containing <variable/attribute, value>
	 * @return a HashMap containing key-value pair as <variable/attribute, value> 
	 */
	public abstract HashMap<String, Object> getVariableMap();
	
	/**
	 * Get the value of a specific variable/attribute
	 * @param variable the name of the variable
	 * @return the value of the specific variable/attribute
	 */
	public abstract Object getVariableValue(String variable);
	
	/**
	 * Either create a new variable/attribute with a value or 
	 * update the value for existing variable/attribute
	 * @param variable the name of the variable
	 * @param value the value of the variable
	 */
	public abstract void setVariableValue(String variable, Object value);

}
