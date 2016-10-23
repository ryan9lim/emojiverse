package com.emojiverse.emojiverse;


import com.android.volley.AuthFailureError;
import com.android.volley.NetworkError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.ServerError;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.google.android.gms.appindexing.Action;
import com.google.android.gms.appindexing.AppIndex;
import com.google.android.gms.common.api.GoogleApiClient;

import android.annotation.SuppressLint;
import android.app.ProgressDialog;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Matrix;
import android.graphics.drawable.BitmapDrawable;
import android.media.ExifInterface;
import android.media.Image;
import android.net.Uri;
import android.support.v7.app.ActionBar;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.os.Handler;
import android.util.Base64;
import android.util.Log;
import android.view.MotionEvent;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.Toast;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Hashtable;
import java.util.List;
import java.util.Map;

/**
 * An example full-screen activity that shows and hides the system UI (i.e.
 * status bar and navigation/system bar) with user interaction.
 */
public class ImageActivity extends AppCompatActivity {

    Button emojiButton;
    ImageView imageView;
    List<ProgressDialog> dialogList = new ArrayList<>();
    private String KEY_IMAGE = "image";
    String photo_url;
    private Communicator communicator;
    /**
     * ATTENTION: This was auto-generated to implement the App Indexing API.
     * See https://g.co/AppIndexing/AndroidStudio for more information.
     */
    private GoogleApiClient client;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.activity_image);


        communicator = new Communicator();
        imageView = (ImageView) findViewById(R.id.image);
        photo_url = getIntent().getStringExtra("photo_url");
        Bitmap raw_bitmap = BitmapFactory.decodeFile(photo_url);
        ExifInterface exif = null;
        try {
            exif = new ExifInterface(photo_url);
        } catch (IOException exception) {

        }
        int orientation = exif.getAttributeInt(ExifInterface.TAG_ORIENTATION, 1);
        Matrix matrix = new Matrix();
        switch (orientation) {
            case 3:
                matrix.postRotate(180);
                break;
            case 6:
                matrix.postRotate(90);
                break;
            case 8:
                matrix.postRotate(270);
                break;
        }
        final Bitmap bitmap = Bitmap.createBitmap(raw_bitmap, 0, 0, raw_bitmap.getWidth(), raw_bitmap.getHeight(), matrix, true);
        imageView.setImageBitmap(bitmap);
        emojiButton = (Button) findViewById(R.id.button_emojify);
        emojiButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                volleyRequest();
            }
        });
        // ATTENTION: This was auto-generated to implement the App Indexing API.
        // See https://g.co/AppIndexing/AndroidStudio for more information.
        client = new GoogleApiClient.Builder(this).addApi(AppIndex.API).build();
    }

    void volleyRequest() {
        final Bitmap bitmap = ((BitmapDrawable) imageView.getDrawable()).getBitmap();
        emojiButton.setEnabled(false);
        final ProgressDialog dialog = new ProgressDialog(ImageActivity.this);
        dialogList.add(dialog);
        dialog.show();
        RequestQueue queue = Volley.newRequestQueue(ImageActivity.this);
        String url = "http://192.168.43.242:5000/get_image";

//        JSONObject obj = new JSONObject();
        String image = getStringImage(bitmap);
//        try {
////            obj.put(KEY_IMAGE, image);
//            obj.put("name", "Androidhive");
//        } catch (JSONException e) {
//            Log.d("error","Failed to create object");
//            e.printStackTrace();
//        }
//        Log.d("json obj",obj.toString());
//        usePost(image);
/*
        JsonObjectRequest jsonObjectRequest = new JsonObjectRequest(Request.Method.POST, url,
                null, new Response.Listener<JSONObject>(){

            @Override
            public void onResponse(JSONObject response) {
                dialog.dismiss();

                Toast.makeText(getApplicationContext(), getString(R.string.success_emojify), Toast.LENGTH_LONG).show();
                Log.d("params",response.toString());
//                byte[] decodedString = Base64.decode(response, Base64.DEFAULT);
//                Bitmap decodedByte = BitmapFactory.decodeByteArray(decodedString, 0, decodedString.length);
//                imageView.setImageBitmap(decodedByte);
//                photoSuccess(decodedByte);
            }
        }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                emojiButton.setEnabled(true);
                dialog.dismiss();
                Log.e("Connect Error", "" + error.getMessage());
                new AlertDialog.Builder(ImageActivity.this)
                        .setTitle("Error")
                        .setMessage("Could not connect to server")
                        .show();
            }
        })
        {
            @Override
            protected Map<String, String> getParams() {
                Map<String, String> params = new HashMap<String, String>();
                params.put("name", "Androidhive");
                params.put("email", "abc@androidhive.info");
                params.put("password", "password123");

                return params;
            }
        };
*/
        // Request a string response from the provided URL.
        StringRequest stringRequest = new StringRequest(Request.Method.POST, url,
            new Response.Listener<String>() {

                @Override
                public void onResponse(String response) {
                    dialog.dismiss();
                    Toast.makeText(getApplicationContext(), getString(R.string.success_emojify), Toast.LENGTH_LONG).show();
                    byte[] decodedString = Base64.decode(response, Base64.DEFAULT);
                    Bitmap decodedByte = BitmapFactory.decodeByteArray(decodedString, 0, decodedString.length);
                    imageView.setImageBitmap(decodedByte);
                    photoSuccess(decodedByte);
                }
            }, new Response.ErrorListener() {
                @Override
                public void onErrorResponse(VolleyError error) {
                    emojiButton.setEnabled(true);
                    dialog.dismiss();
                    Log.e("Connect Error", "" + error.getMessage());
                    new AlertDialog.Builder(ImageActivity.this)
                            .setTitle("Error")
                            .setMessage("Could not connect to server")
                            .show();
                }
            }){
            @Override
            protected Map<String, String> getParams() throws AuthFailureError {
                //Converting Bitmap to String
                String image = getStringImage(bitmap);

                //Creating parameters
                Map<String,String> params = new Hashtable<String, String>();

                //Adding parameters
                params.put(KEY_IMAGE, image);
                Log.d("image!!!",image);
                //returning parameters
                return params;
            }
        };
        // Add the request to the RequestQueue.
        queue.add(stringRequest);

    }
    private void usePost(String image){
        communicator.post(image);
    }
    public String getStringImage(Bitmap bmp){
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        bmp.compress(Bitmap.CompressFormat.JPEG, 100, baos);
        byte[] imageBytes = baos.toByteArray();
        String encodedImage = Base64.encodeToString(imageBytes, Base64.DEFAULT);
        return encodedImage;
    }
    void photoSuccess(Bitmap bitmap) {
        emojiButton.setVisibility(View.GONE);
        View onSuccessView = findViewById(R.id.on_success);
        onSuccessView.setVisibility(View.VISIBLE);
        Button shareButton = (Button) findViewById(R.id.button_share);
        shareButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent shareIntent = new Intent();
                shareIntent.setAction(Intent.ACTION_SEND);
                shareIntent.putExtra(Intent.EXTRA_STREAM, Uri.parse("file://"+photo_url));
                shareIntent.setType("image/jpeg");
                startActivity(Intent.createChooser(shareIntent, getResources().getText(R.string.send_to)));
            }
        });
    }

    @Override
    public void onWindowFocusChanged(boolean hasFocus) {
        View decorView = getWindow().getDecorView();
        // Hide the status bar.
        int uiOptions = View.SYSTEM_UI_FLAG_FULLSCREEN;
        decorView.setSystemUiVisibility(uiOptions);
        // Remember that you should never show the action bar if the
        // status bar is hidden, so hide that too if necessary.
        ActionBar actionBar = getSupportActionBar();
        if (actionBar != null) {
            actionBar.hide();
        }
    }

    @Override
    protected void onPause() {
        super.onPause();
        if (dialogList.size() > 0)
            dialogList.get(0).dismiss();
        BusProvider.getInstance().unregister(this);
    }
    @Override
    public void onResume(){
        super.onResume();
        BusProvider.getInstance().register(this);
    }
    @Override
    public void onStart() {
        super.onStart();

        // ATTENTION: This was auto-generated to implement the App Indexing API.
        // See https://g.co/AppIndexing/AndroidStudio for more information.
        client.connect();
        Action viewAction = Action.newAction(
                Action.TYPE_VIEW, // TODO: choose an action type.
                "Image Page", // TODO: Define a title for the content shown.
                // TODO: If you have web page content that matches this app activity's content,
                // make sure this auto-generated web page URL is correct.
                // Otherwise, set the URL to null.
                Uri.parse("http://host/path"),
                // TODO: Make sure this auto-generated app URL is correct.
                Uri.parse("android-app://com.emojiverse.emojiverse/http/host/path")
        );
        AppIndex.AppIndexApi.start(client, viewAction);
    }

    @Override
    public void onStop() {
        super.onStop();

        // ATTENTION: This was auto-generated to implement the App Indexing API.
        // See https://g.co/AppIndexing/AndroidStudio for more information.
        Action viewAction = Action.newAction(
                Action.TYPE_VIEW, // TODO: choose an action type.
                "Image Page", // TODO: Define a title for the content shown.
                // TODO: If you have web page content that matches this app activity's content,
                // make sure this auto-generated web page URL is correct.
                // Otherwise, set the URL to null.
                Uri.parse("http://host/path"),
                // TODO: Make sure this auto-generated app URL is correct.
                Uri.parse("android-app://com.emojiverse.emojiverse/http/host/path")
        );
        AppIndex.AppIndexApi.end(client, viewAction);
        client.disconnect();
    }
}
