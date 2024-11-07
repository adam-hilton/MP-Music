(

s.waitForBoot {

//// Delcare initial vars

var chordIndex = 0;

var chords = [
        [48, 52, 55, 59], // Cmaj7
        [53, 57, 60, 64], // Fmaj7
        [57, 59, 60, 55], // ABCF
        [60, 62, 64, 69]  // CDEA
    ];

var currentChord = chords[0];

var invertChord = { |chord, inversion|
    // Move the lowest note(s) up by 12 semitones per inversion
    var newChord = chord.collect { |note, i|
        (i < inversion).if { note + 12 } { note };
    };
    newChord;  // Return the inverted chord
};

//// Rings/Clouds SynthDef

b = Buffer.read(s, "/home/patch/Repos/Mediapipe-Midi/SCScripts/TCA-RingsSoundBed.mp3");

// Define buffer playback synth

SynthDef(\help_PlayBuf, { |out = 0, bufnum = 0, rate = 1|
        var sound = PlayBuf.ar(2, bufnum, (BufRateScale.kr(bufnum)), loop: 1.0, doneAction: 0);
        Out.ar(out, sound * 0.5);
    }).add;

// Define RingsClouds synth

SynthDef(\testRingsArp, {
    arg freq = 60, bright = 0.01, chord = #[60, 62, 63, 64], trigRate = 0.75, verb = 0.5, drywet = 0.1, damp = 0.7, dens = 0.4;
    
    // Chord selection logic should be based on control values, not UGens
    var trig, ringsSound, cloudsSound, freqIndex;

    // Trigger impulses at the rate defined by 'trigRate'
    trig = Impulse.kr(trigRate);

    // Cycle through the notes in the selected chord
	freqIndex = Stepper.kr(trig: trig, min: 0, max: chord.size - 1);  // Steps through each note in the chord
	freqIndex.poll;
    freq = Select.kr(freqIndex, chord); // Selects the note index from passed chord
    freq.poll;

    // Generate sound using MiRings
    ringsSound = MiRings.ar(
        trig: trig,
        pit: freq,
        struct: 0.0,
        bright: bright,
        damp: damp,
        pos: 0.4,
        model: 2,
        poly: 4
    );

    cloudsSound = MiClouds.ar(
			ringsSound * 0.8,    // Signal input (MiRings output)
			pos: 0.3,
			size: 0.2,
			dens: dens,
			spread: 1,
            tex: 0.8,
			rvb: verb,
			drywet: drywet
		);

    // Output the sound
    Out.ar(0, Limiter.ar(Pan2.ar(cloudsSound, 0) * 3), 0.8);
}).add;


//// Wait for Server and instantiate synth

s.sync;

~buff = Synth(\help_PlayBuf);

~synth = Synth(\testRingsArp, [\chord, currentChord, \verb, 0.1, \bright, 0.1, \damp, 0.7, \drywet, 0.1]);


//// OSC Defs

/// Music Hand

// OSC control for changing the currently selected chord
OSCdef(\chordSet, { |msg|
    chordIndex = msg[1].linlin(0, 1000, 0, 4).asInteger;  // Clip to avoid out-of-range errors
    currentChord = chords[chordIndex];
}, '/control/XRightIndex');

// OSC control for setting inversion and sending chord

OSCdef(\chordInvert, { |msg|
    var invertNum = msg[1].linlin(0, 1000, 3, 0).asInteger;
    var chordInversion = invertChord.(currentChord, invertNum);
    ~synth.set(\chord, chordInversion);  
}, '/control/YRightIndex');

// OSC control for changing arp speed

OSCdef(\trigRateControl, { |msg|
    var newRate = msg[1].linexp(0, 1000, 8, 0.5);
    ~synth.set(\trigRate, newRate);
}, '/control/YRightIndex');


/// Timbre Hand


// OSC control for changing reverb mix

OSCdef(\verbControl, { |msg|
    var verbValue = msg[1].linlin(0, 100, 0.9, 0.01);
    ~synth.set(\verb, verbValue);
}, '/control/YLeftIndex');

// OSC control for dry/wet

OSCdef(\wetControl, { |msg|
    var wetValue = msg[1].linlin(0, 1000, 0.7, 0.05);
    ~synth.set(\drywet, wetValue);
}, '/control/YLeftIndex');

// OSC control for changing brightness

OSCdef(\brightControl, { |msg|
    var brightValue = msg[1].linexp(0, 1000, 0.7, 0.01);
    ~synth.set(\bright, brightValue);
}, '/control/YLeftIndex');


// OSC control for changing damping

OSCdef(\dampControl, { |msg|
    var dampValue = msg[1].linlin(0, 1000, 0.1, 0.85);
    ~synth.set(\damp, dampValue);
}, '/control/XLeftIndex');

// OSC control for changing density

OSCdef(\densControl, { |msg|
    var densValue = msg[1].linlin(0, 1000, 0.4, 0.8);
    ~synth.set(\dens, densValue);
}, '/control/YLeftIndex');

}
)