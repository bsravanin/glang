package edu.columbia.plt.gramola.abstractdata;

import java.util.HashMap;
import java.util.Set;

/**
 * The parent of Node and Edge in Gramola
 * @author Fang-Hsiang Su, Gramola, 2013 Spring PLT
 * @param <T>
 * @param <T>
 *
 */
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
	 * Get value object for a specific variable
	 * @param variable
	 * @return
	 */
	public abstract String getVariableValue(String variable);
	/**
	 * Set value object for a specific variable
	 * @param <T>
	 * @param variable
	 * @param value
	 */
	
	public abstract void setVariableValue(String variable, String value);
	
	/**
	 * Get all variables from a GraphElement
	 * @return
	 */
	public abstract Set<String> getVariables();
	
	/**
	 * Get the variable map of a GraphElement
	 * @param <T>
	 * @return
	 */
	public abstract HashMap<String, String> getVariableMap();
}
