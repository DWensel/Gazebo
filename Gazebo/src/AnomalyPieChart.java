//Required Imports
import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;
import javax.swing.JPanel;
import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartPanel;
import org.jfree.chart.JFreeChart;
import org.jfree.data.general.DefaultPieDataset;
import org.jfree.data.general.PieDataset;
import org.jfree.ui.ApplicationFrame;
import org.jfree.ui.RefineryUtilities;
 
@SuppressWarnings("serial")
public class AnomalyPieChart extends ApplicationFrame {
   
	//Constructor that declares the title that is passed to it and then calls a default content pane and a custom method to create the panel
	public AnomalyPieChart(String title) throws FileNotFoundException {
		super(title); 
		setContentPane(createChartPanel());
	}
	
	//This method creates and fills the dataset used by JFreeChart Pie charts
	private static PieDataset createDataset() throws FileNotFoundException {
		//Create new dataset
		DefaultPieDataset dataset = new DefaultPieDataset();
      
		//parsing a CSV file into Scanner class constructor  
		Scanner sc = new Scanner(new File("finalAnomCounts.csv"));   
		while (sc.hasNext()){  //Continues until there are no records left
			//Read in whole line as a string
			String line = sc.nextLine();
			//Make a list of values so that we can split our line by commas and store each split
			String values[] = line.split(",");
			//Now we can place the correct split into the correct variables
			String category = values[0];
			String numString = values[1];
			int numInt = Integer.parseInt(numString);//numString, which is the number of anomalies, needs to be an integer.
			//Add our new variables to the DefaultPieDataset we created
			dataset.setValue(category, numInt); 
		}   
		sc.close();  //closes the scanner   
		return dataset; //Return the dataset
	}
   
	//This method creates the chart with the passed 
	private static JFreeChart createChart(PieDataset dataset){
		//Create the 3D Pie Chart
		JFreeChart chart = ChartFactory.createPieChart3D(      
				"Normal vs Anomalies",	//Chart Title 
				dataset,   				//Data    
				true,      				//Include legend   
				true, 					//Include tooltips
				false);					//Exclude URLs.
		return chart; //Return the chart
	}
   
	//This method creates the panel that the chart will be on and called the createChart and createDataset methods
	public static JPanel createChartPanel() throws FileNotFoundException {
		JFreeChart chart = createChart(createDataset());  
		return new ChartPanel(chart); 
	}

	public static void main() throws FileNotFoundException {
		AnomalyPieChart visual = new AnomalyPieChart("Anomalies");
		//visual.dispatchEvent(new WindowEvent(visual, WindowEvent.WINDOW_CLOSED));
		visual.setDefaultCloseOperation(AnomalyPieChart.DISPOSE_ON_CLOSE);
		visual.setSize(560, 367);    
		RefineryUtilities.centerFrameOnScreen(visual);    
		visual.setVisible(true); 
	}
}