# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 02:07:26 2020

@author: Dio
"""

import frida, sys

#一个函数中调用另一个函数(这个功能暂时还未实现)
jscode = """
if(Java.available){
    Java.perform(function(){
        var mainActivity = Java.use("com.my.fridademo.MainActivity");//获取到类
        var util = Java.use("com.my.fridademo.Util");//获取到类
        mainActivity.func1.overload("int").implementation = function(num){
            console.log("param : " + num);
            var instance = util.$new();//根据类实例化一个对象
            console.log("instance : " + instance);
            int result = instance.func();
            //int result = this.func2(num);
            //console.log("func2 result : "+result);
            //return result;
            return 55;
        }
    });
}
"""

def on_message(message, data):
    if message['type'] == 'send':
        print(" {0}".format(message['payload']))
    else:
        print(message)

# 查找USB设备并附加到目标进程
session = frida.get_usb_device().attach('com.my.fridademo')

# 在目标进程里创建脚本
script = session.create_script(jscode)

# 注册消息回调
script.on('message', on_message)

# 加载创建好的javascript脚本
script.load()

# 读取系统输入
sys.stdin.read()