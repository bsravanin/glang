package edu.columbia.plt.gramola.testmain;

import java.util.Iterator;

import edu.columbia.plt.gramola.datastruct.Graph;
import edu.columbia.plt.gramola.datastruct.Node;
import edu.columbia.plt.gramola.util.GraphUtil;

public class FBTest {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		
		/*String token = 
				"CAACEdEose0cBABX58qKLlmGyikootEm4guZBkxA4NreeoxsFwzHdhYMwhELPsitzQnyNZCK7LgOjXFtGjj36wbmHZBkUn0W4DSkz6vyZAO0vKX3Y5v309b7S9yKMUnsC2zjcGpH2GUTZBL71yvTyNXhDpm48wJVAZD";
		Graph g = GraphUtil.getFB(token);*/
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
		
        Cofriend c = (new Cofriend());
        String token1 = "CAACEdEose0cBAKkgPnn06mvZB3JpV5rinhf2civssIEgzmbXowgJCnxdvulWqSMi8b6Ya5ZBD4aAtKZAK5rOyt53dvg0TS2Hp3mOD3jgucETdTD6NdsDHnHMfTqpQDc0OJogptTmXpHqB72lyKfEHZAZBOxFNZCYcZD";
        c.fbgraph1 = GraphUtil.getFBFriend(token1);
        Iterator<Node> tmpIT = c.fbgraph1.getAllNodes().iterator();
        System.out.println(c.fbgraph1);
        
        while(tmpIT.hasNext()) {
        	System.out.println("Traverse: " + tmpIT.next().getVariableValue("name"));
        }
        
        String token2 = "CAACEdEose0cBAOMuLJeBMZACsWZAtTkkjGJkxfFzPZCEldPrr72pObRCCZCdivxprsKI1H0zyhIX0eEN3OK0lZAxOVYcGkEvsO5SnQZAdpR8pyp3FXobDLV81Q0lpEJFZBDHyuHoDq5Osun3ZBZAliiVyJAaBCD1WBNsZD";
        c.fbgraph2 = GraphUtil.getFBFriend(token2);
        
        tmpIT = c.fbgraph2.getAllNodes().iterator();
        while(tmpIT.hasNext()) {
        	System.out.println("Traverse: " + tmpIT.next().getVariableValue("name"));
        }
        System.out.println(c.fbgraph2);
        //c.find_co_friends("Peter Louis Terry", "Apfelpuff JJ");

	}

}
