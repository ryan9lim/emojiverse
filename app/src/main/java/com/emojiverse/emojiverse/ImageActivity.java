package com.emojiverse.emojiverse;


import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import android.annotation.SuppressLint;
import android.app.ProgressDialog;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Matrix;
import android.media.ExifInterface;
import android.media.Image;
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

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

/**
 * An example full-screen activity that shows and hides the system UI (i.e.
 * status bar and navigation/system bar) with user interaction.
 */
public class ImageActivity extends AppCompatActivity {

    Button emojiButton;
    ImageView imageView;
    List<ProgressDialog> dialogList = new ArrayList<>();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.activity_image);


        imageView = (ImageView) findViewById(R.id.image);
        String photo_url = getIntent().getStringExtra("photo_url");
        Bitmap raw_bitmap = BitmapFactory.decodeFile(photo_url);
        ExifInterface exif = null;
        try {
            exif = new ExifInterface(photo_url);
        } catch (IOException exception){

        }
        int orientation = exif.getAttributeInt(ExifInterface.TAG_ORIENTATION, 1);
        Matrix matrix = new Matrix();
        switch(orientation){
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
                volleyRequest(bitmap);
            }
        });
    }

    void volleyRequest(Bitmap bitmap){
        emojiButton.setEnabled(false);
        final ProgressDialog dialog = new ProgressDialog(ImageActivity.this);
        dialogList.add(dialog);
        dialog.show();
        RequestQueue queue = Volley.newRequestQueue(ImageActivity.this);
        String url ="http://67.134.206.62:8081/";

        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        bitmap.compress(Bitmap.CompressFormat.JPEG, 100, baos); //bm is the bitmap object
        byte[] b = baos.toByteArray();
        String encodedImage = Base64.encodeToString(b, Base64.DEFAULT);
        url+="?img="+encodedImage;
        Log.d("base64_image",encodedImage);
        // Request a string response from the provided URL.
        StringRequest stringRequest = new StringRequest(Request.Method.GET, url,
                new Response.Listener<String>() {

                    @Override
                    public void onResponse(String response) {
                        dialog.dismiss();
                        Toast.makeText(getApplicationContext(),getString(R.string.success_emojify),Toast.LENGTH_LONG).show();
                        byte[] decodedString = Base64.decode(response, Base64.DEFAULT);
                        Bitmap decodedByte = BitmapFactory.decodeByteArray(decodedString, 0, decodedString.length);
                        imageView.setImageBitmap(decodedByte);
                        photoSuccess();
                    }
                }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                emojiButton.setEnabled(true);
                dialog.dismiss();
                Log.e("Connect Error",""+error.getMessage());
                new AlertDialog.Builder(ImageActivity.this)
                        .setTitle("Error")
                        .setMessage("Could not connect to server")
                        .show();
            }
        });
        // Add the request to the RequestQueue.
        queue.add(stringRequest);
    }

    void photoSuccess(){
        emojiButton.setVisibility(View.GONE);
        View onSuccessView = findViewById(R.id.on_success);
        onSuccessView.setVisibility(View.VISIBLE);
    }
    @Override
    public void onWindowFocusChanged (boolean hasFocus){
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
    protected void onPause(){
        super.onPause();
        dialogList.get(0).dismiss();
    }
}
