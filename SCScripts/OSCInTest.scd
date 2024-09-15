(
SynthDef(\laggedSynth, { |freq = 440|
    var laggedFreq = Lag2.kr(freq, 0.5);  // Apply lag of 0.5 seconds
    var sig = SinOsc.ar(laggedFreq) * 0.1;
    Out.ar(0, sig);
}).add;

s.waitForBoot {
    var synth = Synth(\laggedSynth);

    OSCdef(\freqControl, { |msg|
        var freq = msg[1];
        synth.set(\freq, freq);
        "Frequency set to (with lag): %\n".format(freq).postln;
    }, '/control/freq');
}
)