package com.example.student.pythonlights;

//Joshua Angeley, Alex Aberman, Patrick McGee

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.EditText;

import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;

import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicHeader;
import org.apache.http.protocol.HTTP;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;


public class MainActivity extends Activity {

    public static final String EXTRA_MESSAGE = "blah";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);


    }

    /*Called when ip address button is pressed*/
//    public void changeIpAddress(View view){
//        Intent intent = new Intent(this, IpAddressActivity.class);
//        EditText editIp = (EditText) findViewById(R.id.editText);
//        String ip_address = editIp.getText().toString();
//        intent.putExtra(EXTRA_MESSAGE, ip_address);
//        startActivity(intent);
//    }

    /*Called when green lights button is pressed*/
    public void greenLightsOn(View view){



        Runnable runnable = new Runnable() {



            public void run() {

                EditText editIp = (EditText) findViewById(R.id.editText);
                String ip_address = editIp.getText().toString();

                Log.w("test", "Before HttpClient");
                DefaultHttpClient client = new DefaultHttpClient();
                Log.w("test", "httpclient is successfully made");
//                HttpPost post = new HttpPost("http://172.27.98.94/rpi");
                HttpPost post = new HttpPost("http://" + ip_address + "/rpi");

                Log.w("test", "post is successfully made");

                ArrayList lights = new ArrayList();
                JSONObject header = new JSONObject();
                try {
                    header.put("lightId", 1);
                    header.put("red", 0);
                    header.put("green", 255);
                    header.put("blue", 0);
                    header.put("intensity", 0.75);
                    Log.w("test", "individual light is made");
                } catch (JSONException e) {
                    e.printStackTrace();
                }
                lights.add(header);


                JSONObject jsonobj = new JSONObject();
                try {
                    jsonobj.put("lights", lights);
                    jsonobj.put("propagate", "true");
                    Log.w("test", "JSON data is constructed");
//                    jsonobj.put("lights", "" );
//                    jsonobj.put("propagate", "true" );
                } catch (JSONException e) {
                    e.printStackTrace();
                }

                StringEntity se = null;
                try {
                    //Todo: fix json to string
//                    se = new StringEntity(jsonobj.toString());
                    se = new StringEntity("{\"lights\":[{\"intensity\":0.75,\"red\":0,\"blue\":0,\"green\":255,\"lightId\":1}],\"propagate\":true}");
                    se.setContentType("application/json;charset=UTF-8");
                    se.setContentEncoding(new BasicHeader(HTTP.CONTENT_TYPE,"application/json;charset=UTF-8"));
                    Log.w("test", "JSON data is strigified");
                    Log.v("test", jsonobj.toString());
                } catch (UnsupportedEncodingException e) {
                    e.printStackTrace();
                }
                post.setEntity(se);

                try {
                  HttpResponse resp = client.execute(post);
//                    client.execute(post);

                    Log.w("test", "POST data is sent to raspberry pi");
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        };

        new Thread(runnable).start();

    }


    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }
}
