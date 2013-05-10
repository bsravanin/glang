package edu.columbia.plt.gramola.util;

import com.restfb.Facebook;

public class LikePage {

	@Facebook
	private String name;
	
	@Facebook
	private String page_id;
	
	public String toString() {
		return name + " " + page_id;
	}
	
	public String getName() {
		return this.name;
	}
	
	public String getId() {
		return this.page_id;
	}

}
