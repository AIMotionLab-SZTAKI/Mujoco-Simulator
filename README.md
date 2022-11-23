# 3D model of the test environment in the building

## Purpose
Development of a simple display and model generator that can be used to add buildings and objects to the 3D scene. Currently the xml generator supports the following objects:
  * Drones
  * Hospital
  * Post office
  * Sztaki landing zone
  * Poles
  * Landing zones
  * Airport
  * Parking lot

## Installation
1. Create and activate a virtual environment

2. Prerequisite for motioncapture (haven't been able to get it to work on windows):
```
sudo apt install libboost-system-dev libboost-thread-dev libeigen3-dev ninja-build
```
3.
```
$ pip install -e .
```
4. On Windows
```
pip install windows-curses
```
5.
```
$ python build_scene.py
```

## Usage

To add a building:
  * Press 'b'
  * In the pop-up window select the bulding with the dropdown list.
  * Specify the position and the orientation (as quaternion). Default quaternion is 1 0 0 0.
  * Click ok, or hit enter.

To add drones:
  * Press 'd'
  * The drones will be added at hard-coded positions, because they will be updated anyway, once data streaming starts from Optitrack.

To name drones:
  * Press 'n'
  * In the pop-up window enter the name of the drones that are 'ticked' in Motive
  * Click ok, or hit enter

To connect to Motive:
  * Press 'c'

To start and stop video recording:
  * Press 'r'
  * The location of the saved video will be printed to the terminal
