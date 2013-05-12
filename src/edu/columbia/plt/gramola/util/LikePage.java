package edu.columbia.plt.gramola.util;

import com.restfb.Facebook;

/**
 * LikePage is the representative object for accepting page that a user like in Facebook
 * A container for a specific FQL
 * @author Fang-Hsiang Su, Gramola, 2013 Spring PLT
 *
 */
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
