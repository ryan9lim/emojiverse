package com.emojiverse.emojiverse;

/**
 * Created by Limmy on 10/22/2016.
 */

public class ServerEvent {
    private ServerResponse serverResponse;

    public ServerEvent(ServerResponse serverResponse) {
        this.serverResponse = serverResponse;
    }

    public ServerResponse getServerResponse() {
        return serverResponse;
    }

    public void setServerResponse(ServerResponse serverResponse) {
        this.serverResponse = serverResponse;
    }
}


