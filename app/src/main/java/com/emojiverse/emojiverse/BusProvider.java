package com.emojiverse.emojiverse;

import com.squareup.otto.Bus;

/**
 * Created by Limmy on 10/22/2016.
 */


public class BusProvider {

    private static final Bus BUS = new Bus();

    public static Bus getInstance(){
        return BUS;
    }

    public BusProvider(){}
}


