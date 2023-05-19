# 北醒Modbus协议在Python下Tkinter模块实现功能配置的GUI使用教程

## 功能介绍
1.设备连接（已知雷达设备的波特率和站号，进行测距）

2.雷达配置（已知雷达设备的波特率和站号，修改雷达波特率、雷达id、恢复出厂设置）

3.设备查找（扫描已经忘记波特率或站号的Modbus雷达设备，并获得测距值）
## 界面展示
![39702710249687](https://github.com/ahhlyy/lidar_project_gui/assets/76689985/bf8f1cb5-2d2d-4463-9489-1284c9badd2a)


## 使用步骤
+ 已知雷达设备的波特率和id，能够创建Modbus从站连接，进行测距，见 [1.设备连接](#1)
+ 已知雷达设备的波特率和id，在Modbus从站连接成功后，能够进行雷达配置，如修改波特率、修改id、恢复出厂等，见 [2.雷达配置](#2)
+ 未知雷达设备的波特率和id，想要进行测距和雷达配置，可进行设备查找，获得设备的波特率和id，见 [3.设备查找](#3)


<a id=1> </a>
### 1.设备连接
当已知设备波特率和id时，可连接设备，获得测距值显示。

<mark>注：</mark>为防止连接时间过长或忘记断开连接导致程序卡死，当鼠标移出连接按钮范围，则自动取消连接测距。

#### 1.1 图示教程
![557245810249688](https://github.com/ahhlyy/lidar_project_gui/assets/76689985/ece6ffad-eb73-443c-9d50-f3b4fc8827ed)
#### 1.2 动态演示
![288842711246243](https://github.com/ahhlyy/lidar_project_gui/assets/76689985/3b8c4583-c953-4f09-b20d-18f64dd67a2c)

<a id=2> </a>
### 2.雷达配置
+ [修改波特率](#2.1)
+ [修改id](#2.2)
+ [恢复出厂](#2.3)

<mark>注1：</mark> 对雷达配置进行修改时，需已知设备的波特率和id，若未知波特率和id，则无法连接Modbus从站，不能对配置进行修改。可先进行设备查找，扫描设备后，获得设备波特率和id，再进行配置。

<mark>注2：</mark> 对雷达配置进行修改时，若无设置成功提示框弹出，则设置修改失败，注意检查设备是否成功连接，即所选择的波特率和id号是否正确，若设备成功连接，会显示距离值，见[1.设备连接](#1)

<mark>注3：</mark> 每进行一次配置修改，需检查设备是否成功连接，注意检查选择的波特率和id是否正确，若忘记设备波特率和id，见 [3.设备查找](#3)

<a id=2.1> </a>
#### 2.1 修改波特率
##### 2.1.1 图示教程
![421842311236223](https://github.com/ahhlyy/lidar_project_gui/assets/76689985/0e1f7b49-2806-465d-b071-3dc46eee13cc)
##### 2.1.2 动态演示
![281414611241997](https://github.com/ahhlyy/lidar_project_gui/assets/76689985/2ef869eb-cc48-4369-86e9-54a7f3b7d6a7)

<a id=2.2> </a>
#### 2.2 修改id
##### 2.2.1 图示教程
![557254211253799](https://github.com/ahhlyy/lidar_project_gui/assets/76689985/76193728-0869-427a-94ad-0aa6e00ff5e5)
##### 2.2.2 动态演示
![575424113259877](https://github.com/ahhlyy/lidar_project_gui/assets/76689985/50cbb039-22cc-4601-9f68-ebb198b3b2f0)

<a id=2.3> </a>
#### 2.3 恢复出厂
##### 2.3.1 图示教程
![100605211240479](https://github.com/ahhlyy/lidar_project_gui/assets/76689985/d8ac0bec-5629-4218-9f26-d8a49069c17c)
##### 2.3.2 动态演示
![477785013257481](https://github.com/ahhlyy/lidar_project_gui/assets/76689985/f731318c-00de-4686-a3ce-910f27a55aa7)

<a id=3> </a>
### 3.设备查找
当未知设备波特率和id时，可进行设备扫描，获得设备的波特率和id。
#### 3.1 图示教程
![266575413233513](https://github.com/ahhlyy/lidar_project_gui/assets/76689985/139b84ec-f5bd-4dbd-9ba8-6ed784e36898)
#### 3.2 动态演示
![391730314254983](https://github.com/ahhlyy/lidar_project_gui/assets/76689985/4446ac92-9c53-49ec-ab01-bb7270e24dec)
