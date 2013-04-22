package edu.columbia.plt.gramola.util;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;

import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;

import org.gephi.io.exporter.api.ExportController;
import org.gephi.io.importer.api.Container;
import org.gephi.io.importer.api.ImportController;
import org.gephi.io.processor.plugin.DefaultProcessor;
import org.gephi.preview.api.PreviewController;
import org.gephi.preview.api.PreviewModel;
import org.gephi.preview.api.PreviewProperty;
import org.gephi.preview.api.ProcessingTarget;
import org.gephi.preview.api.RenderTarget;
import org.gephi.preview.types.DependantOriginalColor;
import org.gephi.preview.types.EdgeColor;
import org.gephi.project.api.ProjectController;
import org.gephi.project.api.Workspace;
import org.openide.util.Lookup;

import processing.core.PApplet;

import edu.columbia.plt.gramola.datastruct.Edge;
import edu.columbia.plt.gramola.datastruct.Graph;

public class GraphVisualizer {

	private static String dotFileRoot = "/Users/mikefhsu/javaws/Gramola/dotdata/";
	
	private String finalPath;
	
	private Graph g;
	
	private String nodeVar;
	
	private String edgeVar;
	
	public GraphVisualizer(Graph g, String nodeVar, String edgeVar) {
		this.g = g;
		this.nodeVar = nodeVar;
		this.edgeVar = edgeVar;
		this.createDotFile();
	}
	
	private void createDotFile() {
		finalPath = dotFileRoot + this.g.getGraphId() + ".dot";
		StringBuilder sb = new StringBuilder();
		try {
			FileWriter fw = new FileWriter(finalPath);
			BufferedWriter bw = new BufferedWriter(fw);
			
			sb.append("digraph{\n");
			for (Edge e: this.g.getAllEdges()) {
				sb.append(e.inV().getVariableValue(this.nodeVar) + " -> "
						+ e.outV().getVariableValue(this.nodeVar) + " ");
				sb.append("[ label = \"" + e.getVariableValue(edgeVar) + "\" ]");
				sb.append(" [ len = \"1\" ];\n");
			}
			sb.append("}\n");
			bw.write(sb.toString());
			bw.close();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
	/**
	 * Reference: 
	 * https://github.com/gephi/gephi-toolkit-demos/
	 * blob/master/src/org/gephi/toolkit/demos/PreviewJFrame.java
	 */
	public void draw() {
		//Init a project - and therefore a workspace
        ProjectController pc = Lookup.getDefault().lookup(ProjectController.class);
        pc.newProject();
        Workspace ws = pc.getCurrentWorkspace();

        //Import file
        ImportController importController = Lookup.getDefault().lookup(ImportController.class);
        Container container;
        try {
            File file = new File(this.finalPath);
            container = importController.importFile(file);
        } catch (Exception ex) {
            ex.printStackTrace();
            return;
        }

        //Append imported data to GraphAPI
        importController.process(container, new DefaultProcessor(), ws);

        //Preview configuration
        PreviewController previewController = Lookup.getDefault().lookup(PreviewController.class);
        PreviewModel previewModel = previewController.getModel();
        previewModel.getProperties().putValue(PreviewProperty.SHOW_NODE_LABELS, Boolean.TRUE);
        previewModel.getProperties().putValue(PreviewProperty.SHOW_EDGE_LABELS, Boolean.TRUE);
        previewModel.getProperties().putValue(PreviewProperty.NODE_LABEL_COLOR, new DependantOriginalColor(Color.BLUE));
        previewModel.getProperties().putValue(PreviewProperty.EDGE_CURVED, Boolean.FALSE);
        previewModel.getProperties().putValue(PreviewProperty.EDGE_OPACITY, 30);
        previewModel.getProperties().putValue(PreviewProperty.EDGE_RADIUS, 5L);
        previewModel.getProperties().putValue(PreviewProperty.EDGE_THICKNESS, 2);
        previewModel.getProperties().putValue(PreviewProperty.EDGE_COLOR, new EdgeColor(Color.WHITE));
        previewModel.getProperties().putValue(PreviewProperty.EDGE_RESCALE_WEIGHT, true);
        previewModel.getProperties().putValue(PreviewProperty.BACKGROUND_COLOR, Color.BLACK);
        previewModel.getProperties().putValue(PreviewProperty.ARROW_SIZE, 5);
        previewController.refreshPreview();

        //New Processing target, get the PApplet
        ProcessingTarget target = (ProcessingTarget) previewController.getRenderTarget(RenderTarget.PROCESSING_TARGET);
        PApplet applet = target.getApplet();
        applet.init();

        //Refresh the preview and reset the zoom
        previewController.render(target);
        target.refresh();
        //target.resetZoom();
        target.zoomMinus();

        //Add the applet to a JFrame and display
        JFrame frame = new JFrame(String.valueOf(this.g.getGraphId()));
        frame.setJMenuBar(this.createMenuBar(target));
        
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.getContentPane().add(applet, BorderLayout.CENTER);
        
        frame.pack();
        frame.setVisible(true);
	}
	
	private JMenuBar createMenuBar(final ProcessingTarget target) {
		JMenuBar menuBar = new JMenuBar();
		menuBar.setOpaque(true);
		menuBar.setPreferredSize(new Dimension(200,25));
		
		JMenu menu = new JMenu("Options");
		JMenuItem zoomIn = new JMenuItem("Zoom In");
		zoomIn.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				target.zoomPlus();
			}
		});
		
		JMenuItem zoomOut = new JMenuItem("Zoom out");
		zoomOut.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				target.zoomMinus();
			}
		});
		
		JMenuItem export = new JMenuItem("Export");
		export.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				ExportController exporter = 
						Lookup.getDefault().lookup(ExportController.class);
				try {
					exporter.exportFile(new File(dotFileRoot + g.getGraphId() + ".pdf"));
				} catch (IOException e1) {
					// TODO Auto-generated catch block
					e1.printStackTrace();
				}
			}
		});
		
		menu.add(zoomIn);
		menu.add(zoomOut);
		menu.add(export);
		
		menuBar.add(menu);
		
		return menuBar;
	}
}
