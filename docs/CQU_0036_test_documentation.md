# CQU_0036: 鬼探头 (Ghost Appearance) Test Case

## Overview
This test case simulates the "鬼探头" (ghost appearance) scenario where a pedestrian suddenly appears at a crosswalk, requiring the ego vehicle to perform emergency braking to avoid collision.

## Scenario Description
The test involves:
- Ego vehicle driving straight through an intersection
- A truck approaching from the opposite direction
- A cyclist crossing from the opposite direction
- A pedestrian suddenly appearing at the crosswalk
- Emergency braking triggered when the truck reaches specific distances from the intersection

## Trigger Conditions
1. **Cyclist Crossing Trigger**: When truck is within 45m of the intersection, initiate cyclist crossing
2. **Emergency Brake Trigger**: When truck is within 20m of the intersection, trigger emergency brake on ego vehicle

## Test Parameters
- **Map**: M499_FTX_suburban.xodr
- **Speed Range**: 20kph to 80kph
- **Truck Distance Range**: 20m to 50m from intersection
- **Crosswalk Length**: Determined by road configuration
- **Cyclist Speed**: 6.5kph
- **Pedestrian Speed**: 5kph

## Expected Behavior
1. Ego vehicle proceeds normally through intersection
2. Truck approaches from opposite direction
3. Cyclist begins crossing when truck is 45m away
4. Emergency brake activated when truck is 20m away
5. All vehicles complete their movements safely

## Execution Script
```bash
# Run the test case
osc2 run CQU_0036.osc

# With specific parameters
osc2 run CQU_0036.osc --speed 40kph --distance 30m
```