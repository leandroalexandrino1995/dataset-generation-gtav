#!/bin/sh

set -e

echo "Copying"

cp -n -r ../../PointCloudsMaterialHash/* ../../PointCloudsMaterialHash_withIntensity/

echo "python"

python3 where_it_stands.py
