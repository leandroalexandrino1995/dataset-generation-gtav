#!/bin/sh

set -e

# echo "PointClouds"
# python3 ValidPC_v2.py --rd PointClouds

# echo "PointClouds2ndSession"
# python3 ValidPC_v2.py --rd PointClouds2ndSession

# echo "PointCloudsASerio"
# python3 ValidPC_v2.py --rd PointCloudsASerio

# # echo "PointClouds_Carapas_v1"
# # python3 ValidPC_v2.py --rd PointClouds_Carapas_v1

# echo "PointCloudsMesmoASerio"
# python3 ValidPC_v2.py --rd PointCloudsMesmoASerio

# echo "PointCloudsMesmoASerio_vCARAPAS"
# python3 ValidPC_v2.py --rd PointCloudsMesmoASerio_vCARAPAS

# echo "PointCloudsMesmoASerio_vPAI"
# python3 ValidPC_v2.py --rd PointCloudsMesmoASerio_vPAI

# echo "PointCloudsMesmoASerio_vPAI_NumInv"
# python3 ValidPC_v2.py --rd PointCloudsMesmoASerio_vPAI_NumInv --inv 1

# echo "OQueGostoMesmoEDePCs_vREALISTA"
# python3 ValidPC_v2.py --rd OQueGostoMesmoEDePCs_vREALISTA --inv 1

# echo "OQueGostoMesmoEDePCs_vREALISTA_INV"
# python3 ValidPC_v2.py --rd OQueGostoMesmoEDePCs_vREALISTA_INV --inv 1

# echo "OQueGostoMesmoEDePCs_vPAI"
# python3 ValidPC_v2.py --rd OQueGostoMesmoEDePCs_vPAI

echo "+PCs"
python3 ValidPC_v2.py --rd +PCs