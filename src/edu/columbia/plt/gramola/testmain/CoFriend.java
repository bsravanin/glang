package edu.columbia.plt.gramola.testmain;

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



class Cofriend {

        public Graph fbgraph1;
        public Graph fbgraph2;
        public HashSet cofriend;

        public void find_co_friends(String name1, String name2) {
                Node owner1 = fbgraph1.getNode("name", name1);
                Node owner2 = fbgraph2.getNode("name", name2);
                NodeSet ns1 = owner1.outE().filter("type", "friend").outV();
                NodeSet ns2 = owner2.outE().filter("type", "friend").outV();
                HashSet ns1_name = ns1.select("name");
                HashSet ns2_name = ns2.select("name");
                cofriend = GraphUtil.union(ns1_name, ns2_name);
        }

        public HashSet get_cofriend() {
                return cofriend;
        }
}

