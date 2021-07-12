#!/bin/sh

set -e

#echo "Cópia PointCloudsMaterialHash"
#cp -r ../../PointCloudsMaterialHash/ ../../BonsDadosComHashes-backup
#echo "PointCloudsMaterialHash"
#python3 ValidPC_v3.py --rd PointCloudsMaterialHash

#echo "Cópia PointCloudsMaterialHash_vPAI"
#cp -r ../../PointCloudsMaterialHash_vPAI/ ../../BonsDadosComHashes-backup
#echo "PointCloudsMaterialHash_vPAI"
#python3 ValidPC_v3.py --rd PointCloudsMaterialHash_vPAI

echo "Numbering"
python3 numbering.py

#python3 Main.py --gtaSamplesPath "../../BonsDados-backup/AllPointClouds/" --kittiOutputPath "../../BonsDados-backup/GTAtoKITTI/kitti" --targetArchitecure "PointPillars"
