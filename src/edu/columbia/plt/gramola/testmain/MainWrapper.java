package edu.columbia.plt.gramola.testmain;

import edu.columbia.plt.gramola.datastruct.Edge;
import edu.columbia.plt.gramola.datastruct.Graph;
import edu.columbia.plt.gramola.datastruct.Node;
import edu.columbia.plt.gramola.util.GraphDBController;
import edu.columbia.plt.gramola.util.GraphVisualizer;
import edu.columbia.plt.gramola.util.GraphUtil;



public class MainWrapper  {

	public static void main(String[] args) {
		Graph g = (new Graph());
		Node n1 = g.Node(GraphUtil.createVarMap("name", "Michael", "age", 30, "birthday_month", 9, "popularity", 10));
		Node n2 = g.Node(GraphUtil.createVarMap("name", "David", "age", 25, "birthday_month", 5, "popularity", 8));
		Node n3 = g.Node(GraphUtil.createVarMap("name", "Jack", "age", 18, "birthday_month", 5, "popularity", 9));
		Node n4 = g.Node(GraphUtil.createVarMap("name", "Tom", "age", 26, "birthday_month", 5, "popularity", 4));
		Node n5 = g.Node(GraphUtil.createVarMap("name", "John", "age", 29, "birthday_month", 11, "popularity", 3));
		Node n6 = g.Node(GraphUtil.createVarMap("name", "shop"));
		g.Edge(g.Node(GraphUtil.createVarMap("name", "Cathy", "birthday_month", 10, "age", 20)), n5, GraphUtil.createVarMap("type", "wife"));
		g.Edge(n1, n2, GraphUtil.createVarMap("type", "fbfriend"));
		g.Edge(n1, n3, GraphUtil.createVarMap("type", "fbfriend"));
		g.Edge(n2, n3, GraphUtil.createVarMap("type", "fbfriend"));
		g.Edge(n2, n5, GraphUtil.createVarMap("type", "fbfriend"));
		g.Edge(n3, n2, GraphUtil.createVarMap("type", "fbfriend"));
		g.Edge(n3, n4, GraphUtil.createVarMap("type", "fbfriend"));
		g.Edge(n3, n4, GraphUtil.createVarMap("type", "brother"));
		g.Edge(n6, n1, GraphUtil.createVarMap("type", "fbfriend"));
		g.Edge(n6, n2, GraphUtil.createVarMap("type", "fbfriend"));
		g.Edge(n6, n3, GraphUtil.createVarMap("type", "fbfriend"));
		g.Edge(n6, n4, GraphUtil.createVarMap("type", "fbfriend"));
		g.Edge(n6, n5, GraphUtil.createVarMap("type", "fbfriend"));
		g.Edge(n6, n2, GraphUtil.createVarMap("type", "member"));
		g.Edge(n6, n4, GraphUtil.createVarMap("type", "member"));
		g.Edge(n6, n5, GraphUtil.createVarMap("type", "member"));
		g.Edge(g.Node(GraphUtil.createVarMap("name", "Claire")), n2, GraphUtil.createVarMap("type", "fbfriend"));
		g.Edge(g.Node(GraphUtil.createVarMap("name", "Judy")), n2, GraphUtil.createVarMap("type", "fbfriend"));
		g.Edge(g.Node(GraphUtil.createVarMap("name", "Jason")), n4, GraphUtil.createVarMap("type", "fbfriend"));
		g.Edge(g.Node(GraphUtil.createVarMap("name", "Jon")), n4, GraphUtil.createVarMap("type", "fbfriend"));
		g.Edge(g.Node(GraphUtil.createVarMap("name", "Bob")), n4, GraphUtil.createVarMap("type", "fbfriend"));
		GraphUtil.dump(g, "fbdata1");
		GraphUtil.draw(g, "name", "type");
	}
	
}
