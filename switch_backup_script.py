import csv
import paramiko
import datetime
import os

# 设置日志和结果输出目录
log_dir = '/home/aie/d_log/backup'
dest_dir = '/home/aie/d_dest/backup'

# 获取当前日期作为文件夹名的一部分
date_str = datetime.datetime.now().strftime('%Y-%m-%d')

# 创建以日期命名的子目录
daily_log_dir = os.path.join(log_dir, date_str)
daily_dest_dir = os.path.join(dest_dir, date_str)
os.makedirs(daily_log_dir, exist_ok=True)
os.makedirs(daily_dest_dir, exist_ok=True)

# 读取设备列表
def read_device_list(csv_filename):
    with open(csv_filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)

def execute_commands(ssh, commands, file_handle):
    for command in commands:
        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode()
        error = stderr.read().decode()
        if error:
            file_handle.write(f"Error executing command: {command}\n{error}\n")
        if output:
            file_handle.write(f"Output from command '{command}':\n{output}\n")
        file_handle.flush()

def main():
    # CSV文件名
    csv_filename = '/home/aie/d_source/source_sw_list.csv'
    json_list = read_device_list(csv_filename)

    # 配置命令列表
    switch_commands = [
        'display current-configuration'
    ]

    # 遍历设备列表并执行命令
    for device in json_list:
        hostname = device['hostname']
        dest_filename = f'{hostname}.txt'
        bug_filename = f'{hostname}_bug.txt'

        try:
            # 确保目录存在
            os.makedirs(daily_dest_dir, exist_ok=True)

            # 建立SSH连接
            with paramiko.SSHClient() as ssh:
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(device['ip'], int(device['port']), device['username'], device['password'])

                # 执行 switch_commands 并记录到 dest_file
                with open(os.path.join(daily_dest_dir, dest_filename), 'a') as dest_file:
                    execute_commands(ssh, switch_commands, dest_file)

        except (paramiko.AuthenticationException, paramiko.SSHException) as e:
            with open(os.path.join(daily_log_dir, bug_filename), 'a') as bug_file:
                bug_file.write(f"SSH error on {hostname}: {e}\n")
        except Exception as e:
            with open(os.path.join(daily_log_dir, bug_filename), 'a') as bug_file:
                bug_file.write(f"Unexpected error on {hostname}: {e}\n")

if __name__ == "__main__":
    main()
