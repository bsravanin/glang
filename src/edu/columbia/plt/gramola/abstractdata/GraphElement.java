package edu.columbia.plt.gramola.abstractdata;

import java.util.Set;

public interface GraphElement {
	
	public void setId(int id);
	
	public int getId();
	
	public Set<String> getVariables();

}
