# Health_Checkin_Helper

> 健康打卡助手: 将脚本部署于服务器上后，使用cron启动定时任务，每日打卡。

## 脚本说明：

本工程提供两个脚本二选一使用：

- ZJU_Clock_In
- ZJU_Health_Checkin_Helper

区别于：[ZJU_Clock_In](https://github.com/lgaheilongzi/ZJU-Clock-In) 的地方是，ZJU_Clock_In采用的是利用缓存数据提交，如果没有缓存数据则需要手动先打一次卡；而Health_Checkin_Helper**没有这个限制**，直接可以打卡，并且可以**设置打卡位置**。

## 下载地址：

- 蓝奏云下载地址：https://wwe.lanzoui.com/iDrkRu5y4dg

## 更新日志：
- 2021年9月19日: 执行run中增加随机数延时，以实现每次打卡时间不同。
- 2021年9月17日: Done V1~