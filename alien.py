import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """表示个人外星人的类型"""
    def __init__(self, ai_settings, screen):
        """初始化外星人并设置其起始位置"""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # 加载外星人图像，并设置起rect属性
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # 每个外星人最初都在屏幕左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 存储外星人的准确位置
        self.x = float(self.rect.x)

    def check_edges(self):
        """如果外星人位于屏幕边缘，就返回True"""
        flag = False
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            flag = True
        elif self.rect.left <= screen_rect.left:
            flag = True
        return flag

    def update(self):
        """向右移动的外星人"""
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        #print('-----%i'%self.x)
        self.rect.x = self.x

    def blitme(self):
        """在指定位置绘制外星人"""
        self.screen.blit(self.image, self.rect)


