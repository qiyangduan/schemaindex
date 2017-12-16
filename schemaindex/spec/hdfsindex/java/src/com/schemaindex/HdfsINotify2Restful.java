// package com.onefoursix;
// https://www.mkyong.com/java/apache-httpclient-examples/



import java.io.IOException;
import java.net.URI;

import java.io.BufferedReader; 
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;
import java.util.Date;
import java.text.DateFormat;
import java.text.SimpleDateFormat;


import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.hdfs.DFSInotifyEventInputStream;
import org.apache.hadoop.hdfs.client.HdfsAdmin;
import org.apache.hadoop.hdfs.inotify.Event;
import org.apache.hadoop.hdfs.inotify.Event.CreateEvent;
import org.apache.hadoop.hdfs.inotify.Event.RenameEvent;
import org.apache.hadoop.hdfs.inotify.Event.UnlinkEvent;
import org.apache.hadoop.hdfs.inotify.EventBatch;
import org.apache.hadoop.hdfs.inotify.MissingEventsException;


import org.apache.http.HttpResponse;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.impl.client.HttpClientBuilder;
import org.apache.http.message.BasicNameValuePair;

import org.apache.http.NameValuePair;


public class HdfsINotify2Restful {

	public static long getCheckpointTxID(String indexServerURL) throws IOException, InterruptedException, MissingEventsException  {
        String USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0";

        HttpClient client = HttpClientBuilder.create().build();
        HttpGet request = new HttpGet(indexServerURL);

        // add request header
        request.addHeader("User-Agent", USER_AGENT);
        HttpResponse response = client.execute(request);

        System.out.println("Response Code : "
                        + response.getStatusLine().getStatusCode());

        BufferedReader rd = new BufferedReader(
            new InputStreamReader(response.getEntity().getContent()));

        StringBuffer result = new StringBuffer();
        String line = "";
        while ((line = rd.readLine()) != null) {
            result.append(line);
            System.out.println(line);
            return Long.parseLong(line);
        }
        return Long.parseLong(line);

    }
            
        
    public static void main(String[] args) throws IOException, InterruptedException, MissingEventsException {
        System.out.println("parater 2 is: " +  "a");
        /*
        if (args.length == 4 ) {
			System.out.println("id is: " + getCheckpointTxID("http://localhost:8088/hdfs_inotify_get_checkpoint_txid"));
            System.exit(1);
		}
        */
        
        if (args.length < 3  ) {
			System.out.println("please input arguments in format of: INDEX_SERVER_URL DATA_SOURCE_NAME HDFS_URL [starting_trx_id] ");
            System.exit(1);
		}
        String indexServer =  args[0] ;
        String indexServerURL =  indexServer    + "/hdfs_inotify_change";  // "http://localhost:8088/hdfs_inotify_change";
        String indexServerGetCheckpointURL =  indexServer    + "/hdfs_inotify_get_checkpoint_txid";
        System.out.println("parater 2 is: " +  "a");
        String dataSourceName =  args[1] ; // "hdfs1";
        System.out.println("parater 2 is: " +  dataSourceName);
        String hdfsServerURL =  args[2] ; // "hdfs://localhost:9000";
        long lastReadTxid  = 0;
        if (args.length == 4  ) {
			lastReadTxid = Long.parseLong(args[1]);

        } else {
            lastReadTxid = getCheckpointTxID(indexServerGetCheckpointURL);
        }

        System.out.println("server is: " + indexServerURL);
        
		System.out.println("lastReadTxid = " + lastReadTxid);

		HdfsAdmin admin = new HdfsAdmin(URI.create(hdfsServerURL), new Configuration());

		DFSInotifyEventInputStream eventStream = admin.getInotifyEventStream(lastReadTxid);


 

        HttpClient client = HttpClientBuilder.create().build();

        // add header
        String USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0";

        List<NameValuePair> urlParameters ;
        urlParameters = new ArrayList<NameValuePair>();
        
        
     
        HttpPost post;
        HttpResponse response;
        DateFormat df = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss"); 
        Date d = new Date();


		while (true) {
			EventBatch batch = eventStream.take();
            String txID =  Long.toString(batch.getTxid() ); // Integer.toString(i)    
			System.out.println("Current Traction Id = " + txID);
            


			for (Event event : batch.getEvents()) {
				System.out.println("event type = " + event.getEventType());
                post = new HttpPost(indexServerURL);
                post.setHeader("User-Agent", USER_AGENT);
                urlParameters.clear();    
                urlParameters.add(new BasicNameValuePair("txid",txID)); 
                urlParameters.add(new BasicNameValuePair("data_source_name",dataSourceName)); 

                switch (event.getEventType()) {

                    case CREATE:
                        CreateEvent createEvent = (CreateEvent) event;

                        urlParameters.add(new BasicNameValuePair("event_type", "CREATE")); 
                        urlParameters.add(new BasicNameValuePair("path", createEvent.getPath())); 
                        urlParameters.add(new BasicNameValuePair("owner", createEvent.getOwnerName())); 
                        d= new Date(createEvent.getCtime());
                        urlParameters.add(new BasicNameValuePair("date_time", df.format(d))); 

                        System.out.println("  path = " + createEvent.getPath());
                        System.out.println("  owner = " + createEvent.getOwnerName());
                        System.out.println("  ctime = " + createEvent.getCtime());
                        break;
                    case UNLINK:
                        UnlinkEvent unlinkEvent = (UnlinkEvent) event;

                        urlParameters.add(new BasicNameValuePair("event_type", "UNLINK")); 
                        urlParameters.add(new BasicNameValuePair("path", unlinkEvent.getPath()));  
                        d= new Date(unlinkEvent.getTimestamp());
                        urlParameters.add(new BasicNameValuePair("date_time", df.format(d)));  

                        System.out.println("  path = " + unlinkEvent.getPath());
                        System.out.println("  timestamp = " + unlinkEvent.getTimestamp());
                        break;
                    case RENAME:
                        RenameEvent rEvent = (RenameEvent) event;

                        urlParameters.add(new BasicNameValuePair("event_type", "RENAME")); 
                        urlParameters.add(new BasicNameValuePair("src_path", rEvent.getSrcPath()));  
                        urlParameters.add(new BasicNameValuePair("dst_path", rEvent.getDstPath()));  
                        d= new Date(rEvent.getTimestamp());
                        urlParameters.add(new BasicNameValuePair("date_time", df.format(d)));  

                        System.out.println("  from = " + rEvent.getSrcPath());
                        System.out.println("  to = " + rEvent.getDstPath());
                        System.out.println("  ctime = " + rEvent.getTimestamp());
                        break;

                    case APPEND:
                    case CLOSE:
                    default:
                        continue;
				}
                post.setEntity(new UrlEncodedFormEntity(urlParameters));
                response = client.execute(post);

                System.out.println("Response Code : " + response.getStatusLine().getStatusCode());   
                BufferedReader rd = new BufferedReader(new InputStreamReader(response.getEntity().getContent()));

                StringBuffer result = new StringBuffer();
                String line = "";
                while ((line = rd.readLine()) != null) {
                    result.append(line);
                    System.out.println(line);
                }


            
            
            }
		}
	}
}

