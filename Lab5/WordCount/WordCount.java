import java.io.IOException;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.GenericOptionsParser;
public class WordCount {
public static void main(String [] args) throws Exception
{
Configuration c=new Configuration();
String[] files=new GenericOptionsParser(c,args).getRemainingArgs();
Path input=new Path(files[0]);
Path output=new Path(files[1]);
Job j=new Job(c,"wordcount");
j.setJarByClass(WordCount.class);
j.setMapperClass(MapForWordCount.class);
j.setReducerClass(ReduceForWordCount.class);
j.setOutputKeyClass(Text.class);
j.setOutputValueClass(IntWritable.class);
FileInputFormat.addInputPath(j, input);
FileOutputFormat.setOutputPath(j, output);
System.exit(j.waitForCompletion(true)?0:1);
}
public static class MapForWordCount extends Mapper<LongWritable, Text, Text, IntWritable>{
public static int offset=0,lineNo=0;
public void map(LongWritable key, Text value, Context con) throws IOException, InterruptedException
{
String line = value.toString();
String[] words=line.split(" ");
con.write(new Text(line.toLowerCase()),new IntWritable(lineNo));
lineNo+=1;
for(String word: words )
{
      Text outputKey = new Text(word.toLowerCase().trim());
  IntWritable outputValue = new IntWritable(1);
  //con.write(outputKey, outputValue);
  con.write(outputKey,new IntWritable(offset));
	offset+=1;
}
}
}
public static class ReduceForWordCount extends Reducer<Text, IntWritable, Text, IntWritable>
{
public void reduce(Text word, Iterable<IntWritable> values , Iterable<IntWritable> offset,Iterable<IntWritable> lineNo, Context con) throws IOException, InterruptedException
{
int sum = 0;
   for(IntWritable off: offset)
   {
     con.write(word,new IntWritable(off.get()));
   }
int o;
for(IntWritable off : lineNo)
   {
   
   o = off.get();
   con.write(word,new IntWritable(o));
   
   }

//con.write(word, new IntWritable(sum));

   
}
}
}
