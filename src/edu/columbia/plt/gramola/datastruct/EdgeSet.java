package edu.columbia.plt.gramola.datastruct;

import java.util.Collection;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Set;

public class EdgeSet<K, V> implements Set{
	
	private Set<Edge<K,V>> edgeSet = new HashSet<Edge<K,V>>();
	
	/**
	 * Find out Edges that fit variable-value constraint in the EdgeSet
	 * @param variable
	 * @param value
	 * @return
	 */
	public EdgeSet<K,V> filter(K variable, V value) {
		EdgeSet<K,V> filterEdges = new EdgeSet<K,V>();
		Iterator<Edge<K,V>> edgeIT = edgeSet.iterator();
		Edge<K,V> tmp;
		while(edgeIT.hasNext()) {
			tmp = edgeIT.next();
			if (tmp.getVariableValue(variable).toString().equals(value.toString()))
				filterEdges.add(tmp);
		}
		return filterEdges;
	}

	@Override
	public boolean add(Object e) {
		// TODO Auto-generated method stub
		if (e instanceof Edge) {
			this.edgeSet.add((Edge<K,V>)e);
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
				edgeSet.clear();
				return false;
			}
		}
		
		return true;
	}

	@Override
	public void clear() {
		// TODO Auto-generated method stub
		this.edgeSet.clear();
	}

	@Override
	public boolean contains(Object o) {
		// TODO Auto-generated method stub
		return this.edgeSet.contains(o);
	}

	@Override
	public boolean containsAll(Collection c) {
		// TODO Auto-generated method stub
		return this.edgeSet.containsAll(c);
	}

	@Override
	public boolean isEmpty() {
		// TODO Auto-generated method stub
		return this.edgeSet.isEmpty();
	}

	@Override
	public Iterator<Edge<K,V>> iterator() {
		// TODO Auto-generated method stub
		return this.edgeSet.iterator();
	}

	@Override
	public boolean remove(Object o) {
		// TODO Auto-generated method stub
		return this.edgeSet.remove(o);
	}

	@Override
	public boolean removeAll(Collection c) {
		// TODO Auto-generated method stub
		return this.edgeSet.removeAll(c);
	}

	@Override
	public boolean retainAll(Collection c) {
		// TODO Auto-generated method stub
		return this.edgeSet.retainAll(c);
	}

	@Override
	public int size() {
		// TODO Auto-generated method stub
		return this.edgeSet.size();
	}

	@Override
	public Object[] toArray() {
		// TODO Auto-generated method stub
		return this.edgeSet.toArray();
	}

	@Override
	public Object[] toArray(Object[] a) {
		// TODO Auto-generated method stub
		return this.edgeSet.toArray(a);
	}
	
	/**
	 * Return a NodeSet containing all Nodes on the end side of Edges in the EdgeSet
	 * @return a NodeSet
	 */
	public NodeSet outV() {
		NodeSet ret = new NodeSet();
		Iterator<Edge<K,V>> eIT = this.edgeSet.iterator();
		
		while(eIT.hasNext()) {
			ret.add(eIT.next().outV());
		}
		
		return ret;
	}
}
