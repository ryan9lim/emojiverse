package com.emojiverse.emojiverse;

import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.AsyncTask;

import java.io.IOException;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;

/**
 * Created by Limmy on 10/23/2016.
 */
public class MyAsync extends AsyncTask<String, Void, Bitmap> {

    ImageActivity activity;
    public MyAsync(ImageActivity activity){
        this.activity = activity;
    }

    @Override
    protected Bitmap doInBackground(String... params) {

        try {
            URL url = new URL(params[0]);
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setDoInput(true);
            connection.connect();
            InputStream input = connection.getInputStream();
            Bitmap myBitmap = BitmapFactory.decodeStream(input);
            return myBitmap;
        } catch (IOException e) {
            e.printStackTrace();
            return null;
        }

    }
    protected void onPostExecute(Bitmap bitmap) {
        activity.photoSuccess(bitmap);
    }
}
