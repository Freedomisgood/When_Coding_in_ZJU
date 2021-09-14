# Net_Assistant

- [基于AutoJS的CST上网APP](./Andriod)
- [CST-PC上网二进制](./PC)

> :smile: 运行上网助手: 运行APP或者exe即可登录上网，但由于CST校园网免费账号只能
> 一个设备登录，因此目前实现机制为**设备上线前会下线已上线的设备，从而保证当前设备上线成功**
> TODO：为了能够更好地利用空闲账号，可以搭建账号池，即每个宿舍留出固定路由器的账号后
> 共享出自己的账号作为公共账号, 从而高效利用所有人的上网账号并实现单人可以上线多设备的可能。
> 
```
账号池有两种方式维护： 
    1.账号信息放在配套的本地配置文件中==>随机碰撞找到空闲账号
    2.账号信息放在服务器上，通过http请求空闲账号==>通过服务器管控，登出时需要反馈给服务器
如果没有空闲账号，则强迫登录自己账号的设备下线，使自己上线
```

