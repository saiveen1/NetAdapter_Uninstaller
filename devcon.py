from subprocess import run as subp_run

devcon_path = r'devcon.exe'
device_name = 'Realtek PCIe GbE Family Controller'

# 枚举设备
result = subp_run([devcon_path, 'find', '*', 'more'], capture_output=True, text=True)
device_list = result.stdout.split('\n')
# 查找设备
device_id = None
for device in device_list:
    if device_name in device:
        device_id = device.split(':')[0].strip()
        break
# 卸载设备
if device_id:
    devcon_path = r'devcon.exe'
    subp_run([devcon_path, 'remove', device_id], capture_output=True, text=True)
    print(f"Device '{device_name}' has been uninstalled.")
else:
    print(f"Device '{device_name}' not found.")
