# -*- coding: utf-8 -*-

import frida, sys

# 主动调用普通方法  并定时循环
jscode = """
if(Java.available){
    Java.perform(function(){
        //hook动态函数，找到instance实例，从实例调用函数方法
        Java.choose("com.my.fridademo.Util2",{
            onMatch:function(instance){
                loop_func(instance);
            },onComplete:function(){}
        })

        //不能在了线程中操作,因为子线程没在附加到jvm上,只能这样在主线程中定时执行,不过主线程被占用太久会导致python代码崩溃
        function loop_func(instance){  
             for(var i = 0; i < 20; i++){
                instance.active_call_func("hooked_param " + i);
                sleep(5 * 1000);
            }
        }
        
        //参数n为休眠时间，单位为毫秒:
        function sleep(n) {
            var start = new Date().getTime();
            //  console.log('休眠前：' + start);
            while (true) {
                if (new Date().getTime() - start > n) {
                    break;
                }
            }
            // console.log('休眠后：' + new Date().getTime());
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