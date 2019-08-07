import java.io.IOException;
import java.util.StringTokenizer;
import java.util.Scanner;
import java.io.FileReader;
import java.util.*;
import java.lang.Math;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.FloatWritable;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.GenericOptionsParser;
import org.apache.hadoop.filecache.DistributedCache;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;

import java.io.DataInput;
import java.io.DataOutput;
import org.apache.hadoop.io.Writable;

import org.apache.hadoop.mapreduce.InputSplit;
import org.apache.hadoop.mapreduce.RecordReader;
import org.apache.hadoop.mapreduce.TaskAttemptContext;

import java.io.StringReader;
import org.apache.hadoop.mapreduce.lib.input.LineRecordReader;


class TwoDPointFileRecordReader  extends RecordReader<LongWritable, TwoDPointWritable>{

	LineRecordReader lineReader;
	TwoDPointWritable value;

	public void initialize(InputSplit inputSplit, TaskAttemptContext attempt)
			throws IOException, InterruptedException {
		lineReader = new LineRecordReader();
		lineReader.initialize(inputSplit, attempt);

	}

	public boolean nextKeyValue() throws IOException, InterruptedException {
		if (!lineReader.nextKeyValue())
		{
			return false;
		}
		Scanner reader  = new Scanner (new StringReader(lineReader.getCurrentValue().toString()));
		float x = reader.nextFloat();
		float y = reader.nextFloat();
		value = new TwoDPointWritable();
		value.set(x,y);
		return true;
	}

	public LongWritable getCurrentKey() throws IOException,
			InterruptedException {
		return lineReader.getCurrentKey();
	}

	public TwoDPointWritable getCurrentValue() throws IOException,
			InterruptedException {
		return value;
	}

	public float getProgress() throws IOException, InterruptedException {
		return lineReader.getProgress();
	}

	public void close() throws IOException {
		lineReader.close();
	}

}



class TwoDPointFileInputFormat extends FileInputFormat<LongWritable, TwoDPointWritable>{

    public RecordReader<LongWritable, TwoDPointWritable> createRecordReader(
	InputSplit arg0, TaskAttemptContext arg1) throws IOException,
	InterruptedException {
	return new TwoDPointFileRecordReader();
    }

}

class TwoDPointWritable implements Writable {

    private FloatWritable x,y;

    public TwoDPointWritable() {
	this.x = new FloatWritable();
	this.y = new FloatWritable();
    }

    public void set ( float a, float b)
    {
	this.x.set(a);
	this.y.set(b);
    }


    public void readFields(DataInput in) throws IOException {
	x.readFields(in);
	y.readFields(in);
    }

    public void write(DataOutput out) throws IOException {
	x.write(out);
	y.write(out);
    }


    public FloatWritable getx() {
	return x;
    }

    public FloatWritable gety() {
	return y;
    }

}

class KMeansMapper
      extends Mapper<LongWritable, TwoDPointWritable, IntWritable, TwoDPointWritable>{
      public final static String centerfile="centers2.txt";
      public float[][] centroids = new float[4][2];

      public void setup(Context context) throws IOException {
	  Scanner reader = new Scanner(new FileReader(centerfile));

	  for (int  i=0; i<=3; i++ ) {
	      int pos = reader.nextInt();

	      centroids[pos][0] = reader.nextFloat();
	      centroids[pos][1] = reader.nextFloat();
	  }
      }

      public void map(LongWritable key, TwoDPointWritable value, Context context
	  ) throws IOException, InterruptedException {
	  float distance=0;
	  float mindistance=999999999.9f;
	  int winnercentroid=-1;
	  int i=0;
	  for ( i=0; i<=3; i++ ) {
	      FloatWritable X = value.getx();
	      FloatWritable Y = value.gety();
	      float x = X.get();
	      float y = Y.get();
	      //distance = (float)(Math.sqrt(( x-centroids[i][0])*(x-centroids[i][0]) + (y - centroids[i][1])*(y-centroids[i][1]))); 
	      distance = (float)((Math.abs( x-centroids[i][0]))+ (Math.abs(y - centroids[i][1])));
	      if ( distance < mindistance ) {
		  mindistance = distance;
		  winnercentroid=i;
	      }
	  }

	  IntWritable winnerCentroid = new IntWritable(winnercentroid);
	  context.write(winnerCentroid, value);
	  System.out.printf("Map: Centroid = %d distance = %f\n", winnercentroid, mindistance);
      }
  }

	class KMeansReducer
			extends Reducer<IntWritable,TwoDPointWritable,IntWritable,Text> {
	
	float ans = 0;
			public void reduce(IntWritable clusterid, Iterable<TwoDPointWritable> points,
			 Context context
		) throws IOException, InterruptedException {

		int num = 0;
		float centerx=0.0f;
		float centery=0.0f;
		ArrayList<Float> xc= new ArrayList<Float>(100);
		ArrayList<Float> yc= new ArrayList<Float>(100);
		for (TwoDPointWritable point : points) {
				num++;
				FloatWritable X = point.getx();
				FloatWritable Y = point.gety();
				float x = X.get();
				float y = Y.get();
				xc.add(x);
				yc.add(y);
				context.write(clusterid, new Text(String.format("%f %f",x,y)));
				centerx += x;
				centery += y;
		}
		centerx = centerx/num;
		centery = centery/num;
		
		float intraDist = 0.0f;
		for(int i=0;i<xc.size();i++)
		{
			
			intraDist += Math.abs(centerx-xc.get(i));
		}
		for(int i=0;i<yc.size();i++)
		{
			
			intraDist += Math.abs(centery-yc.get(i));
		}
		
		intraDist /= xc.size();		
		
		context.write(clusterid,new Text("Cluster Center : \n"));
		String pre_res = String.format("%f %f", centerx, centery);
		Text result = new Text(pre_res);
		context.write(clusterid, result);
		String ans = String.format("%f",intraDist);
		Text result2 = new Text(ans);
		context.write(clusterid, result2);
		context.write(clusterid,new Text("-----END-----\n\n"));
			}
	}

public class KMeans {

  public static void main(String[] args) throws Exception {
    Configuration conf = new Configuration();
    String[] otherArgs = new GenericOptionsParser(conf, args).getRemainingArgs();
    if (otherArgs.length != 2) {
      System.err.println("Usage: KMeans <in> <out>");
      System.exit(2);
    }

    Job job = new Job(conf, "KMeans");
    Path toCache = new Path("/centers2.txt");
    job.addCacheFile(toCache.toUri());
    job.createSymlink();

    job.setJarByClass(KMeans.class);
    job.setMapperClass(KMeansMapper.class);
    job.setReducerClass(KMeansReducer.class);

    job.setInputFormatClass (TwoDPointFileInputFormat.class);
    FileInputFormat.addInputPath(job, new Path(otherArgs[0]));

    job.setMapOutputKeyClass(IntWritable.class);
    job.setMapOutputValueClass(TwoDPointWritable.class);

    FileOutputFormat.setOutputPath(job, new Path(otherArgs[1]));
    job.setOutputKeyClass(IntWritable.class);
    job.setOutputValueClass(Text.class);

    System.exit(job.waitForCompletion(true) ? 0 : 1);
  }
}
