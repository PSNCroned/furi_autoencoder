const Myo = require("myo");
const fs = require("fs");
const dgram = require("dgram");

const client = dgram.createSocket("udp4");

var listeners = function (myo) {
    var res = "";
    var time = Date.now();
    var win = 40;
    var saved = false;
    var i = 0;

    myo.on("connected", function () {
        myo.streamEMG(true);
    });

    myo.on("emg", function (data) {
        client.send(data.toString(), 41234, "localhost", function (err) {
            console.log(data);
        });
    });
};


Myo.on("connected", function () {
    listeners(this);
});

Myo.onError = function () {
    console.log("Error connecting to armband");
};

Myo.connect("com.elliot.myo", require("ws"));
