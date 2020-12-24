import sys
from mini_readability import MiniReadabilityManager as Manager

if __name__ == '__main__':
    # Example URL https://lenta.ru/articles/2020/12/23/kozlov/
    URL = ''
    config_path = 'config.json'
    if len(sys.argv) == 1:
        URL = input('input URL: ')
    if len(sys.argv) >= 2:
        URL = sys.argv[1]
    manager = Manager()
    if len(sys.argv) == 3:
        manager.use_config(sys.argv[2])
    if len(sys.argv) > 3:
        print('usage: main.py <URL <config_path>>')

    manager.read_url(URL)
    manager.save_in_file()
