# Python-Kinectv2
This repo shows how to use Python connect the Kinect v2 camera
## 1 Environment

- Anaconda 64-bit（32-bit is ok）
- NumPy
- comtypes
- PyGame

## 2 Preparation

1. Install Kinect for Windows SDK v2 [Baidu Yun](https://pan.baidu.com/s/1i0VZkBdmeofV8MatbzQHfA) Code:p73c

2. Install PyKinect2 [Git](https://github.com/Kinect/PyKinect2)

   Anaconda 64-bit version: copy ./pykinect2 to path/to/your/Anaconda/site-package

   Anaconda 32-bit version:

   ```shell
   pip install pykinect2
   ```

## 3 Run

1. read RGB frames and Depth frames

```
cd ./demo
python read_stream.py
```

2. read RGB frames and Depth frames (RGB and Depth are mapped) and save it in ./result

```
cd ./demo
python mapper.py
```
## Acknowledgement
A large portion of code is borrowed from [Kinect/PyKinect2](https://github.com/Kinect/PyKinect2) and [KonstantinosAng/PyKinect2-Mapper-Functions](https://github.com/KonstantinosAng/PyKinect2-Mapper-Functions), many thanks to their wonderful work!

# 使用python连接Kinect v2相机

我已将所有的工程文件上传至Github中，请上git自取代码。

## 1 机器所需环境

- Anaconda 64-bit（32-bit也可以）
- NumPy
- comtypes
- PyGame

## 2 环境配置过程

1. 安装Kinect for Windows SDK v2 [百度云链接](https://pan.baidu.com/s/1i0VZkBdmeofV8MatbzQHfA) Code:p73c

2. 安装PyKinect2 [官方Git](https://github.com/Kinect/PyKinect2)

   Anaconda 64-bit版本：请将git工程中的pykinect2文件夹粘贴至anaconda中的site-package文件夹中

   Anaconda 32-bit版本：

   ```shell
   pip install pykinect2
   ```

## 3 代码运行

1. 读取可见光和深度流

```
cd ./demo
python read_stream.py
```

2. 读取可见光图像和深度图像（自动校正深度图像和可见光图像视场角），并将其保存至result文件夹

```
cd ./demo
python mapper.py
```

## Acknowledgement
A large portion of code is borrowed from [Kinect/PyKinect2](https://github.com/Kinect/PyKinect2) and [KonstantinosAng/PyKinect2-Mapper-Functions](https://github.com/KonstantinosAng/PyKinect2-Mapper-Functions), many thanks to their wonderful work!
