# Roundabout Intersection Test Scenario

## Description
This test scenario evaluates vehicle behavior at a roundabout intersection with multiple traffic participants including a blocking vehicle and an obstacle vehicle.

## Scenario Details
- **Road Scenario**: Roundabout intersection
- **Traffic Participants**: 
  - Main vehicle (blue car) - traveling straight through
  - Other traffic participants (red car, yellow car) - turning directions
  - Blocking vehicle (adversary) - blocking the path
  - Obstacle vehicle - slow-moving in front
- **Initial Position**: 
  - Ego vehicle in inner lane
  - Blocking vehicle in outer lane alongside ego
  - Obstacle vehicle 27 meters ahead in inner lane
- **Movement**: 
  - Ego vehicle goes straight through the roundabout
  - Red vehicle turns right
  - Yellow vehicle turns left
  - Blocking vehicle follows maintaining relative speed
  - Obstacle vehicle moves slowly ahead

## Trigger Condition
When ego vehicle approaches the obstacle vehicle, the blocking vehicle begins to follow maintaining relative speed.

## Test Objective
Test vehicle's ability to navigate roundabout intersections with blocking and obstacle conditions.