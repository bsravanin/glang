package edu.columbia.plt.gramola.abstractdata;

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
}
