#!/bin/sh

set -e

# echo "PointClouds"
# cp -r /media/joao/Elements/PointClouds /media/joao/Elements/Removed/PointClouds
# echo "Done copying"
# python3 ValidPC.py --rd PointClouds

# echo "PointClouds2ndSession"
# cp -r /media/joao/Elements/PointClouds2ndSession /media/joao/Elements/Removed/PointClouds2ndSession
# echo "Done copying"
# python3 ValidPC.py --rd PointClouds2ndSession

# echo "PointCloudsASerio"
# cp -r /media/joao/Elements/PointCloudsASerio /media/joao/Elements/Removed/PointCloudsASerio
# echo "Done copying"
# python3 ValidPC.py --rd PointCloudsASerio

# echo "PointClouds_Carapas_v1"
# cp -r /media/joao/Elements/PointClouds_Carapas_v1 /media/joao/Elements/Removed/PointClouds_Carapas_v1
# echo "Done copying"
# python3 ValidPC.py --rd PointClouds_Carapas_v1

# echo "PointCloudsMesmoASerio"
# cp -r /media/joao/Elements/PointCloudsMesmoASerio /media/joao/Elements/Removed/PointCloudsMesmoASerio
# echo "Done copying"
# python3 ValidPC.py --rd PointCloudsMesmoASerio

# echo "PointCloudsMesmoASerio_vCARAPAS"
# cp -r /media/joao/Elements/PointCloudsMesmoASerio_vCARAPAS /media/joao/Elements/Removed/PointCloudsMesmoASerio_vCARAPAS
# echo "Done copying"
# python3 ValidPC.py --rd PointCloudsMesmoASerio_vCARAPAS

# echo "PointCloudsMesmoASerio_vPAI"
# cp -r /media/joao/Elements/PointCloudsMesmoASerio_vPAI /media/joao/Elements/Removed/PointCloudsMesmoASerio_vPAI
# echo "Done copying"
# python3 ValidPC.py --rd PointCloudsMesmoASerio_vPAI

# echo "PointCloudsMesmoASerio_vPAI_NumInv"
# cp -r /media/joao/Elements/PointCloudsMesmoASerio_vPAI_NumInv /media/joao/Elements/Removed/PointCloudsMesmoASerio_vPAI_NumInv
# echo "Done copying"
# python3 ValidPC.py --rd PointCloudsMesmoASerio_vPAI_NumInv --inv 1

python3 ValidPC.py --rd OQueGostoMesmoEDePCs_vREALISTA --inv 1

python3 ValidPC.py --rd OQueGostoMesmoEDePCs_vREALISTA_INV --inv 1