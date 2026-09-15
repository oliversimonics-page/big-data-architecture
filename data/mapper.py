#!/usr/bin/env python
import sys
import json

for line in sys.stdin:
    try:
        record = json.loads(line)

        if record["sensor_type"] == "temperature":
            print(line.strip())

    except Exception:
        pass