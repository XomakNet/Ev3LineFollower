# PID-regulator for the line following robot
Innopolis University SIS course home assignment

----------
## Task description

The task was to design PID-controller for EV3 robot with light-sensors to make it following the line as fast as possible, in the same time being stable.

## Code description
There are calibrator and line follower component for the car, equipped with one and two color sensors.

Common code is located in "common" directory. "Data" directory contains:

* Calibration files
* PID-regulator parameters and speed value files

## Work description and explanation
The system is based on ev3dev alternative firmware for EV3 and is developed on Python 3. It was bluetooth connection to the robot, using SSH. Therefore it was possible to remotely change the code and PID-parametres as well as base speed value. In the software, it was implemented a feature of re-reading PID-control parameters from the file during the working cycle. It allowed me to change parameters and see the result immediately.

At the beginning of the work, the car with only one color sensor was constructed, aimed to follow not the line, but the edge of the line (left or right, depending on the constant in the code). During the calibration, it was gathered values from a color detector for terrain area and line area, a mean value was considered as a target value for the robot, so it tried to keep sensor over the line edge.

This system worked, however, I did not succeed in params adjustment for speed greater than 200 (where 960 is the maximum). This can be explained by the fact that edge of the line is a very small area, which could be easily lost during the sharp turn.

After that, it was constructed the car with two color sensors, located over almost over terrain near both sides of the line. It allowed to sufficiently increase stability.

Two principles of error calculation were considered, using two sensors:

* Mean of absolute values from both sensors with the sign, depending on the sign of the value from one selected sensor
* Maximum absolute value from both sensors with the sign, depending on the dominating sensor

Since during the turn one sensor is located over the line (and has large value change) and another is located somewhere over terrain (and has not large value change), the mean value does not represent the real error. That is why it was decided to use the second approach, which turned out to be more suitable for this case.

In both cases (for one sensor and two sensors) it was the same PID-regulator adjustment procedure performed. At first, the proportional coefficient was being adjusted to allow the car to go through turns (especially, sharp ones). Obviously, increasing the proportional coefficient led to overcontrol and the robot started to oscillate near the line. To eliminate this effect, the derivative coefficient was increased. It works for the low-speed system, but some oscillations are still presented in the high-speed final system.

The integral coefficient was set to zero for the high-speed system since it makes the system more unstable without visible positive changes. However, for the low-speed system, it allowed decreasing proportional coefficient without loss of maneuvrability on turns.

Result values are located in corresponding files in the data directory.

They seem to be "the best" for this assignment since they provide the good compromise between system oscillability, stability, and moving speed.

## Video

[YouTube link](https://www.youtube.com/watch?v=5Kl0X8Di-mU)