(

s.waitForBoot {

SynthDef(\testRingsArp, {
    arg freq = 60, bright = 0.01, chord = 0, trigRate = 4, verb = 0.5, damp = 0.7;
    
    // Chord selection logic should be based on control values, not UGens
    var trig, ringsSound, cloudsSound, chords, currentChord, freqIndex;

    // Define a set of chords (arrays of MIDI notes)
    chords = [
        [60, 64, 67, 72], // C major chord
        [62, 65, 69, 74], // D minor chord
        [64, 67, 71, 76], // E minor chord
        [65, 69, 72, 77]  // F major chord
    ];

    // Ensure that 'chord' is used as an integer index to access the 'chords' array
		currentChord = Select.kr(chord, chords);  // Use modulo to avoid out-of-range errors

    // Trigger impulses at the rate defined by 'trigRate'
    trig = Impulse.kr(trigRate); // set to 4 by default via arg declaration

    // Cycle through the notes in the selected chord
		freqIndex = Stepper.kr(trig, 0, 0, 4);  // Steps through each note in the chord
		freq = Select.kr(freqIndex, currentChord);  // Convert MIDI note to frequency

    // Generate sound using MiRings
    ringsSound = MiRings.ar(
        trig: trig,
        pit: freq,  // Pass arpeggiated note
        struct: 0.0,
        bright: bright,
        damp: damp,
        pos: 0.1,
        model: 2
    );

    cloudsSound = MiClouds.ar(
			ringsSound * 0.8,    // Signal input (MiRings output)
			// freeze: 0,             // Freeze off by default -- add in a freeze option for hand pose?
			pos: 0.1,           // Fixed grain position -- add in 2nd hand control?
			size: 0.5,           // Fixed grain size -- add in 2nd hand control?
			dens: 1.0,           // Fixed grain density
			spread: 0.9,
			rvb: verb,
			drywet: 0.3,            // Fixed dry/wet mix -- add in 2nd hand control?
		);

    // Output the sound
    Out.ar(0, Pan2.ar(cloudsSound, 0));
}).add;

s.sync;

~synth = Synth(\testRingsArp, [\chord, 0, \verb, 0.1, \bright, 0.1, \damp, 0.7]);
"synth initialized".postln;

// OSC control for changing chord makeup
OSCdef(\chordControl, { |msg|
    var chordValue = msg[1].linlin(0, 1000, 0, 5).asInteger;  // Clip to avoid out-of-range errors
    ~synth.set(\chord, chordValue);  // Set 'chord' control value
    ("Chord index set to: " + chordValue).postln; // log
}, '/control/chord');

// OSC control for changing reverb mix

OSCdef(\verbControl, { |msg|
    var verbValue = msg[1].linlin(0, 1000, 0.99, 0.01);
    ~synth.set(\verb, verbValue);  // Set 'chord' control value
}, '/control/verb');

// OSC control for changing brightness

OSCdef(\brightControl, { |msg|
    var brightValue = msg[1].linexp(0, 1000, 0.8, 0.01);
    ~synth.set(\bright, brightValue);  // Set 'chord' control value
}, '/control/bright');

// OSC control for changing arp speed

// OSC control for changing damping

OSCdef(\dampControl, { |msg|
    var dampValue = msg[1].linlin(0, 1000, 0.05, 0.99);
    ~synth.set(\damp, dampValue);
}, '/control/damp');

// OSC control for changing 

}
)