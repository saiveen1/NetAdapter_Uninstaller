from time import time
from multiprocessing import freeze_support
from os import path
import locale

import net_adapters

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')


def main():
    devcon_path = r'devcon.exe'

    if not path.exists(devcon_path):
        print("devcon.exe not exist, check path or install manually.")
        return

    try:
        result = net_adapters.remove_net_adapters()
        if result is False:
            print("Uninstallation incomplete. Please uninstall the remaining components manually.")
        elif result == -1:
            print("Network device not detected. Please uninstall manually or check your network connection.")
        else:
            print("Uninstallation successful!\n")

            # print(result)
    except Exception as exp:
        print(exp)


# pyinstaller  --add-binary "devcon.exe" -F main.py
# pyinstaller --add-binary "devcon.exe;/" -F main.py


if __name__ == '__main__':
    freeze_support()  # 添加这一行来处理多进程相关的问题
    start_time = time()
    main()
    end_time = time()
    execution_time = end_time - start_time
    print(f"Execution Time: {execution_time} seconds")
    input("Press any key to exit!")
