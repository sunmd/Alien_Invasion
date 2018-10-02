import sys
import pygame

from bullet import Bullet

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

                
def update_screen(ai_settings, screen, ship, bullets):
    """更新屏幕上的图片，并且切换到新的屏幕上"""
    # 每次循环时都重绘屏幕
    screen.fill(ai_settings.bg_color)

    # 绘制飞船
    ship.blitme()

    # 绘制子弹
    for bullet in bullets:
        bullet.draw_bullet()

    # 让最近绘制的屏幕可见
    pygame.display.flip()

def update_bullets(bullets):
    # 子弹移动刷新
    bullets.update()
    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom < 0:
            bullets.remove(bullet)   

def fire_bullet(ai_settings, screen, ship, bullets):
    """如果没有达到上线，就可以发送一颗子弹"""
    # 创建子弹，并将子弹放置在bullets
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
