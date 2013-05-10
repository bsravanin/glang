package edu.columbia.plt.gramola.testmain;

import edu.columbia.plt.gramola.datastruct.Graph;
import edu.columbia.plt.gramola.util.GraphUtil;

public class FBTest {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		
		String token = 
				"https://developers.facebook.com/tools/explorer";
		Graph g = GraphUtil.getFB(token);
		//Graph g = GraphUtil.getFBFriend(token);
		//Graph g = GraphUtil.getFBFeed(token);
		//Graph g = GraphUtil.getFBPage(token);
		GraphUtil.draw(g, "name", "type");

	}

}
