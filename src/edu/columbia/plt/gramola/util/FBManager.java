package edu.columbia.plt.gramola.util;

import java.util.HashMap;
import java.util.List;

import com.restfb.Connection;
import com.restfb.DefaultFacebookClient;
import com.restfb.FacebookClient;
import com.restfb.types.Post;
import com.restfb.types.User;
import com.restfb.types.User.Education;

import edu.columbia.plt.gramola.datastruct.Graph;
import edu.columbia.plt.gramola.datastruct.Node;

public class FBManager {
	
	private String token;
	
	private FacebookClient fbManager;
	
	private Connection<User> myFriends;
	
	private Connection<Post> myFeeds;
	
	private List<LikePage> myPages;
	
	private User me;
	
	public FBManager(String token) {
		this.token = token;
	}
	
	public void connect() {
		if (this.token == null || this.token.isEmpty()) {
			GInformer.printMessage("No active token. Please set up token first");
			GInformer.printMessage("http://https://developers.facebook.com/tools/explorer");
			return ;
		}
		
		this.fbManager = new DefaultFacebookClient(this.token);
		this.me = fbManager.fetchObject("me", User.class);
		GInformer.printMessage("Connecting to Facebook succeeds");
	}
	
	public void retrieveMyRelations() {
		this.myFriends = this.fbManager.fetchConnection("me/friends", User.class);
		this.myFeeds = this.fbManager.fetchConnection("me/feed", Post.class);
		
		String fqlQuery = 
				"SELECT page_id, name From page WHERE page_id IN (SELECT page_id FROM page_fan WHERE uid = " + this.me.getId() + ")";
		this.myPages = fbManager.executeFqlQuery(fqlQuery, LikePage.class);
	}
	
	public Graph convertToGraph() {
		Graph g = new Graph();
		
		Node myNode = this.createUserNode(g, me);
		
		this.createFriendGraph(g, myNode);
		this.createFeedGraph(g, myNode);
		this.createPageGraph(g, myNode);
		
		return g;
	}
	
	public Graph convertToFriendGraph() {
		Graph g = new Graph();
		
		Node myNode = this.createUserNode(g, me);
		
		this.createFriendGraph(g, myNode);
		
		return g;
	}
	
	public Graph convertToFeedGraph() {
		Graph g = new Graph();
		
		Node myNode = this.createUserNode(g, me);
		
		this.createFeedGraph(g, myNode);
		
		return g;
	}
	
	public Graph convertToPageGraph() {
		Graph g = new Graph();
		
		Node myNode = this.createUserNode(g, me);
		
		this.createPageGraph(g, myNode);
		
		return g;
	}
	
	private void createFriendGraph(Graph g, Node myNode) {
		Node tmpUsrNode;
		HashMap<String, String> varMap;
		for (User f: myFriends.getData()) {
			tmpUsrNode = this.createUserNode(g, f);
			varMap = new HashMap<String, String>();
			varMap.put("type", "friend");
			g.Edge(myNode, tmpUsrNode, varMap);
		}
	}
	
	private void createFeedGraph(Graph g, Node myNode) {		
		Node tmpFeedNode;
		for (Post p: myFeeds.getData()) {
			if (p.getMessage() == null || p.getMessage().isEmpty() || p.getMessage().length() == 0)
				continue;
			
			tmpFeedNode = this.createFeedNode(g, p);
			HashMap<String, String> varMap = new HashMap<String, String>();
			varMap.put("type", "feed");
			g.Edge(myNode, tmpFeedNode, varMap);
		}
	}
	
	private void createPageGraph(Graph g, Node myNode) {		
		Node tmpPageNode;
		HashMap<String, String> varMap;
		for (LikePage page: this.myPages) {
			if (page.getName() == null || page.getName().isEmpty())
				continue;
			
			tmpPageNode = this.createPageNode(g, page);
			varMap = new HashMap<String, String>();
			varMap.put("type", "page");
			g.Edge(myNode, tmpPageNode, varMap);
		}
	}
	
	private Node createUserNode(Graph g, User u) {
		String name;
		String edu;
		String home;
		String location;
		
		if (u.getName() == null || u.getName().isEmpty())
			name = "";
		else
			name = u.getName().replaceAll("-|\\s", "");
		
		List<Education> eduList = u.getEducation();
		
		if (eduList.size() <= 0)
			edu = "";
		else
			edu = u.getEducation().get(0).getSchool().getName().replaceAll("\\s", "");

		
		if (u.getHometownName() == null || u.getHometownName().isEmpty())
			home = "";
		else
			home = u.getHometownName().replaceAll("\\s", "");
		
		if (u.getLocation() == null || u.getLocation().getName() == null || u.getLocation().getName().isEmpty())
			location = "";
		else
			location = u.getLocation().getName().replaceAll("\\s", "");
		
		HashMap<String, String> usrMap = new HashMap<String, String>();
		usrMap.put("name", name);
		usrMap.put("edu", edu);
		usrMap.put("home", home);
		usrMap.put("location", location);
		Node userNode = g.Node(usrMap);
		return userNode;
	}
	
	private Node createFeedNode(Graph g, Post p) {
		String name = p.getMessage().replaceAll("\\s", "");
		long likeCount;
		String link;
		
		if (p.getLikesCount() == null)
			likeCount = 0;
		else
			likeCount = p.getLikesCount();
		
		if (p.getLink() == null)
			link = "";
		else
			link = p.getLink();
		
		HashMap<String, String> feedMap = new HashMap<String, String>();
		feedMap.put("name", name);
		feedMap.put("likes", String.valueOf(likeCount));
		feedMap.put("link", link);
		Node feedNode = g.Node(feedMap);
		return feedNode;
	}
	
	private Node createPageNode(Graph g, LikePage page) {
		String name = page.getName().replaceAll("\\s", "");
		String id = page.getId();
		
		HashMap<String, String> pageMap = new HashMap<String, String>();
		pageMap.put("name", name);
		pageMap.put("id", id);
		Node pageNode = g.Node(pageMap);
		return pageNode;
	}
	
	public List<User> getMyFriends() {
		return this.myFriends.getData();
	}
	
	public List<Post> getMyFeeds() {
		return this.myFeeds.getData();
	}
	
	public List<LikePage> getMyPages() {
		return this.myPages;
	}

}
