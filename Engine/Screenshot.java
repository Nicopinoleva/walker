package com.zolbit;

import java.awt.AWTException;
import java.awt.Rectangle;
import java.awt.Robot;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import javax.imageio.ImageIO;
import javax.swing.JFrame;
import java.awt.Toolkit; 
 
public class Screenshot extends JFrame {
private static final long serialVersionUID = 1L;
	public static int save(String name) throws InterruptedException {
      try {
         Robot robot = new Robot();
         String fileName = name;
//       // Define an area of size 500*400 starting at coordinates (10,50)
//         Rectangle rectArea = new Rectangle(10, 50, 500, 400);
         Thread.sleep(3000);
//       Rectangle rectArea = new Rectangle(102, 428, 1156, 439);
         Rectangle rectArea = new Rectangle(Toolkit.getDefaultToolkit().getScreenSize());
         BufferedImage screenFullImage = robot.createScreenCapture(rectArea);
         ImageIO.write(screenFullImage, "png", new File(fileName));
      }
      catch (AWTException | IOException ex) {
               System.err.println(ex);
               return 1;
      }
      return 0;
   }
	public static int save_crop(String name, int x, int y, int w, int h) throws InterruptedException {
	      try {
	         Robot robot = new Robot();
	         String fileName = name;
//	       // Define an area of size 500*400 starting at coordinates (10,50)
//	         Rectangle rectArea = new Rectangle(10, 50, 500, 400);
	         Thread.sleep(3000);
	         Rectangle rectArea = new Rectangle(x, y, w, h);
	         BufferedImage screenFullImage = robot.createScreenCapture(rectArea);
	         ImageIO.write(screenFullImage, "png", new File(fileName));
	      }
	      catch (AWTException | IOException ex) {
	               System.err.println(ex);
	               return 1;
	      }
	      return 0;
	   }
}