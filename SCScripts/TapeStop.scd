(

// s.options.sampleRate = 44100;

s.waitForBoot {
    
    // var testVar = 5;

    // Load the buffer
    b = Buffer.read(s, "/home/patch/Repos/Mediapipe-Midi/SCScripts/BellezaLoop.wav"); // remember to free the buffer later.



    // Define the SynthDef after the server is booted
    SynthDef(\help_PlayBuf, { |out = 0, bufnum = 0, rate = 1|
        // Play the buffer with variable rate

        // var bufRate = b.bufRate;

        // var testVar = 5;
        
        // var servRate = s.sampleRate;

        // var rateCorrection = bufRate / servRate;

        // (0.91875 * Lag.kr(rate, 0.2))

        // BufRateScale.kr(bufnum)

        var sound = PlayBuf.ar(2, bufnum, (BufRateScale.kr(bufnum) * Lag.kr(rate, 0.75)), loop: 1.0, doneAction: 0);
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
        // ("Frequency set to: " + rate).postln;
    }, '/control/freq');
};
)