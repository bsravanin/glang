package edu.columbia.plt.gramola.testmain;

import java.util.Collection;
import java.util.HashSet;
import java.util.HashMap;
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

        public HashSet<String> find_co_friends(String name1, String name2) {
                Node owner1 = fbgraph1.getNode("name", name1);
                Node owner2 = fbgraph2.getNode("name", name2);
                System.out.println("owner1: " + owner1);
                System.out.println("owner2: " + owner2);
                NodeSet ns1 = owner1.outE().filter("type", "friend").outV();
                NodeSet ns2 = owner2.outE().filter("type", "friend").outV();
                HashSet<String> ns1_name = ns1.select("name");
                HashSet<String> ns2_name = ns2.select("name");
                HashSet<String> cofriend = GraphUtil.union(ns1_name, ns2_name);
                return cofriend;
        }
}

