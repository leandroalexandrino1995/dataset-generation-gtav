from dataclasses import dataclass
from enum import Enum

# used to configure the dataset generation (according to the interface of the "Pointcloud Workbench" project)
@dataclass
class ConfigParams:
    # kitti dataset directories
    kittiLabelsDir: str = 'data_object_label_2/training/label_2/'
    kittiVelodyneDir: str = 'data_object_velodyne/training/velodyne/'
    kittiViewsDir: str = 'data_object_image_2/training/image_2/'
    kittiCalibDir: str = 'data_object_calib/training/calib/'

    kittiLabelsDirTesting: str = 'data_object_label_2/testing/label_2/'
    kittiVelodyneDirTesting: str = 'data_object_velodyne/testing/velodyne/'
    kittiViewsDirTesting: str = 'data_object_image_2/testing/image_2/'
    kittiCalibDirTesting: str = 'data_object_calib/testing/calib/'

    # gta inpu samples filenames
    pcPlyFn: str = "LiDAR_PointCloud.ply"
    pcPlyNoiseFn: str = "LiDAR_PointCloud_error.ply"
    pcLabelsFn: str = "LiDAR_PointCloud_labels.txt"
    pcLabelsDetailedFn: str = "LiDAR_PointCloud_labelsDetailed.txt"
    # pcProjectedPointsFn: str = "LiDAR_PointCloud_points.txt" -- Não tenho isto, será que é necessário?
    # fvImgFn: str = "LiDAR_PointCloud_Camera_Print_Day_0.bmp"
    fvImgFn: str = "LiDAR_PointCloud_Camera_Print_Day_0.jpg"
    # output filenames
    rotationFn: str = "LiDAR_PointCloud_rotation.txt"
    entityInfoFn: str = "LiDAR_PointCloud_vehicles_dims.txt"
    rotatedPointCloudFn: str = "Rotated point cloud.ply"
    frontviewPointCloudFn: str = "Frontview point cloud.ply" # -- Não tenho isto, será que é necessário
    vehiclesOnlyPointCloudFn: str = "Vehicles point cloud.ply"
    pedestriansOnlyPointCloudFn: str = "Pedestrians point cloud.ply"
    noBackgroundPointsCloudFn: str = "No background point cloud.ply"

    # data formatting settings used by the UI
    useNoise: bool = False                           
    includeIntensity: (bool, float) = (True, 0)     
    ignoreVehicles: bool = False                      
    ignorePedestrians: bool = True                      
    filterByDistance: (bool, float) = (False, 50)       # ignore entities at a distance greater than the specified
    targetArchitecture: str = "FrustumPointnet"
    genSingleEntities: bool = True                    
    genCloudsWithoutBackground: bool = True            
    fov: float = 75                                   


# GTA entity indexes
class EntityType(Enum):
    BACKGROUND = 0
    PEDESTRIAN = 1
    VEHICLE = 2
    PROPS = 3


class PointAttributes(Enum):
    COLOR = 'c'
    INTENSITY = 'i'

class KittiTypes(Enum):
    CAR = "Car"
    VAN = "Van"
    TRUCK = "Truck"
    PEDESTRIAN = "Pedestrian"
    PERSON_SITTING = "Person_sitting"
    CYCLIST = "Cyclist"
    TRAM = "Tram"
    MISC = "Misc"
    DONTCARE = 'DontCare'

class TargetArch(Enum):
    FRUSTUM_POINTNET = 0