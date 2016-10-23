package com.emojiverse.emojiverse;

import retrofit.Callback;
import retrofit.http.Field;
import retrofit.http.FormUrlEncoded;
import retrofit.http.GET;
import retrofit.http.POST;
import retrofit.http.Query;

/**
 * Created by Limmy on 10/22/2016.
 */
public interface Interface {

    //This method is used for "POST"
    @FormUrlEncoded
    @POST("/")
    void postData(@Field("method") String method,
                  @Field("image") String image,
                  Callback<ServerResponse> serverResponseCallback);

    @GET("/api.php")
    void getData(@Query("method") String method,
                 @Query("username") String username,
                 @Query("password") String password,
                 Callback<ServerResponse> serverResponseCallback);
}
