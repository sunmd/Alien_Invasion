import sys
import pygame
from time import sleep

from bullet import Bullet
from alien import Alien

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """相应键值按下"""
    if event.key == pygame.K_RIGHT:
        # 向右移动飞船
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        # 向左移动飞船
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
        

def check_keyup_events(event, ship):
    """响应键值松开"""
    if event.key == pygame.K_RIGHT:
        # 向右移动飞船
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        # 向左移动飞船
        ship.moving_left = False
    elif event.key == pygame.K_q:
        sys.exit()



def check_events(ai_settings, screen, ship, bullets):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

                
def update_screen(ai_settings, screen, ship, aliens, bullets):
    """更新屏幕上的图片，并且切换到新的屏幕上"""
    # 每次循环时都重绘屏幕
    screen.fill(ai_settings.bg_color)

    # 绘制飞船
    ship.blitme()

    # 绘制外星人
    aliens.draw(screen)

    # 绘制子弹
    for bullet in bullets:
        bullet.draw_bullet()

    # 让最近绘制的屏幕可见
    pygame.display.flip()

def update_bullets(ai_settings, screen, ship, aliens, bullets):
    # 子弹移动刷新
    bullets.update()
    check_bullets_aliens_collisions(ai_settings, screen, ship, aliens, bullets)
        # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom < 0:
            bullets.remove(bullet)   

def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    """检查是否有外星人到达了屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break

def ship_hit( ai_settings, stats, screen, ship, aliens, bullets):
    """相应被外星人撞到的飞船"""
    if stats.ships_left > 0:
        # 将ships_left减1
        stats.ships_left -= 1
        # 清空外星人和子弹
        aliens.empty()
        bullets.empty()
        #创建一圈新的外星人，并肩飞船放在屏幕的底端中央
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        #暂停
        sleep(0.5)
    else:
        stats.game_activity = False

def update_allens(ai_settings, stats, screen, ship, aliens, bullets):
    """ 更新外星人群中所有外星人的位置"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    # 检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        print('ship hit!!!')
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)

def fire_bullet(ai_settings, screen, ship, bullets):
    """如果没有达到上线，就可以发送一颗子弹"""
    # 创建子弹，并将子弹放置在bullets
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def create_fleet(ai_settings, screen, ship, aliens):
    """创建外星人群"""
    # 创建一个外星人，并计算一行可容纳多少个外星人
    # 外星人间距为外星人宽度
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien_height = alien.rect.height
    ship_height = ship.rect.height
    number_aliens_x = get_number_aliens_x(ai_settings, alien_width)
    number_rows = get_number_aliens_rows(ai_settings, ship_height,
            alien_height)

    # 创建外星人群
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def get_number_aliens_x(ai_settings, alien_width):
    """计算每行可容纳多少外星人"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / ( 2 * alien_width))
    return number_aliens_x

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """创建一个外星人在当前行"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien_height = alien.rect.height
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.y = alien_height + 2 * alien_height * row_number
    alien.rect.x = alien.x
    alien.rect.y = alien.y
    aliens.add(alien)

def get_number_aliens_rows(ai_settings, ship_height, alien_height):
    """计算屏幕可容纳多少行外星人"""
    available_space_y = (ai_settings.screen_height - (3 * alien_height)
            - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def check_fleet_edges(ai_settings, aliens):
    """有外星人到达边缘时采取相应的措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_dirction(ai_settings, aliens)
            break

def change_fleet_dirction(ai_settings, aliens):
    """将整群外星人下移动，并且改变他们的方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1
    #print(ai_settings.fleet_direction)

def check_bullets_aliens_collisions(ai_settings, screen, ship, aliens, bullets):
    # 检查是否有子弹击中了外星人
    # 如果时这样，就删除相应的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    # 当所有外星人都被消灭的时候，重新添加
    if len(aliens) == 0:
        # 删除现有所有的子弹并新建一群外星人
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)

