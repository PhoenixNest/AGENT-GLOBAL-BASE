#!/bin/bash
# aggregate-results.sh — Merge JUnit XML from all platforms

RESULTS_DIR="./test-results"
OUTPUT_DIR="./test-results/aggregated"

mkdir -p $OUTPUT_DIR

# Merge Android results (Firebase + AWS Device Farm)
find $RESULTS_DIR -name "*android*.xml" -exec cat {} + > $OUTPUT_DIR/android-merged.xml

# Merge iOS results
find $RESULTS_DIR -name "*ios*.xml" -exec cat {} + > $OUTPUT_DIR/ios-merged.xml

# Generate summary report
REPORT_FILE="$OUTPUT_DIR/test-summary-$(date +%Y%m%d).md"

cat > $REPORT_FILE << EOF
# Test Results Summary — $(date +%Y-%m-%d)

## Android
| Metric | Value |
|--------|-------|
| Total Tests | $(grep -c 'testcase' $OUTPUT_DIR/android-merged.xml) |
| Passed | $(grep -c 'testcase' $OUTPUT_DIR/android-merged.xml | xargs -I{} echo {} | awk '{print $1 - failures}') |
| Failed | $(grep -c 'failure' $OUTPUT_DIR/android-merged.xml || echo 0) |
| Skipped | $(grep -c 'skipped' $OUTPUT_DIR/android-merged.xml || echo 0) |
| Duration | $(grep 'time=' $OUTPUT_DIR/android-merged.xml | awk -F'"' '{sum+=$2} END {print sum "s"}') |

## iOS
| Metric | Value |
|--------|-------|
| Total Tests | $(grep -c 'testcase' $OUTPUT_DIR/ios-merged.xml) |
| Passed | $(grep -c 'testcase' $OUTPUT_DIR/ios-merged.xml | xargs -I{} echo {} | awk '{print $1 - failures}') |
| Failed | $(grep -c 'failure' $OUTPUT_DIR/ios-merged.xml || echo 0) |
| Skipped | $(grep -c 'skipped' $OUTPUT_DIR/ios-merged.xml || echo 0) |
| Duration | $(grep 'time=' $OUTPUT_DIR/ios-merged.xml | awk -F'"' '{sum+=$2} END {print sum "s"}') |

## Failed Tests
$(grep -B2 'failure' $OUTPUT_DIR/android-merged.xml | grep 'name=' | sed 's/.*name="\([^"]*\)".*/- Android: \1/')
$(grep -B2 'failure' $OUTPUT_DIR/ios-merged.xml | grep 'name=' | sed 's/.*name="\([^"]*\)".*/- iOS: \1/')
EOF

echo "Report generated: $REPORT_FILE"