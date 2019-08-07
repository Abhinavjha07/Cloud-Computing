import java.util.*;
import java.io.*;

public class Input
{
  public static void main(String[] args)throws Exception
  {
    Random r = new Random();
    Formatter x = new Formatter("input.txt");
    int i=0;

    while(i<100)
    {
      float a = 1+r.nextInt(100);
      float b = 1+r.nextInt(100);
      x.format("%f\t%f\n",a,b);
      i++;
    }
    //System.out.print("\n"+i);
    x.close();
  }
}
