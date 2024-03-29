# Projeto 22 - Data Engineering Challenge - Reverse Index Dictionary <br>

## Purpose: 
 This document contains necessary information to run the application and explain the purposes and expected results. <br />
<br />
Customer: Proj22 <br /><br />
Developer: Arthur Flores Duarte <br /><br />
Challenge: https://github.com/projeto22/challenge-data-engineer <br /><br />
Description: for this challenge, we used a reversed index algorithm applying MapReduce from Hadoop Streaming with Python language. The solution was tested over a Hadoop HDFS cluster deployed on AWS EC2 instances.
<br /><br />
Created Date: 2019/11/12 <br />
Last Updates:  2019/11/13<br />
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
1. Upload the challenge dataset (https://github.com/projeto22/challenge-data-engineer/tree/master/dataset) to a folder in the NameNode server. In our example we created the following folder in namenode: <br />
    ` mkdir ~/data/dataset  `
  <br />
  
2. After upload the dataset files, we will need to convert these files to UTF-8 format, since some of them are in ISO-8859-1 encoding and this encoding can cause some errors in our map reduce job: 

  ```
    mkdir ~/data/dataset_utf8/ 
    cd ~/data/dataset  
    find . -type f -exec iconv -f iso-8859-1 -t utf-8 "{}" -o ~/data/dataset_utf8/"{}" \; 
  ```

<br />

3. With your Hadoop HDFS and YARN running, go to the $HADOOP_HOME dir:
  - Create 2 folders in the HDFS (docs and out):
  
  ``` 
      hdfs dfs -mkdir /docs
      hdfs dfs -mkdir /out 
  ```
   
  - Copy the utf8 files to the /docs folder in HDFS:
  
    ` hdfs dfs -copyFromLocal ~/data/dataset_utf8/* /docs/ `
  
<br />

4. Create a scripts folder into $HADOOP_HOME and upload the MapReduce python scripts into this folder:
    
    - ` mkdir $HADOOP_HOME/scripts `
    
    - [scripts/mapper.py](scripts/mapper.py)
    - [scripts/dict_reducer.py](scripts/dict_reducer.py)
    - [scripts/idx_reducer.py](scripts/idx_reducer.py)
    - [scripts/ext_reducer.py](scripts/ext_reducer.py)

  - Give the proper permissions to the scripts:<br />

    ` chmod a+x HADOOP_HOME/scripts/*er.py `

<br />
<br />

## Job Execution:
Execute the Hadoop Streaming jar, informing the params as below ( input, output, mapper, reducer, file) for each job. All the jobs will use the same input and mapper script (mapper.py), but we will change only the reducer script and the output destination: <br />

  1. Dictionary Reference Job. This job will get the words from all documents and create an index reference. <br/>
    Output format " < word > \tab < word_id > " <br/>
    Reducer script: **dict_reducer.py** - Output: out/index01

      ```
        $HADOOP_HOME/bin/hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-2.9.2.jar \
        -input  hdfs:///docs/*  \
        -file scripts/mapper.py   \
        -mapper mapper.py   \
        -file  scripts/dict_reducer.py  \
        -reducer dict_reducer.py   \
        -output out/index01
      ```
  <br/>

  2. Reversed Index Job: This job execution will get the words from all documents and create an inverted index. <br/>
      Output format: " <word_id> \tab < [ doc_id_01, doc_id_02 , ... ] > " <br/>
      Reducer script: **idx_reducer.py** - Output: out/index02

      ```
      $HADOOP_HOME/bin/hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-2.9.2.jar \
      -input  hdfs:///docs/*  \
      -file scripts/mapper.py   \
      -mapper mapper.py   \
      -file  scripts/idx_reducer.py  \
      -reducer idx_reducer.py   \
      -output out/index02
      ```
      <br />

  3. Extended Index Job: This job execution will get the words from all documents and create an extended inverted index.
      Output format: " < word > \tab < [ doc_id_01 : word_count , doc_id_02 : word_count , ... ] > " <br/>
      Reducer script: **ext_reducer.py** - Output: out/index03

    ```
      $HADOOP_HOME/bin/hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-2.9.2.jar \
      -input  hdfs:///docs/*  \
      -file scripts/mapper.py   \
      -mapper mapper.py   \
      -file  scripts/ext_reducer.py  \
      -reducer ext_reducer.py   \
      -output out/index03	  -file  scripts/reducer3.py  -reducer reducer3.py   -input  hdfs:///docs/*  -output out/index01
      ```

<br />
<br />

## Job Output:
Here is an image of our job execution in Hadoop applications Web GUI. It took 1 minute and half to execute one of the map reduce jobs in our EC2 cluster: <br/> <br/>
![Hadoop web gui job execution results!](/img/Dict_Index_MapReduce_Job_Result.png "Hadoop web gui job result")
 <br/> <br/>

We can see the output result in hdfs, using the commands below: <br />

    ``` 
      hdfs dfs -tail out/index01/part-00000  # Dictionary Reference output
      hdfs dfs -tail out/index02/part-00000  # Reversed Index output
      hdfs dfs -tail out/index03/part-00000  # Extended Reversed Index output
    ``` 
    
   or we can also copy the output result from HDFS to a local file as the following example : <br />

      ```
        hdfs dfs -copyToLocal out/index01/part-00000 output/dict_reference.out    
        hdfs dfs -copyToLocal out/index02/part-00000 output/reversed_index.out     
        hdfs dfs -copyToLocal out/index03/part-00000 output/extended_index.out    
      ```
      
  The output for the previous job executions that we've made in our environment are available in this repository:
  - Job1 - Dictionary Reference: [output/dict_reference.out.gz](output/dict_reference.out.gz)
  - Job2 - Reversed Index: [output/reversed_index.out.gz](output/reversed_index.out.gz)
  - Job3 - Extended Reversed Index: [output/extended_index.out.gz](output/extended_index.out.gz)
  <br/><br/>
  
## Quick Test:
Here is a quick test to check if the dictionary reference and the index are correct, comparing with a search on my local machine using Notepad++ : <br/> <br/>
![Comparing some words from job output and Notepad++ search!](/img/TestResults.png "Quick test results")
 <br/> <br/>
 We can see in the image above that the words "formosa", "zurich" and "zoological" have the same count of hits and the document names are matching, between Notepad++ search results and our job output in the editor.

## References:
  Setting up Hadoop cluster on AWS EC2 (4 nodes) <br/>
  https://medium.com/@jeevananandanne/setup-4-node-hadoop-cluster-on-aws-ec2-instances-1c1eeb4453bd <br/><br/>

  CRIANDO SEU PRIMEIRO CÓDIGO HADOOP EM PYTHON <br/>
  https://aquelatecnologia.com.br/2018/10/08/criando-seu-primeiro-codigo-hadoop-em-python/ <br/><br/>

  Writing An Hadoop MapReduce Program In Python  <br/>
  https://www.michael-noll.com/tutorials/writing-an-hadoop-mapreduce-program-in-python/  <br/><br/>

  ### Next steps: <br/>
  #### Spark (PySpark or Scala) and AWS EMR <br/>
   MapReduce VS Spark – Inverted Index example (spark e java) <br/>
   https://stdatalabs.com/2017/03/mapreduce-vs-spark-inverted-index/ <br/><br/>

   Real-world Python workloads on Spark: EMR clusters <br/>
   https://becominghuman.ai/real-world-python-workloads-on-spark-emr-clusters-3c6bda1a1350 <br/><br/>

   Word-count exercise with Spark on Amazon EMR (SCALA) <br/>
   https://skipperkongen.dk/2014/07/18/word-count-with-spark-on-amazon-emr/ <br/>

