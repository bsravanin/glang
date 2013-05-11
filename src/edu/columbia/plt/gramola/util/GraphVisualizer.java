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

	private static String dotFileRoot = "../dotdata/";
	
	private static String exportRoot = "../export/";
	
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
	
	/**
	 * Gephi lib consumes several data type for drawing. We choose dot here.
	 * Convert Node and Edge info from Graph object to a dot file.
	 */
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
	 * Visualize graph. Consume dot file created by createDotFile()
	 * Reference: 
	 * https://github.com/gephi/gephi-toolkit-demos/
	 * blob/master/src/org/gephi/toolkit/demos/PreviewJFrame.java
	 */
	public void draw() {
        ProjectController pc = Lookup.getDefault().lookup(ProjectController.class);
        pc.newProject();
        Workspace ws = pc.getCurrentWorkspace();

        ImportController importController = Lookup.getDefault().lookup(ImportController.class);
        Container container;
        try {
            File file = new File(this.finalPath);
            container = importController.importFile(file);
        } catch (Exception ex) {
            ex.printStackTrace();
            return;
        }

        importController.process(container, new DefaultProcessor(), ws);

        //Change graph (in visualization) properties here
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

        //Draw applet
        ProcessingTarget target = (ProcessingTarget) previewController.getRenderTarget(RenderTarget.PROCESSING_TARGET);
        PApplet applet = target.getApplet();
        applet.init();

        previewController.render(target);
        target.refresh();
        //target.resetZoom();
        target.zoomMinus();

        //Create UI. Title is the graph id
        JFrame frame = new JFrame(String.valueOf(this.g.getGraphId()));
        //Create menu bar
        frame.setJMenuBar(this.createMenuBar(target));
        
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.getContentPane().add(applet, BorderLayout.CENTER);
        
        frame.pack();
        frame.setVisible(true);
        GInformer.printMessage("Graph drawing succeeds");
	}
	
	/**
	 * Create menubar containing three items: zoom-in, zoom-out and pdf exporting
	 * Not allow user to specify exporting path. Use default path.
	 * @param target
	 * @return
	 */
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
					String exportName = exportRoot + g.getGraphId() + ".pdf";
					exporter.exportFile(new File(exportName));
					GInformer.printMessage("Exporting graph to pdf succeeds " + exportName);
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
