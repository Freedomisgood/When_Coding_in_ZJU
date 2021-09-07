#  ZJU-新生报到服务-适应性课程速过

>  ZJU迎新系统中需要完成的课程任务： http://regi.zju.edu.cn/classes (首页->报到服务->适应性课程)

需要填写的参数有两个：（需要从Cookies中获取）

- JSESSIONID
- stu_token

## 方一(旧版)：

### 1.获取所需参数：

> 选择下列一种即可，推荐第一种

1. 点击浏览器地址栏前的安全性图标，选择Cookies，然后按如下操作

![](https://i.loli.net/2021/08/23/BGwCz3AcpaSlDkE.png)

2. 先访问 http://regi.zju.edu.cn/classes 登录账号后后打开开发者工具(Chrome为F12快捷键) 然后将Application菜单栏下Storage->cookies中的stu_token和 JSESSIONID 对应输入为本程序的参数

![](https://i.loli.net/2021/08/23/LiudKFgpBrNkqn3.png)

### 2.执行程序

在脚本所在目录打开命令行，输入：` python zju_guide_class.py -s 获取的JSESSIONID -t  获取的STU_TOKEN`

![](https://i.loli.net/2021/08/23/VtS7DH2PyGM8hsc.png)

## 方二(2021年9月7日更新)：

运行通过统一认证平台登录获得信息从而运行的程序: `python guide_class_login.py`