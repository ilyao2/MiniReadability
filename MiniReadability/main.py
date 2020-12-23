from mini_readability import MiniReadabilityManager as Manager

if __name__ == '__main__':
    manager = Manager("https://lenta.ru/articles/2020/12/23/kozlov/")
    print(manager.text)
