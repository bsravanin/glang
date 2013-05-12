package edu.columbia.plt.gramola.datastruct;

import java.util.Collection;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Set;

/**
 * EdgeSet is a Set containing Edges with filtering functionalities
 * @author Fang-Hsiang Su, Gramola, 2013 Spring PLT
 *
 */
public class EdgeSet implements Set<Edge>{
	
	private Set<Edge> edgeSet = new HashSet<Edge>();
	
	public EdgeSet(Collection<Edge> edges) {
		edgeSet.addAll(edges);
	}

	public EdgeSet() {
	}

	/**
	 * Find out Edges that fit variable-value constraint in the EdgeSet
	 * @param variable
	 * @param value
	 * @return
	 */
	public EdgeSet filter(String variable, String value) {
		EdgeSet filterEdges = new EdgeSet();
		Iterator<Edge> edgeIT = edgeSet.iterator();
		Edge tmp;
		while(edgeIT.hasNext()) {
			tmp = edgeIT.next();
			if (tmp.getVariableValue(variable).toString().equals(value.toString()))
				filterEdges.add(tmp);
		}
		return filterEdges;
	}

	@Override
	public boolean add(Edge e) {
		// TODO Auto-generated method stub
		return this.edgeSet.add(e);
	}

	@Override
	public boolean addAll(Collection<? extends Edge> c) {
		// TODO Auto-generated method stub
		Iterator cIT = c.iterator();
		while(cIT.hasNext()) {
			if (!this.add((Edge)cIT.next())) {
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
	public Iterator<Edge> iterator() {
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
		Iterator<Edge> eIT = this.edgeSet.iterator();
		
		while(eIT.hasNext()) {
			ret.add(eIT.next().outV());
		}
		
		return ret;
	}
}
