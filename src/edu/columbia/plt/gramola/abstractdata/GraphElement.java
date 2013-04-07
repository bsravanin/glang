package edu.columbia.plt.gramola.abstractdata;

import java.util.Set;

public abstract class GraphElement {
	
	public abstract void setId(int id);
	
	public abstract int getId();
	
	public abstract Set<String> getVariables();

}
