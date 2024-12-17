目录结构：  
1、/d_script  执行脚本文件  
2、/d_dest 执行代码后输出结果文件  
3、/d_log 存放报错日志  
4、/d_source 存放交换机信息表  


    # 配置命令列表
    switch_commands = [
        'display current-configuration'
    ]



d_source中csv需要按照以下格式：  

hostname,ip,port,username,password  
sw1,192.168.4.1,22,admin,password  
sw2,192.168.4.2,22,admin,password  


