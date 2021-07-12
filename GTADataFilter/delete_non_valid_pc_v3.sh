#!/bin/sh

set -e

#echo "Cópia Only1PCperFrameAnd1Capture"
#cp -r ../../Only1PCperFrameAnd1Capture/ ../../BonsDados-backup
# echo "Only1PCperFrameAnd1Capture"
# python3 ValidPC_v3.py --rd Only1PCperFrameAnd1Capture

# echo "Cópia Only1PCperFrameAnd1Capture_vPAI"
# cp -r ../../Only1PCperFrameAnd1Capture_vPAI/ ../../BonsDados-backup
# echo "Only1PCperFrameAnd1Capture_vPAI"
# python3 ValidPC_v3.py --rd Only1PCperFrameAnd1Capture_vPAI

echo "PegaPumba"
python3 ValidPC_v3.py --rd PegaPumba

echo "Numbering"
python3 numbering.py

python3 Main.py --gtaSamplesPath "../../BonsDados-backup/AllPointClouds/" --kittiOutputPath "../../BonsDados-backup/GTAtoKITTI/kitti" --targetArchitecure "PointPillars"

