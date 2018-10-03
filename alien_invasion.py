import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
from game_stats import GameStats
import game_functions as gf


def run_game():
    # 初始化游戏设置
    settings = Settings()

    # 初始化游戏并创建一个屏幕对象
    pygame.init()
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    pygame.display.set_caption('Alien Invasion')

    # 创建一个用于存储游戏统计信息的实例
    stats = GameStats(settings)

    # 创建一艘飞船
    ship = Ship(settings, screen)

    # 创建一个用于存储子弹的编组
    bullets = Group()

    # 创建外星人群
    aliens = Group()
    gf.create_fleet(settings, screen, ship, aliens)

    # 设置游戏背景颜色
    back_color = settings.bg_color

    #开始游戏主循环
    while True:

        # 监视键盘和鼠标事件
        gf.check_events(settings, screen, ship, bullets)
        if stats.game_activity:
            # 飞船控制移动
            ship.update()
            gf.update_bullets(settings, screen, ship, aliens, bullets)
            gf.update_allens(settings, stats, screen, ship, aliens, bullets)
            # print('屏幕上的子弹数量：%i'%len(bullets))
            # 刷新屏幕的
            gf.update_screen(settings, screen, ship, aliens, bullets)

run_game()
