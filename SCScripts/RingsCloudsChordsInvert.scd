///// modify to make sure we're either: a) not just passing the index but the chord itself, which may not be simple to do, sending an array in as an argument
/// or b) put the function inside of the synthdef, which the synthdef will prob not like bc it evaluates the function once.
//// we need to 'set' an array, I think


(

s.waitForBoot {

var invertChord = { |chord, inversion|
    // Move the lowest note(s) up by 12 semitones per inversion
    var newChord = chord.collect { |note, i|
        (i < inversion).if { note + 12 } { note };
    };
    newChord;  // Return the inverted chord
};

var chords = [
        [60, 64, 67],  // C major
        [62, 65, 69],  // D minor
        [65, 69, 72],  // F major
        [69, 72, 76]   // A minor
    ];

var currentChord = chords[0];  // Start with the first chord
var currentInversion = 0;      // Start with root inversion

SynthDef(\testRingsArp, {
    arg freq = 60, bright = 0.01, chord = 0, trigRate = 4, verb = 0.5, damp = 0.7;
    
    // Chord selection logic should be based on control values, not UGens
    var trig, ringsSound, cloudsSound, currentChord, freqIndex, currentInversion;

    // Define a set of chords (arrays of MIDI notes)
    // chords = [
    //     [60, 64, 67],  // C major
    //     [62, 65, 69],  // D minor
    //     [65, 69, 72],  // F major
    //     [60, 64, 69]   // A minor
    // ];

    // Ensure that 'chord' is used as an integer index to access the 'chords' array
	currentChord = Select.kr(chord, chords);  // Use modulo to avoid out-of-range errors
    currentInversion = 0;

    // Trigger impulses at the rate defined by 'trigRate'
    trig = Impulse.kr(trigRate); // set to 4 by default via arg declaration

    // Cycle through the notes in the selected chord
		freqIndex = Stepper.kr(trig, 0, 0, 2);  // Steps through each note in the chord
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
			drywet: 0.0,            // Fixed dry/wet mix -- add in 2nd hand control?
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

// OSC control for chord inversion

OSCdef(\inversionChange, { |msg|
    var chord;  // Declare the variable here
    // Get the inversion from the OSC message
    currentInversion = msg[1].linlin(0, 1000, 3, 0).floor.asInteger;  // Scale to 0-2
    chord = invertChord.([1, 2, 3, 4], 1);
    ("New chord inversion: " + chord).postln;  // Post the new inverted chord
}, '/control/inversion');  // Listening for messages on '/inversion'

// OSC control for chord change
    OSCdef(\chordChange, { |msg|
        var chord;  // Declare the variable here
        // Get the chord index from the OSC message
        var chordIndex = msg[1].linlin(-100, 100, 0, chords.size - 1).floor.asInteger;
        currentChord = chords[chordIndex];  // Set the current chord based on the OSC message
        chord = invertChord.(currentChord, currentInversion);  // Apply the current inversion to the new chord
        ("New chord selection: " + chord).postln;  // Post the new selected and inverted chord
    }, '/control/chord');  // Listening for messages on '/chord'
};

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