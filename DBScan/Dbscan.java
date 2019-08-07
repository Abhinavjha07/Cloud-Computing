import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;

import java.io.IOException;
import java.util.*;

import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.mapreduce.Mapper;

import org.apache.hadoop.mapreduce.Reducer;


import java.lang.*;

import java.io.BufferedReader;
import java.io.FileReader;


class Point {
private double x;
private double y;
private double id;
private boolean isKey;
private boolean isClassed;
private boolean isBorder;
public boolean isKey () {
return isKey;
}
public boolean isBorder(){
	return isBorder;
}
public void setBorder(boolean isBorder){
	this.isBorder=isBorder;
	this.isClassed=true;
}
public void setKey (boolean isKey) {
this.isKey = isKey;
this.isClassed = true;
}
public boolean isClassed () {
return isClassed;
}
public void setClassed (boolean isClassed) {
this.isClassed = isClassed;
}
public double getX () {
return x;
}
public void setX (int x) {
this.x = x;
}
public double getY () {
return y;
}
public void setY (int y) {
this.y = y;
}
public Point () {
x = 0;
y = 0;
}
public Point (double x, double y) {
this.x = x;
this.y = y;
}
public Point (String str) {
String [] p = str.split(" ");
this.x = Double.parseDouble (p[0]);
this.y = Double.parseDouble (p[1]);
this.id=Double.parseDouble(p[2]);
}
public String print () {
return   this.x +" "+ this.y +" " +this.id;
}
}



class Utility {
	
public static double getDistance (Point p, Point q) {
double dx = p.getX ()-q.getX ();
double dy = p.getY ()-q.getY ();
double distance = Math.sqrt (dx * dx + dy * dy);
return distance;
} 

public static List<Point> isKeyPoint (List lst, Point p, int e, int minp) {
int count =0;
List<Point> tmpLst = new ArrayList<Point> ();
for (Iterator<Point> it = lst.iterator(); it.hasNext ();){
Point q = it.next();
if (getDistance(p,q) <= e) {
++count;
if (! tmpLst.contains (q)) {
tmpLst.add (q);
}
}
}
if (count >= minp) {
p.setKey(true);
return tmpLst;
}
return null;
}
public static void setListClassed (List lst) {
for (Iterator<Point> it = lst.iterator (); it.hasNext ();){
Point p = it.next ();
if (! p.isClassed ()) {
p.setClassed (true);
}
}
}

public static boolean mergeList (List a, List b) {
boolean merge = false;
for (int index = 0; index < b.size(); index++){
if (a.contains (b.get (index))) {
merge = true;
break;
}
}

if (merge) {
for (int index = 0; index <b.size();index++){
if (! a.contains (b.get (index))) {
a.add (b.get (index));
}
}
}
return merge;
}

}

class DbscanReducer 
        extends Reducer<IntWritable, Text, IntWritable, Text>{
	int e=2;
	int minp=3;
    	Text word;
	int index = 1;

    protected void reduce(IntWritable key, Iterable<Text> values, 
            Context context)
            throws IOException, InterruptedException {
        
		List<List<Point>> resultList = new ArrayList();
        Point p;
        boolean flag=false;
        String temp="";
        int i,j=0;
        List<Point> all= new ArrayList();
        List<Point> mergecandidates= new ArrayList();
        List<Point> noise=new ArrayList();
    	Point p1;
    	String line="";
    	Iterator<Text> itr = values.iterator();
        while (itr.hasNext()) {
            line=itr.next().toString();
        }

        String[] points = line.split(";");
        String temp1=points[points.length-1];
        points[points.length-1]="";
        String [] border=temp1.split(":");
        for (String w : points) {
        	if(!w.isEmpty()){
        		p1=new Point(w);
        		if(!all.contains(p1))
        		all.add(p1);
        	}
        }
        for(String t: border){
        	p1=new Point(t);
        	p1.setBorder(true);
        	if(!all.contains(p1))
        	all.add(p1);
        }
        
        
        
        
        for(i=0;i<all.size();i++){
        	flag=false; 
        	p = all.get(i);
        	if (! p.isClassed ()) {
        	List<Point> tmpLst = new ArrayList();
        	if ((tmpLst = Utility.isKeyPoint (all, p, e, minp))!= null) {
        	Utility.setListClassed (tmpLst);
        	resultList.add (tmpLst);
        	for(j=0;j<tmpLst.size();j++){
        		if(tmpLst.get(j).isBorder()&& !mergecandidates.contains(tmpLst.get(j))){
        			mergecandidates.add(tmpLst.get(j));
        			flag=true;
        		}
        	}
        	if(flag && !mergecandidates.contains(p))
        		mergecandidates.add(p);
        	
        	}
        	else
        		noise.add(p);
        	}
        }
        int length = resultList.size ();
        for ( i = 0; i <length;i++){
        for ( j = i+1; j <length;j++){
        if (Utility.mergeList (resultList.get (i), resultList.get(j))) {
        	resultList.get(j). clear ();
        	}
        }
        }
        
        for (Iterator <List<Point>> it = resultList.iterator(); it.hasNext ();){
        List<Point> lst = it.next ();
        if (lst.isEmpty ()) {
        continue;
        } 
        for(Iterator<Point> it1 = lst.iterator(); it1.hasNext();){
        Point t1 = it1.next ();
        if(mergecandidates.contains(t1))
        	{temp=t1.print()+" "+index+" "+ "1";}
        else{
        	temp=t1.print()+" "+index+ " " + "0";}
        word=new Text();
        word.set(temp);
        context.write (key,word);
        temp="";
        }
        index++;
        }
        
    }
}

class DbscanMapper
        extends Mapper<LongWritable, Text, IntWritable, Text>{

	int count=0;

    protected void map(LongWritable key, Text value, Context context)
            throws IOException, InterruptedException {
    	List<Point> lst= new ArrayList();
    	Point p;
    	String line = value.toString();
        String[] points = line.split(";");
        String temp=points[points.length-1];
        points[points.length-1]="";
        String [] border=temp.split(":");
        for (String w : points) {
        	if(!w.isEmpty()){
        		lst.add(new Point(w));
        	}
        }
        for(String t: border){
        	p=new Point(t);
        	p.setBorder(true);
        	lst.add(p);
        }
        
        context.write(new IntWritable(count++), value);
    
    }
    
}

public class Dbscan {
    public static void main(String[] args) throws Exception {        

        
        Configuration conf = new Configuration();
        Job job = new Job(conf, "Dbscan");


        job.setJarByClass(Dbscan.class);

        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        job.setMapperClass(DbscanMapper.class);
        job.setReducerClass(DbscanReducer.class);
        job.setInputFormatClass(TextInputFormat.class);
	job.setOutputFormatClass(TextOutputFormat.class);

        job.setOutputKeyClass(IntWritable.class);
        job.setOutputValueClass(Text.class);
        
        long start = new Date().getTime();
        boolean status = job.waitForCompletion(true);            
        long end = new Date().getTime();
        System.out.println("Job took "+(end-start) + " milliseconds");
        if(status)
        System.exit(0);
        else
        System.exit(1);	
        
    }
}
