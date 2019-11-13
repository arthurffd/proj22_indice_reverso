# Projeto 22 - Data Engineering Challenge - Reverse Index Dictionary <br>

## Purpose: 
  this document contains necessary information to run the application and explain the purposes and expected results.<br />
<br />
Customer: Proj22 <br />
Developer: Arthur Flores Duarte <br />
<br />
Created Date: 2019/11/13 <br />
Last Updates:  <br />
<br /><br />

## Requirements:
- This application will run a Hadoop Map Reduce job in order to generate the dictionary. So a Unix environment with a Hadoop HDFS cluster is necessary. <br /><br />
- Miminum Requirements (tested with this application):
  - Hadoop Cluster using Amazon EC2 instances:
    - 01 NameNode:  t3a.large	 | 2 cores | 8 GiB RAM | 8GB HD
    - 03 DataNodes: t3a.medium | 2 cores | 4 GiB RAM | 8GB HD
    - OS: Ubuntu Server 16.04 LTS (HVM), SSD Volume Type (64-bit x86)
  <br /><br />
  
## Settings:
1- Upload the challenge dataset (https://github.com/projeto22/challenge-data-engineer/tree/master/dataset) to a folder in the NameNode server. In our example we created the following folder in namenode: <br />
  ``` mkdir ~/data/dataset  ``` <br /><br />
2- After upload the dataset files, we will need to convert these files to UTF-8 format, since some of them are in ISO-8859-1 encoding and this encoding can cause some errors in our map reduce job. 
  ``` 
  mkdir ~/data/dataset_utf8/
  cd ~/data/dataset 
  find . -type f -exec iconv -f iso-8859-1 -t utf-8 "{}" -o ~/data/dataset_utf8/"{}" \;  
  ```
  
<br /><br /> 

With your hdfs and yarn running, go to the $HADOOP_HOME dir:<br />
Create 2 folders in the HDFS: docs and out<br />
$ hdfs dfs -mkdir /docs<br />
$ hdfs dfs -mkdir /out<br />
Copy the utf8 files to the /docs folder in HDFS:<br />
$ hdfs dfs -copyFromLocal ~/data/dataset_utf8/* /docs/<br />
<br /><br />
Upload the map reduce python scripts to $HADOOP_HOME<br />
$ mkdir $HADOOP_HOME/scripts<br />
$ HADOOP_HOME/scripts/mapper3.py<br />
$ HADOOP_HOME/scripts/reducer3.py<br />

Give the proper permissions to the scripts:<br />
chmod a+x HADOOP_HOME/scripts/*er3.py<br />

Execute the Hadoop Streaming jar, informing the params( input, output, mapper, reducer, file):<br />
$HADOOP_HOME/bin/hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-2.9.2.jar  -file scripts/mapper3.py   -mapper mapper3.py   -file  scripts/reducer3.py  -reducer reducer3.py   -input  hdfs:///docs/*  -output out/index01

<br /><br />
If the Map Reduce job succeed, we can see the output result in hdfs:<br />
hdfs dfs -tail out/index01/part-00000<br />
<br />
Or we can also copy the sorted result to a local file (dict_index01.out) :<br />
hdfs dfs -cat out/index01/part-00000 | sort -k1,1 > dict_index01.out<br />

<br /><br />


