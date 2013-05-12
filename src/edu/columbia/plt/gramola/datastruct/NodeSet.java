package edu.columbia.plt.gramola.datastruct;

import java.util.Collection;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Set;

/**
 * NodeSet is a Set containing Node objects
 * @author Fang-Hsiang Su, Gramola, 2013 Spring PLT
 *
 */
public class NodeSet implements Set<Node>{
	
	private HashSet<Node> nodeSet = new HashSet<Node>();

	public NodeSet(Collection<Node> nodes) {
		nodeSet.addAll(nodes);
	}

	public NodeSet() {
	}

	/**
	 * Find out Nodes that fit var-value constraints in NodeSet
	 * @param variable
	 * @param value
	 * @return
	 */
	public NodeSet filter(String variable, String value) {
		NodeSet filterNodes = new NodeSet();
		Iterator<Node> nodeIT = nodeSet.iterator();
		Node tmp;
		while(nodeIT.hasNext()) {
			tmp = nodeIT.next();
			if (tmp.getVariableValue(variable).toString().equals(value.toString()))
				filterNodes.add(tmp);
		}
		return filterNodes;
	}
	
	@Override
	public boolean add(Node n) {
		// TODO Auto-generated method stub
      return this.nodeSet.add(n);
	}

	@Override
	public boolean addAll(Collection<? extends Node> c) {
		// TODO Auto-generated method stub
		Iterator cIT = c.iterator();
		while(cIT.hasNext()) {
          if (!this.add((Node)cIT.next())) {
				nodeSet.clear();
				return false;
			}
		}
		
		return true;
	}

	@Override
	public void clear() {
		// TODO Auto-generated method stub
		this.nodeSet.clear();
	}

	@Override
	public boolean contains(Object o) {
		// TODO Auto-generated method stub
		if (o instanceof Node) {
			return this.nodeSet.contains(o);
		}
		return false;
	}

	@Override
	public boolean containsAll(Collection<?> c) {
		// TODO Auto-generated method stub
		Iterator cIT = c.iterator();
		
		while(cIT.hasNext()) {
			if (!this.nodeSet.contains(cIT.next())) {
				return false;
			}
		}
		
		return true;
	}

	@Override
	public boolean isEmpty() {
		// TODO Auto-generated method stub
		return this.nodeSet.isEmpty();
	}

	@Override
	public Iterator<Node> iterator() {
		// TODO Auto-generated method stub
		return this.nodeSet.iterator();
	}

	@Override
	public boolean remove(Object o) {
		// TODO Auto-generated method stub
		return this.nodeSet.remove(o);
	}

	@Override
	public boolean removeAll(Collection<?> c) {
		// TODO Auto-generated method stub
		return this.nodeSet.removeAll(c);
	}

	@Override
	public boolean retainAll(Collection<?> c) {
		// TODO Auto-generated method stub
		return this.nodeSet.retainAll(c);
	}

	@Override
	public int size() {
		// TODO Auto-generated method stub
		return this.nodeSet.size();
	}

	@Override
	public Object[] toArray() {
		// TODO Auto-generated method stub
		return this.nodeSet.toArray();
	}

	@Override
	public Object[] toArray(Object[] a) {
		// TODO Auto-generated method stub
		return this.nodeSet.toArray(a);
	}
	
	/**
	 * Return an EdgeSet containing all outgoing Edges from Nodes in the NodeSet
	 * @return an EdgeSet
	 */
	public EdgeSet outE() {
		EdgeSet ret = new EdgeSet();
		Iterator<Node> nIT = this.nodeSet.iterator();
		
		Iterator<Edge> tmpEIT;
		while(nIT.hasNext()) {
			tmpEIT = nIT.next().outE().iterator();
			
			while(tmpEIT.hasNext()) {
				ret.add(tmpEIT.next());
			}
		}
		
		return ret;
	}
	
	public HashSet<String> select(String attr) {
		HashSet<String> ret = new HashSet<String>();
		Iterator<Node> nIT = this.nodeSet.iterator();
		while(nIT.hasNext()) {
			ret.add(nIT.next().getVariableValue(attr).toString());
		}
		return ret;
	}
}
