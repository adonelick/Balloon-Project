# Balloon-Project

Created by Andrew Donelick

## Summary

This repository contains code for the ground station operation, simulation,
and analysis of high altitude sounding balloons.

The ground station is designed to allow for two-way communication with a 
high altitude balloon payload. Users can receive status updates from onboard
instruments, send commands to the payload, and track the payload. The 
ground station is meant to be interfaced with an Arduino/2-meter radio.

The simulations are used to understand the dynamics of the payload's movement
throughout flight. The purpose in gaining this understanding is to develop
attitude control solutions for the payload to enable accurate pointing of
cameras or other instruments at specific targets. 

The analysis code is used to post-process data recovered from the payload's
instruments, and report useful information, such as ascent rate, flight 
path, attitude history, etc. 

## Dependencies

LabVIEW 2013 or later
Scilab 5.5.2 or later