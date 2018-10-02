import pygame

class Ship():
    def __init__(self, ai_settings, screen):
        """初始化飞船设置起初始化位置"""
        self.screen = screen
        self.ai_settings = ai_settings
        # 加载飞船图像并获取起外接矩形
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # 将每艘新飞船放在屏幕底部中央
        self.rect.centerx =self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # 在飞船的cernter属性存储浮点型数据
        self.center = float(self.rect.centerx)

        # 添加上下左右的表示符号
        self.moving_left = False
        self.moving_right = False

    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)
        
    def update(self):
        if self.moving_left == True and self.center > 0:
            self.center -= self.ai_settings.ship_speed_factor
        elif self.moving_right == True and self.center < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        self.rect.centerx = self.center
