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

   public BusiestLineChart(String frameTitle, String chartTitle) throws FileNotFoundException{
      super(frameTitle);
      JFreeChart lineChart = ChartFactory.createLineChart(
         chartTitle,
         "Date","Number of Records",
         createDataset(),
         PlotOrientation.VERTICAL,
         true,true,false);
         
      ChartPanel chartPanel = new ChartPanel(lineChart);
      chartPanel.setPreferredSize(new java.awt.Dimension(650, 400));
      setContentPane(chartPanel);
   }

   private DefaultCategoryDataset createDataset() throws FileNotFoundException {
      DefaultCategoryDataset dataset = new DefaultCategoryDataset();
      
      Scanner sc = new Scanner(new File("busiestTimes.csv"));
      
      while (sc.hasNext()) {
    	  String line = sc.nextLine();
    	  String values[] = line.split(",");
    	  String recordString = values[1];
    	  String dateString = values[0];
    	  int recordNum = Integer.parseInt(recordString);
    	  
    	  dataset.addValue(recordNum,"Volume of Traffic", dateString);
      }
      return dataset;
   }
   
   public static void main() throws FileNotFoundException {
	   BusiestLineChart chart = new BusiestLineChart(
         "Busiest Timeframe" ,
         "Traffic For Each Date");

      chart.pack();
      RefineryUtilities.centerFrameOnScreen(chart);
      chart.setVisible(true);
   }
}

