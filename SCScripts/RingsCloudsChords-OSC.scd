(
s.waitForBoot {

SynthDef(\testRingsArp, {
    arg freq = 60, bright = 0.5, chord = 0, trigRate = 4;
    
    // Chord selection logic should be based on control values, not UGens
    var trig, ringsSound, chords, currentChord, freqIndex;

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
        struct: 0.55,
        bright: bright,
        damp: 0.7,
        pos: 0.4
    );

    // Output the sound
    Out.ar(0, Pan2.ar(ringsSound, 0));
}).add;

s.sync;

~synth = Synth(\testRingsArp, [\chord, 0]);
"synth initialized".postln;

// OSC control
OSCdef(\chordControl, { |msg|
    var chordValue = msg[1].linlin(-100, 100, 0, 3).asInteger;  // Clip to avoid out-of-range errors
    ~synth.set(\chord, chordValue);  // Set 'chord' control value
    ("Chord index set to: " + chordValue).postln;
}, '/control/chord');
}
)