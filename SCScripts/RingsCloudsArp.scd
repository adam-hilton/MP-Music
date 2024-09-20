(
// s.quit;  // Ensure the server is fully stopped before we try booting
s.waitForBoot {
    // Define the sound function, which generates the arpeggiated MiRings and processes it with MiClouds
    var sound = {
        var notes, numNotes, trig, freq, ringsSound, cloudsSound, brightness, yscale, xscale;

        // Define a list of MIDI notes for the arpeggio (C major scale)
		notes = [0, 2, 5, 7, 11, 16, 19] + 48;  // MIDI note numbers

        // MouseX controls how many notes are arpeggiated (between 1 and 8)
        numNotes = MouseX.kr(1, 8).round(1);  // Rounded to an integer value

        // MouseY controls the arpeggiation speed (adjust the range as needed)
        trig = Impulse.kr(MouseY.kr(0.5, 10));  // Trigger based on the speed from MouseY

        // Choose which note to play based on the arpeggiation sequence
        freq = Select.kr((Stepper.kr(trig, 0, 0, numNotes - 1) % numNotes), notes);

		// Store the MouseY range as something between 0 - 0.9

		yscale = MouseY.kr(0.01, 0.9);

		// Store the MouseX range as something between 0 - 0.9

		xscale = MouseX.kr(0.01, 0.9);

        // Generate sound using MiRings with internal excitation
        ringsSound = MiRings.ar(
			trig: trig,  // Use the arpeggiation trigger
			in: DC.ar(0),  // Use the internal exciter model
			pit: freq,  // Pass the arpeggiated MIDI note
			struct: 0.55,  // Structure of the resonator
			bright: yscale - 0.4,  // Brightness of the resonator
			damp: 0.7,  // Damping for longer resonance
			pos: 0.4,  // Position within the resonator
			intern_exciter: 1,  // Use internal exciter
			poly: 4,  // Polyphony for richer sound
			model: 1
        );

        // Low-pass filter and MiClouds
        brightness = 8000;
        ringsSound = RLPF.ar(ringsSound, brightness, 0.2);
        cloudsSound = MiClouds.ar(ringsSound, 0, 0.5, 0.4, 1.0, 0.5, 0.5, 0.5);
		cloudsSound = MiClouds.ar(
			ringsSound * 0.5,    // Signal input (MiRings output)
			freeze: 0,             // Freeze off
			pos: 0.1,           // Fixed grain position
			size: 0.4,           // Fixed grain size
			pit: 1.0,           // Fixed pitch (no pitch shift)
			dens: 0.7,           // Fixed grain density
			tex: 0.0,           // Fixed texture
			spread: 0.9,
			rvb: yscale,
			drywet: 0.7,            // Fixed dry/wet mix
			mode: 2,
			lofi: 1
		);

        // Limit the output to prevent runaway values
		// cloudsSound = Limiter.ar(cloudsSound, 0.9, 0.01);

        // Output the processed sound
        Pan2.ar(cloudsSound, 0) * 0.8
    };

    // Play the sound function
    sound.play;
};
)