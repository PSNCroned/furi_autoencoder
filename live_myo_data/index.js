const Myo = require("myo");
const fs = require("fs");
const dgram = require("dgram");

const client = dgram.createSocket("udp4");

var listeners = function (myo) {
    const win = 40;
    const mode = "send";
    const filename = "fist.csv";
    const timeOnStart = Date.now();
    const duration = 100;
    const dataLimit = 100;

    var res = "";
    var saved = false;
    var i = 0;

    myo.on("connected", function () {
        myo.streamEMG(true);
    });

    myo.on("emg", function (data) {
        data = data.toString();

        switch (mode) {
            case "save":
                if (!saved) {
                    res += (data + "\n");
                    i++;
                    console.log(i);

                    if ((Date.now() - timeOnStart) / 1000 > duration || i >= dataLimit) {
                        saved = true;
                        fs.writeFile("./data/" + filename, res, (err) => {
                            if (err)
                                console.log("Error saving data: " + err);
                            else
                                console.log("Data saved");
                        });
                    }
                }
                break;
            case "send":
                client.send(data.toString(), 41234, "localhost", function (err) {
                    console.log(data);
                });
                break;
        }
    });
};


Myo.on("connected", function () {
    listeners(this);
});

Myo.onError = function () {
    console.log("Error connecting to armband");
};

Myo.connect("com.elliot.myo", require("ws"));
