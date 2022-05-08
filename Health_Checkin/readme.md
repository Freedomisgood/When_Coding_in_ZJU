# Health_Checkin_Helper

> 健康打卡助手: 将脚本部署于服务器上后，使用cron启动定时任务，每日打卡。
> Python < 3.9

## 前置依赖安装

`pip install -r requirements.txt`

## 脚本说明：

本工程提供两个脚本二选一使用：

- ZJU_Clock_In
- ZJU_Health_Checkin_Helper
  - cst: 是IP定位写死宁波浙软的版本
  - all: 是会根据第一次手动运行获得的IP信息之后默认以这个地理信息打卡的版本

区别于：[ZJU_Clock_In](https://github.com/lgaheilongzi/ZJU-Clock-In) 的地方是，ZJU_Clock_In采用的是利用缓存数据提交，如果没有缓存数据则需要手动先打一次卡；而Health_Checkin_Helper**没有这个限制**，直接可以打卡，并且可以**设置打卡位置**。

## 设置打卡位置说明：

1. 运行 health_checkin_helper.py 脚本: `-a * -p * -lng 121.63529 -lat 29.89154 -c 宁波校区`
   - 如果不清楚参数设置可以运行`python health_checkin_helper.py --help`
2. 将脚本放在服务器上cron定时执行: `05 12 * * * python /home/mrli/dscripts/app/zju/zju_health_checkin.py -a * -p * -lng 121.63529 -lat 29.89154 -c 宁波校区`

## 更新日志：
- 2022年5月8日: 增加验证码识别, 使用ddddocr库完成, 由于onnruntime需要<Py3.9, 所以现在只支持Python3-3.9
- 2021年9月19日: 执行run中增加随机数延时，以实现每次打卡时间不同。
- 2021年9月17日: Done V1~
- 2021年10月17日：打卡接口数据有所调整，不再需要uid和id参数，因此在正则匹配上删除了这两个参数
- 2021年12月5日: 紫金港有疫情情况, 表单参数有所改变