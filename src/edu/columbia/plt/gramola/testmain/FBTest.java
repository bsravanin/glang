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
				"CAACEdEose0cBABX58qKLlmGyikootEm4guZBkxA4NreeoxsFwzHdhYMwhELPsitzQnyNZCK7LgOjXFtGjj36wbmHZBkUn0W4DSkz6vyZAO0vKX3Y5v309b7S9yKMUnsC2zjcGpH2GUTZBL71yvTyNXhDpm48wJVAZD";
		Graph g = GraphUtil.getFB(token);
		/*Graph g = GraphUtil.getFBFriend(token);
		Graph g = GraphUtil.getFBFeed(token);
		Graph g = GraphUtil.getFBPage(token);*/
		//GraphUtil.draw(g, "name", "type");
		
        /*Cofriend c = (new Cofriend());
        String token1 = "CAACEdEose0cBAALXQLJp19vp1wOfNpd2AZA3GK4AU55k3NvZAM2zznUcOIWeaEigqZCXLScW5EfElaQ4uGyXsY3b6FjYdDFGeaINwqg9G8risz8xZAX2gqgu11ZBYuaVXyCZB7Qwk52DeCgwFxHxRZCA2fGXQMSLZBgZD";
        c.fbgraph1 = GraphUtil.getFBFriend(token1);
        String token2 = "CAACEdEose0cBAMGzOvFXOhHWc7VhCjZByp6RZCmvs9bnONzsXpdZBDb6GRIEzZBzObbZCZADXRFbBLPdMCJk4muxY0YGQgagDpks9qfgrJ4U1kef5kisXkbzkz7FC8NGeetRGw8Y0hlElNJr1sCu3ZAOmiQxZCUqsdYZD";
        c.fbgraph2 = GraphUtil.getFBFriend(token2);
        c.find_co_friends("PeterLouisTerry", "ApfelpuffJJ");
        System.out.println((c.get_cofriend()).toString());*/

	}

}
