package edu.columbia.plt.gramola.datastruct;

import java.util.Collection;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Set;

public class NodeSet<V, K> implements Set{
	
	private HashSet<Node<K,V>> nodeSet = new HashSet<Node<K,V>>();
	
	/**
	 * Find out Nodes that fit var-value constraints in NodeSet
	 * @param variable
	 * @param value
	 * @return
	 */
	public NodeSet<K,V> filter(K variable, V value) {
		NodeSet<K,V> filterNodes = new NodeSet<K,V>();
		Iterator<Node<K,V>> nodeIT = nodeSet.iterator();
		Node<K,V> tmp;
		while(nodeIT.hasNext()) {
			tmp = nodeIT.next();
			if (tmp.getVariableValue(variable).toString().equals(value.toString()))
				filterNodes.add(tmp);
		}
		return filterNodes;
	}
	
	@Override
	public boolean add(Object e) {
		// TODO Auto-generated method stub
		if (e instanceof Node) {
			this.nodeSet.add((Node<K,V>)e);
			return true;
		}
		return false;
	}

	@Override
	public boolean addAll(Collection c) {
		// TODO Auto-generated method stub
		Iterator cIT = c.iterator();
		while(cIT.hasNext()) {
			if (!this.add(cIT.next())) {
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
	public boolean containsAll(Collection c) {
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
	public Iterator iterator() {
		// TODO Auto-generated method stub
		return this.nodeSet.iterator();
	}

	@Override
	public boolean remove(Object o) {
		// TODO Auto-generated method stub
		return this.nodeSet.remove(o);
	}

	@Override
	public boolean removeAll(Collection c) {
		// TODO Auto-generated method stub
		return this.nodeSet.removeAll(c);
	}

	@Override
	public boolean retainAll(Collection c) {
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
	public EdgeSet<K,V> outE() {
		EdgeSet<K,V> ret = new EdgeSet<K,V>();
		Iterator<Node<K,V>> nIT = this.nodeSet.iterator();
		
		while(nIT.hasNext()) {
			ret.add(nIT.next().outE());
		}
		
		return ret;
	}
	
	public HashSet<Object> select(K attr) {
		HashSet<Object> ret = new HashSet<Object>();
		Iterator<Node<K,V>> nIT = this.nodeSet.iterator();
		while(nIT.hasNext()) {
			ret.add(nIT.next().getVariableValue(attr).toString());
		}
		return ret;
	}
}
