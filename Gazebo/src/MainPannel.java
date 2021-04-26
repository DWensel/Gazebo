//Required Imports
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.FileNotFoundException;
import java.io.IOException;
import javax.swing.*;

//This class is responsible for the entire GUI. It uses Java Swing to create a frame and place a multi-tabbed panel on it. 
public class MainPannel {
	JFrame frame;
	//Constructor for MainPannel
	MainPannel(){
		//Frame information
		frame=new JFrame("Gazebo Inc.");
		frame.setSize(1000,600);
		frame.setLayout(null);
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		//Image icon = Toolkit.getDefaultToolkit().getImage("D:\\College\\CPSC 488 - Software Engineering\\Capstone Project\\final_workspace\\tabbedPane\\image.jpg");
		//frame.setIconImage(icon);
		
		//Panels to be added to the TabbedPane
		JPanel dashboard =new JPanel();
		JPanel inputData = new JPanel();
		JPanel graphics = new JPanel();
		
		//Panel information
		dashboard.setLayout(null);
		inputData.setLayout(null);
		graphics.setLayout(null);
		
		//Label for Dashboard
		JLabel welcome = new JLabel("Welcome, to Gazebo Incorporate Log Anyalysis and Visualiztion!");
		welcome.setBounds(450, 10, 900, 25);
		dashboard.add(welcome);
		
		//============================================= Data Panel Visuals ==========================================================
		//Label for Data Step 1
		JLabel dataStep1 = new JLabel("Step 1:  First we need to select the log file we will be analyzing!");
		dataStep1.setBounds(350,25,1000,25);
		inputData.add(dataStep1);
		
		//File Path Label
		//JLabel pathLabel = new JLabel("No File Selected");
		//pathLabel.setBounds(480, 49, 500, 25);
		//data.add(pathLabel);
		
		//Button for Preprocessing, and actionListener to perform a ProcessBuilder and Process of our python script1
		JButton selectDataButton = new JButton("Select File");
		selectDataButton.setBounds(350, 50, 105, 20);
		selectDataButton.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				try {
					ProcessBuilder pb = new ProcessBuilder("python3","script1.py");
					Process p = pb.start();
				} catch (IOException e1) {
					e1.printStackTrace();
				}
			}
		});
		inputData.add(selectDataButton);
		
		//Label for Data Step 2
		JLabel dataStep2 = new JLabel("Step 2: Now we need to Process the file, Just click the button to continue!");
		dataStep2.setBounds(350, 85, 1000, 25);
		inputData.add(dataStep2);
		
		//Button for Processing, and actionListener to perform a ProcessBuilder and Process of our python script2
		JButton confirmPreprocessing = new JButton("Process That File!");
		confirmPreprocessing.setBounds(350, 100, 150, 20);
		confirmPreprocessing.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				try {
					ProcessBuilder pb = new ProcessBuilder("python","script2.py");
					Process p = pb.start();
				} catch (IOException e1) {
					e1.printStackTrace();
				}
			}
		});
		inputData.add(confirmPreprocessing);
		
		//Label for Preprocessor information
		JLabel preprocessInfo = new JLabel("");
		preprocessInfo.setBounds(350, 130, 1000, 75);
		inputData.add(preprocessInfo);
		
		//============================================= Graphics Panel Visuals ==============================================================
		//Label for graphics
		JLabel graphicTitle = new JLabel("Fancy Graphics Hopefully");
		graphicTitle.setBounds(350, 10, 1000, 25);
		graphics.add(graphicTitle);
				
		//Label for userNotice
		JLabel userNotice = new JLabel("");
		userNotice.setBounds(380,250, 500,20);
		graphics.add(userNotice);
				
				
		//Combo Box for the options
		String graphOption[] = {"Anomaly Pie Chart", "Busiest Times Bar Graph"};
		@SuppressWarnings({ "rawtypes", "unchecked" })
		JComboBox graphCB = new JComboBox(graphOption);
		graphCB.setBounds(100,250,150,20);
		graphics.add(graphCB);
				
		//Button to show graph option selected
		JButton showButton = new JButton("Show");
		showButton.setBounds(275,250,70,20);
		graphics.add(showButton);
				
		//Action Listener for the button
		showButton.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				//Determine what graph was selected and inform user
				String displayText = "Your " + graphCB.getItemAt(graphCB.getSelectedIndex()) + " will be displayed in a new window";
				userNotice.setText(displayText);
						
				//Grab index of graph chosen
				int chosenGraph = graphCB.getSelectedIndex();
				//userNotice.setText(""+chosenGraph); Testing purposes
						
				//Make the desired chart
				if (chosenGraph == 0) {
					try {
						AnomalyPieChart.main();
						} catch (FileNotFoundException e1) {
							userNotice.setText("File Not Found. Please Make Sure To Do Previous Steps First");
						}
				}
					else if (chosenGraph == 1) {
						try {
							BusiestLineChart.main();
						} catch (FileNotFoundException e1){
							userNotice.setText("File Not Found. Please Make Sure To Do Previous Steps First");
						}
					}
				}
			});
				
		//TabbedPane is created and panels are added.
		JTabbedPane tabbedPane = new JTabbedPane();
		tabbedPane.setBounds(0,0,frame.getWidth()-16,frame.getHeight()-39);
		//make dashboard cute
		tabbedPane.add("Dashboard",dashboard);
		tabbedPane.add("Input Data & Preprocessing",inputData);
		//add a processing tab
		tabbedPane.add("Graphics",graphics);
				
		//Add the TabbedPane to the main frame, don't allow for resizing, make it visible
		frame.add(tabbedPane);
		frame.setResizable(false);
		frame.setVisible(true);
	}//end of MainPannel constructor
}