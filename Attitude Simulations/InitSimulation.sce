// Written by Andrew Donelick
// 29 March 2016

// This code contains the initial conditions and system properties for the 
// balloon attitude simulations. This script is called before the Xcos
// simulation is run.

payloadPosition_IC = 0;
payloadVelocity_IC = 0;

balloonPosition_IC = 0;
balloonVelocity_IC = 0;

J_payload = 1;
J_balloon = 0.5;
ct = 0.1;
kt = 0.2;
