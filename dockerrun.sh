#!/usr/bin/env bash
docker run \
--mount type=bind,source="$(pwd)"/data,target=/remotedata \
--name fixed2csv-job fixed2csv:latest \
python process_fixed.py \
-s /remotedata/specfile.json -f /remotedata/fixedfile.txt -o /remotedata/csvfile

