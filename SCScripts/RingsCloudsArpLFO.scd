(
s.waitForBoot {
    var trig, ringsSound, cloudsSound;
    
    // Simulate MouseX and MouseY with control signals
    var xControl = LFNoise1.kr(0.1).range(0, 1);  // Use random noise instead of MouseX
    var yControl = LFNoise1.kr(0.05).range(0.1, 2);  // Random noise instead of MouseY

    // Trigger for MiRings
    trig = Impulse.kr(yControl);  // Using yControl to modulate the speed of the impulse

    // MiRings sound
    ringsSound = MiRings.ar(
        trig: trig,
        pit: [60, 62, 65, 67, 70, 72, 75, 77].choose,  // Picking random pitch for variety
        struct: xControl,  // Modulating structure with xControl
        bright: 0.5,
        damp: 0.5,
        pos: 0.5
    );

    // Clouds processing
    cloudsSound = MiClouds.ar(
        ringsSound,
        pit: 0.5,
        pos: 0.5,
        size: 0.4,
        dens: 0.5,
        tex: 0.5,
        drywet: 0.7
    );

    // Output with panning
    Out.ar(0, Pan2.ar(cloudsSound));
};
)