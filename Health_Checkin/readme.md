# Health_Checkin_Helper

> 健康打卡助手: 将脚本部署于服务器上后，使用cron启动定时任务，每日打卡。

## 脚本说明：

本工程提供两个脚本二选一使用：

- ZJU_Clock_In
- ZJU_Health_Checkin_Helper
  - cst: 是IP定位写死宁波浙软的版本
  - all: 是会根据第一次手动运行获得的IP信息之后默认以这个地理信息打卡的版本

区别于：[ZJU_Clock_In](https://github.com/lgaheilongzi/ZJU-Clock-In) 的地方是，ZJU_Clock_In采用的是利用缓存数据提交，如果没有缓存数据则需要手动先打一次卡；而Health_Checkin_Helper**没有这个限制**，直接可以打卡，并且可以**设置打卡位置**。

## 设置打卡位置说明：

> 目前默认设置的location = {'info': 'LOCATE_SUCCESS', 'status': 1, 'lng': '121.63529', 'lat': '29.89154'}是浙大宁波软院的位置。要想修改成其他位置，需要如下操作【第一次需要手动本机运行获得想要设置的IP信息，之后就可以丢到服务器上运行了】

1. 下载health_checkin_helper.py脚本

2. 法一【推荐】

   - 将写死的`location = {'info': 'LOCATE_SUCCESS', 'status': 1, 'lng': '121.63529', 'lat': '29.89154'}`删除，并将注释的`location = get_ip_location()`和`print(location)`打开注释，然后运行一遍程序，得到自己的IP location信息

   法二【非常不推荐】

   - 自己百度IP定位，明确经纬度信息和填入location字典中，注：这个精度得很高，小数点后8位以上

3. 将得到的IP location信息（返回{...}的json数据）代替写死的浙软location信息

4. 重新运行程序测试

5. 将脚本和配置文件(account.json)放在服务器上cron定时执行

## 下载地址：

- 蓝奏云下载exe地址：https://wwe.lanzoui.com/iDrkRu5y4dg （地址为浙软宁波校区）
- 【推荐】DownGit下载仓库当前文件夹文件：http://tool.mkblog.cn/downgit/#/home, 直接下载health_checkin_helper.py也可以

## 更新日志：
- 2021年9月19日: 执行run中增加随机数延时，以实现每次打卡时间不同。
- 2021年9月17日: Done V1~
- 2021年10月17日：打卡接口数据有所调整，不再需要uid和id参数，因此在正则匹配上删除了这两个参数