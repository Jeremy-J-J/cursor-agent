#!/bin/bash

# CQU_0036 Test Execution Script
# This script runs the 鬼探头 (ghost appearance) test case

echo "Starting CQU_0036: 鬼探头 (Ghost Appearance) Test"

# Set up environment
export TEST_NAME="CQU_0036"
export TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Check if osc2 is available
if ! command -v osc2 &> /dev/null; then
    echo "Error: osc2 command not found. Please install osc2 tool."
    exit 1
fi

# Run the test with different speed configurations
echo "Running test with various speed configurations..."

# Test with low speed
echo "Running test at 20kph..."
osc2 run "$TEST_DIR/CQU_0036.osc" --speed 20kph --output-dir "$TEST_DIR/results/low_speed"

# Test with medium speed  
echo "Running test at 40kph..."
osc2 run "$TEST_DIR/CQU_0036.osc" --speed 40kph --output-dir "$TEST_DIR/results/medium_speed"

# Test with high speed
echo "Running test at 60kph..."
osc2 run "$TEST_DIR/CQU_0036.osc" --speed 60kph --output-dir "$TEST_DIR/results/high_speed"

# Test with maximum speed
echo "Running test at 80kph..."
osc2 run "$TEST_DIR/CQU_0036.osc" --speed 80kph --output-dir "$TEST_DIR/results/max_speed"

echo "Test execution completed."
echo "Results are stored in $TEST_DIR/results/"

# Generate summary report
echo "Generating test summary..."
echo "CQU_0036 Test Summary:" > "$TEST_DIR/results/test_summary.txt"
echo "=====================" >> "$TEST_DIR/results/test_summary.txt"
echo "Scenario: 鬼探头 (Ghost Appearance)" >> "$TEST_DIR/results/test_summary.txt"
echo "Description: Emergency braking triggered by truck approaching crosswalk" >> "$TEST_DIR/results/test_summary.txt"
echo "Trigger Conditions:" >> "$TEST_DIR/results/test_summary.txt"
echo "  - Cyclist crossing when truck < 45m from intersection" >> "$TEST_DIR/results/test_summary.txt"
echo "  - Emergency brake when truck < 20m from intersection" >> "$TEST_DIR/results/test_summary.txt"
echo "Speed Range: 20kph - 80kph" >> "$TEST_DIR/results/test_summary.txt"