//Required Imports
import org.jfree.chart.ChartPanel;
import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;
import org.jfree.chart.ChartFactory;
import org.jfree.chart.JFreeChart;
import org.jfree.ui.ApplicationFrame;
import org.jfree.ui.RefineryUtilities;
import org.jfree.chart.plot.PlotOrientation;
import org.jfree.data.category.DefaultCategoryDataset;

@SuppressWarnings("serial")
public class BusiestLineChart extends ApplicationFrame {
	//Constructor that takes the frame title and chart tile
   public BusiestLineChart(String frameTitle, String chartTitle) throws FileNotFoundException{
      super(frameTitle);//sets the frame's title. This is what is displayed in the top white portion of the frame.
      //This creates the chart itself.
      JFreeChart lineChart = ChartFactory.createLineChart(
         chartTitle, 					//chart title
         "Date","Number of Records",	//axis titles
         createDataset(),				//the dataset, in this case calls the constructor below
         PlotOrientation.VERTICAL,		//orientation of the play, vertical is standard.
         true,true,false);				//legend true, tooltips true, URLs false
      //This is the panel that the chart will be added
      ChartPanel chartPanel = new ChartPanel(lineChart);
      chartPanel.setPreferredSize(new java.awt.Dimension(650, 400));
      setContentPane(chartPanel);//This adds our new panel containing the chart to the frame 'chart' in main()
   }
   //This constructor creates the dataset
   private DefaultCategoryDataset createDataset() throws FileNotFoundException {
      DefaultCategoryDataset dataset = new DefaultCategoryDataset();
      //parsing a CSV file into Scanner class constructor  
      Scanner sc = new Scanner(new File("busiestTimes.csv"));
      while (sc.hasNext()) {					//While there is a next record
    	  String line = sc.nextLine();			//Read in the whole line to a temp variable
    	  String values[] = line.split(",");	//Split the line by comma
    	  String recordString = values[1];		//Store the first split of the line as record
    	  String dateString = values[0];		//store the second split of the line as date
    	  int recordNum = Integer.parseInt(recordString);	//we need the records to be in Integer
    	  //add the record, name of the category, date of the record into the dataset
    	  dataset.addValue(recordNum,"Volume of Traffic", dateString);
      }
      return dataset;
   }
   
   //Main class builds the chart frame and calls constructors to take care of the rest
   public static void main() throws FileNotFoundException {
	   BusiestLineChart chart = new BusiestLineChart(
         "Busiest Timeframe" , 		//Title of frame
         "Traffic For Each Date");	//Title of Chart
	  //pack allows it to be resized to the frame and display correctly
      chart.pack();
      RefineryUtilities.centerFrameOnScreen(chart); //set the frame to the center of the screen
      chart.setVisible(true);	//make it visible
   }
}

