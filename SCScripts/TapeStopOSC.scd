(
s.waitForBoot {
    // Load the buffer
    b = Buffer.read(s, "BrownBreak.wav"); // remember to free the buffer later.

    // Define the SynthDef after the server is booted
    SynthDef(\help_PlayBuf, { |out = 0, bufnum = 0, rate = 1|
        // Play the buffer with variable rate
        var sound = PlayBuf.ar(2, bufnum, rate, loop: 1.0, doneAction: 0);
        Out.ar(out, sound);
    }).add;

    // Wait for the SynthDef to be added before creating the Synth
    s.sync;

    // Instantiate the Synth as a global environment variable
    ~synth = Synth(\help_PlayBuf, [\bufnum, b]);

    // Define the OSC function to control the rate parameter
    OSCdef(\freqControl, { |msg|
        var rate = msg[1];  // The value from Python
        ~synth.set(\rate, rate);  // Access the synth via the global environment variable
        ("Frequency set to: " + rate).postln;
    }, '/control/freq');
};
)