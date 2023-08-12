import numpy as np
from scipy.spatial import distance
import time
# 定义卫星位置数据
GPS_satellite_positions = {
    'G01': [6882882.4, -938900.8, 2056543.8],
    'G02': [-12425681.1, -22426192.4, 10036943.7],
    # 添加更多卫星位置数据...
}

Beidou_satellite_positions = {
    'B01': [16834553.5, 4887872.6, 19515704.1],
    'B02': [21589003.8, -14664625.7, 10953783.0],
    # 添加更多卫星位置数据...
}

# 模拟接收到的北斗和GPS信号强度数据
Beidou_received_signal_strength = {
    'B01': -70,
    'B02': -80,
    # 添加更多北斗信号强度数据...
}

GPS_received_signal_strength = {
    'G01': -75,
    'G02': -85,
    # 添加更多GPS信号强度数据...
}

def calculate_position(satellite_positions, received_signal_strength):
    # 构建待定位卫星列表和接收信号强度列表
    satellites = []
    signal_strengths = []
    
    for satellite, position in satellite_positions.items():
        print('satellite:',satellite,'position:',position)
        if satellite in received_signal_strength:
            print('satellite:',satellite)
            satellites.append(position)
            signal_strengths.append(received_signal_strength[satellite])
    print('satellites:',satellites)
    
    # 计算待定位卫星间的相对距离
    distances = distance.pdist(satellites)#distances: [21868047.01726467]
    print('distances:',distances)
    # 利用加权最小二乘法求解定位坐标
    weights = np.power(10, np.divide(signal_strengths, -20))
    weights = np.array([5623.4132519, 17782.79410039])
    #print('weights:',type(weights))#weights: [ 5623.4132519  17782.79410039]
    print(np.multiply(distances, weights))#[1.22973065e+11 3.88874977e+11]
    a=np.multiply(distances, weights)
    a.reshape(-1, 1)
    print('111:',type(np.zeros(len(distances))))
    #x, y, z = np.linalg.lstsq(np.multiply(distances, weights), np.zeros(len(distances)))[0]
    x, y, z = np.linalg.lstsq(a, np.zeros(len(distances)))[0]
    return x, y, z


# 测试定位功能
beidou_position = calculate_position(Beidou_satellite_positions, Beidou_received_signal_strength)
gps_position = calculate_position(GPS_satellite_positions, GPS_received_signal_strength)

print("北斗定位结果:", beidou_position)
print("GPS定位结果:", gps_position)
