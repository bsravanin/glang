import java.util.Collection;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Set;
import java.util.Arrays;
import java.util.ArrayList;

import edu.columbia.plt.gramola.datastruct.Edge;
import edu.columbia.plt.gramola.datastruct.Graph;
import edu.columbia.plt.gramola.datastruct.Node;
import edu.columbia.plt.gramola.datastruct.NodeSet;
import edu.columbia.plt.gramola.datastruct.EdgeSet;
import edu.columbia.plt.gramola.util.GraphDBController;
import edu.columbia.plt.gramola.util.GraphVisualizer;
import edu.columbia.plt.gramola.util.GraphUtil;


public class ad {

	public static ArrayList customermaillist(Graph fbgraph, Graph googlegraph) {
		Node fbnode_shop = fbgraph.getNode("name", "shop");
		Node googlenode_shop = googlegraph.getNode("name", "shop");
		NodeSet fbns = fbnode_shop.outE().filter("type", "member").outV().filter("birthday_month", "5");
		NodeSet googlens = googlenode_shop.outE().filter("type", "member").outV().filter("birthday_month", "5");
		HashSet fbns_name = fbns.select("name");
		HashSet googlens_name = googlens.select("name");
		HashSet give_gift_card = GraphUtil.union(fbns_name, googlens_name);
		NodeSet high_connection_set = fbnode_shop.outE().filter("type", "fbfriend").outV().filter("popular", "yes");
		NodeSet potential_customer_set = fbnode_shop.outE().filter("type", "fbfriend").outV().outE().filter("type", "fbfriend").outV();
		return (new ArrayList(Arrays.asList(give_gift_card, high_connection_set, potential_customer_set)));
	}

	public static Integer num_old_member(Graph fbgraph) {
		ArrayList nodelist = fbgraph.getAllNodes();
		Integer num = 0;
		for (Node n : nodelist) {
			if (!(n.getVariableValue("age")).equals("20")) {
				num = num + 1;
			}
		}
		return num;
	}

	public static void main(String[] args) {
		Graph fbgraph = GraphUtil.load("fbdata1");
		Graph googlegraph = GraphUtil.load("googledata1");
		ArrayList mailinglist = ad.customermaillist(fbgraph, googlegraph);
		System.out.println((mailinglist).toString());
		Integer k = ad.num_old_member(fbgraph);
		System.out.println((k).toString());
	}
	
}
