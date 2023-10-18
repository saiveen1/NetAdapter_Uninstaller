import concurrent.futures
import subprocess

import wmi


def get_real_device_id(pnp_device_id: str):
    t = pnp_device_id.split('\\')
    if t[0] == 'SWD':
        pnp_device_id = t[-1]
    elif t[0] == 'BTH':  # 蓝牙
        pnp_device_id = '\\'.join(t[0:2])
    elif '\\'.join(t[0:2]) == 'ROOT\\NET':  # 一些加速器
        pnp_entities = wmi.WMI().Win32_PnPEntity()
        for pnp_entity in pnp_entities:
            if pnp_entity.PNPDeviceID == pnp_device_id:
                pnp_device_id = pnp_entity.DeviceID
    elif t[0] == 'PCI':
        pnp_device_id = '\\'.join(t[0:2])
    return pnp_device_id


def uninstall_hwd(hwd_id):
    """
    无法传递net_adapter 错误信息 "cannot pickle 'PyIDispatch' object"
    是由于wmi.WMI()返回的对象无法被序列化（pickled）而导致的。
    concurrent.futures.ProcessPoolExecutor在启动子进程时会尝试对任务进行序列化和传递给子进程。
    """
    devcon_path = r'devcon.exe'
    process = subprocess.Popen([devcon_path, 'remove', hwd_id],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               text=True)
    stdout, stderr = process.communicate()
    return hwd_id, stdout, stderr


def remove_net_adapters():
    del_net_adapters = []
    futures = []

    for net_adapter in wmi.WMI().Win32_NetworkAdapter():
        if net_adapter.PNPDeviceID:
            del_net_adapters.append(net_adapter)

    with concurrent.futures.ProcessPoolExecutor() as executor:
        for net_adapter in del_net_adapters:
            # 异步执行uninstall_hwd， get_real_device_id为参数
            future = executor.submit(uninstall_hwd, get_real_device_id(net_adapter.PNPDeviceID))
            futures.append(future)

    count = 1
    for future in concurrent.futures.as_completed(futures):
        hw_id, stdout, stderr = future.result()
        print(stdout)
        print(f"Uninstall {count}.")
        count += 1
        if stdout == 'No devices were removed.\n':
            print(hw_id)

    if len(del_net_adapters) == 0:
        return -1
    return del_net_adapters
