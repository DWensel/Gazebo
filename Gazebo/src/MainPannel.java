//Required Imports
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.File;
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
		JPanel visuals = new JPanel();
		
		//Panel information
		dashboard.setLayout(null);
		inputData.setLayout(null);
		visuals.setLayout(null);
		
		//Label for Dashboard
		JLabel welcome = new JLabel("Welcome, to Gazebo Incorporate Log Anyalysis and Visualiztion!");
		welcome.setBounds(350, 10, 900, 25);
		dashboard.add(welcome);
		
		//============================================================ Data Panel Visuals ===========================================================================
		//Label for Data Step 1
		JLabel dataStep1 = new JLabel("Step 1:  First we need to select the log file we will be analyzing!");
		dataStep1.setBounds(150,25,1000,25);
		inputData.add(dataStep1);
		
		//User Notice Label for Step 1
		JLabel preNotice = new JLabel("");
		preNotice.setBounds(300, 55, 500, 200);
		inputData.add(preNotice);
		
		//Button for Preprocessing, and actionListener to perform a ProcessBuilder and Process of our python script1
		JButton selectDataButton = new JButton("Select File");
		selectDataButton.setBounds(150, 50, 105, 20);
		selectDataButton.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				try {
					ProcessBuilder pb = new ProcessBuilder("python","script1.py");
					@SuppressWarnings("unused")
					Process p = pb.start();
					preNotice.setText("<html>This is the <u>Preprocessing Stage</u>. In this stage our code looks through each row in the data and cuts it down in various ways.\r\n"
							+ "Rows will be kept only if they fall between the time range that you specify. Rows with null values will also be removed because they cannot be used for analysis.\r\n"
							+ "Null values can be considered anomalies, so they will be stored in <i>nullValues.csv</i> for your viewing convenience.\r\n"
							+ "Then each record will be converted to values between 0 and 1 which makes it easier for our algorithm to detect anomalies.</html>");
				} catch (IOException e1) {
					//e1.printStackTrace();
					preNotice.setText("Something went wrong! :( Please retry.");
				}
			}
		});
		inputData.add(selectDataButton);
		
		//Label for Data Step 2
		JLabel dataStep2 = new JLabel("Step 2: Now we need to Process the file, Just click the button to continue!");
		dataStep2.setBounds(150, 300, 1000, 25);
		inputData.add(dataStep2);
		
		//User Notice Label for Step 2
		JLabel processNotice = new JLabel("");
		processNotice.setBounds(300, 305, 500, 200);
		inputData.add(processNotice);
		
		//Button for Processing, and actionListener to perform a ProcessBuilder and Process of our python script2
		JButton confirmPreprocessing = new JButton("Process That File!");
		confirmPreprocessing.setBounds(150, 325, 135, 20);
		confirmPreprocessing.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				try {
					File tempFile = new File("normalizedData.csv");
					boolean fileExists = tempFile.exists();
					if (fileExists) {
						ProcessBuilder pb = new ProcessBuilder("python","script2.py");
						@SuppressWarnings("unused")
						Process p = pb.start();
						processNotice.setText("<html>This is the <u>Processing Stage</u>. In this stage we use a method known as <em>Principle Component Analysis</em> to determine which groups of columns are the best for processing,\r\n"
							+ "and then only select those columns. Afterwards, we put the remaining data through an unsupervised machine learning algorithm, known as <em>CBLOF<em>, to determine outliers.\r\n"
							+ "Detected outliers are then matched to the original data that they go with, and this data is exported to Anomalies.csv for your viewing convenience.\r\n"
							+ "Several other CSVs are also created to facilitate chart creation which can be observed on the next tab.</html>\n\n\nPlease Move on to the Visuals Panel!");
					}
					else
					{
						processNotice.setText("File Not Found. Make Sure To Do Step 1 Found Above First!");
					}
				} catch (IOException e1) {
					e1.printStackTrace();
				}
				
			}
		});
		inputData.add(confirmPreprocessing);
		
		
		
		//========================================================= Visuals Panel Visuals ===========================================================================
		//Label for graphics
		JLabel visualTitle = new JLabel("Welcome to the Final Step!\n", SwingConstants.CENTER);
		visualTitle.setBounds(0, 10, 1000, 25);
		visuals.add(visualTitle);
				
		//Label for userNotice
		JLabel userNotice = new JLabel("");
		userNotice.setBounds(380,250, 500,20);
		visuals.add(userNotice);
				
		//Combo Box for the options
		String graphOption[] = {"Anomaly Pie Chart", "Busiest Times Bar Graph"};
		@SuppressWarnings({ "rawtypes", "unchecked" })
		JComboBox graphCB = new JComboBox(graphOption);
		graphCB.setBounds(100,250,150,20);
		visuals.add(graphCB);
				
		//Button to show graph option selected
		JButton showButton = new JButton("Show!");
		showButton.setBounds(275,250,70,20);
		visuals.add(showButton);
				
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
		tabbedPane.add("Preprocessing & Processing",inputData);
		//add a processing tab
		tabbedPane.add("Visuals",visuals);
				
		//Add the TabbedPane to the main frame, don't allow for resizing, make it visible
		frame.add(tabbedPane);
		frame.setResizable(false);
		frame.setVisible(true);
	}//end of MainPannel constructor
}