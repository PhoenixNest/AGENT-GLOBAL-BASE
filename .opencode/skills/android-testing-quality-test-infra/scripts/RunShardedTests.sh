#!/bin/bash
# run-sharded-tests.sh
NUM_SHARDS=4

for shard in $(seq 0 $((NUM_SHARDS - 1))); do
  adb shell am instrument -w \
    -e numShards $NUM_SHARDS \
    -e shardIndex $shard \
    com.example.app.test/androidx.test.runner.AndroidJUnitRunner &
done

wait