from mini_readability import MiniReadabilityManager as Manager

if __name__ == '__main__':
    manager = Manager()
    manager.use_config('config.json')
    manager.read_url("https://lenta.ru/articles/2020/12/23/kozlov/")
    print(manager.text)
