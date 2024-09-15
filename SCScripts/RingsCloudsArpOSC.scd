(
s.waitForBoot {
    // Define the SynthDef, which generates the arpeggiated MiRings and processes it with MiClouds
    SynthDef(\testRings, { |numNotes = 4, trigSpeed = 1, brightness = 0.5|
        var trig, freq, ringsSound, cloudsSound, notes;

        // Define a list of MIDI notes for the arpeggio (C major scale)
        notes = [0, 2, 5, 7, 11, 16, 21] + 48;  // MIDI note numbers

        // Generate the trigger based on the arpeggiation speed
        trig = Impulse.kr(trigSpeed);  // Trigger based on the OSC-controlled speed

        // Choose which note to play based on the arpeggiation sequence
        freq = Select.kr(Stepper.kr(trig, 0, 0, numNotes - 1), notes);

        // Generate sound using MiRings with internal excitation
        ringsSound = MiRings.ar(
            trig: trig,  // Use the arpeggiation trigger
            in: DC.ar(0),  // Use the internal exciter model
            pit: freq,  // Pass the arpeggiated MIDI note
            struct: 0.55,  // Structure of the resonator
            bright: brightness,  // OSC-controlled brightness of the resonator
            damp: 0.7,  // Damping for longer resonance
            pos: 0.4,  // Position within the resonator
            intern_exciter: 1,  // Use internal exciter
            poly: 4,  // Polyphony for richer sound
            model: 1
        );

        // Process sound with MiClouds
        cloudsSound = MiClouds.ar(
            ringsSound,    // Signal input (MiRings output)
            freeze: 0,             // Freeze off
            pos: 0.1,           // Fixed grain position
            size: 0.4,           // Fixed grain size
            pit: 1.0,           // Fixed pitch (no pitch shift)
            dens: 0.7,           // Fixed grain density
            tex: 0.9,           // Fixed texture
            rvb: brightness,   // OSC-controlled reverb amount
            drywet: brightness - 0.1,  // OSC-controlled dry/wet mix
            mode: 2,
            lofi: 1
        );

        // Limit the output to prevent runaway values
        cloudsSound = Limiter.ar(cloudsSound, 0.9, 0.01);

        // Output the processed sound
        Out.ar(0, Pan2.ar(cloudsSound, 0) * 0.5);
    }).add;

    // Create the synth
    s.sync;
    ~synth = Synth(\testRings);

    // Set up OSC controls for numNotes, trigSpeed, and brightness, with logging
    OSCdef(\numNotesControl, { |msg|
        msg.postln;  // Post the entire incoming message to the post window for debugging
        ("Received numNotes message: " + msg).postln;
        ~synth.set(\numNotes, msg[1].clip(1, 8));  // Limit numNotes between 1 and 8
        ("NumNotes set to: " + msg[1]).postln;
    }, '/control/numNotes');

    OSCdef(\trigSpeedControl, { |msg|
        msg.postln;  // Post the entire incoming message to the post window for debugging
        ("Received trigSpeed message: " + msg).postln;
        ~synth.set(\trigSpeed, msg[1].clip(0.5, 10));  // Limit trigSpeed between 0.5 and 10 Hz
        ("TrigSpeed set to: " + msg[1]).postln;
    }, '/control/trigSpeed');

    OSCdef(\brightnessControl, { |msg|
        msg.postln;  // Post the entire incoming message to the post window for debugging
        ("Received brightness message: " + msg).postln;
        ~synth.set(\brightness, msg[1].clip(0.1, 1.0));  // Limit brightness between 0.1 and 1.0
        ("Brightness set to: " + msg[1]).postln;
    }, '/control/brightness');

    "OSC controls set up!".postln;
};
)