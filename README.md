# modbusTCPsever
## 目录

- [modbusTCPsever](#modbustcpsever)
  - [目录](#目录)
  - [简介](#简介)
  - [主要依赖](#主要依赖)
  - [文件结构](#文件结构)

## 简介
一个基于[Modbus](https://zh.wikipedia.org/wiki/Modbus)Tcp协议的无线传感器网络的控制管理程序，提供一个临时储存器，存储传感器网络数据，供其它设备取用。  
**本项目协议内容：**  
[环境传感器通讯协议说明书.pdf](https://github.com/wu-zero/modbus/blob/master/doc/%E7%8E%AF%E5%A2%83%E4%BC%A0%E6%84%9F%E5%99%A8%E9%80%9A%E8%AE%AF%E5%8D%8F%E8%AE%AE%E8%AF%B4%E6%98%8E%E4%B9%A6.pdf)  
**主要功能：**  
* 通过中继节点（串口通信）实时接收所有传感器节点的数据，存储传感器数据到正确的Modbus寄存器地址中
* 监控所有传感器节点的上线、离线以及稳定性
* 其它功能：
  * 通过终端管理维护传感器网络（查询节点连接、发送命令重启节点等）
  * 全局的时钟同步
  * CRC校验
  * 用户可以通过`.xls文件`进行简单设置

## 主要依赖
```
modbus_tk
pyserial
```

## 文件结构
```
modbus
├─ data
│    └─ save.data
├─ doc
│    ├─ setting.xls
│    └─ 环境传感器通讯协议说明书.docx
├─ log
├─ modbusTCPserver
│    ├─ Consumer_CommandSolve.py
│    ├─ MyModbusServer.py
│    ├─ MySerial.py
│    ├─ Producer_Console.py
│    ├─ Producer_SerialPort.py
│    ├─ SensorModuleMonitor.py
│    ├─ Setting.py
│    ├─ main.py
│    ├─ modbus_tk
│    └─ utils
│           ├─ Convert.py
│           ├─ CyclicRedundancyCheck.py
│           ├─ SetPiTime.py
│           └─ __init__.py
└─ others
       └─ Findport.py
```
`modbusTCPserver文件夹`：本项目的主要实现内容。
`log 文件夹`：log文件。
`doc 文件夹`：协议的详细说明文件、用户的设置说明文件。
`data文件夹`：定时保存的数据，防止程序重启后的数据跳变。



