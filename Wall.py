## Kenneth Andersson
## Multimediaprogrammering i Python (DSV)

import pygame

class Wall(pygame.sprite.Sprite):
    """Paints a wall object"""
    def __init__(self, rect):
        """rect, ((x,y),(width,height))"""
        pygame.sprite.Sprite.__init__(self);
        if(not isinstance(rect, pygame.Rect) and not isinstance(rect, tuple)):
            raise TypeError('Rect is neither a pygame.Rect nor a tuple');
        self.color = (255, 255, 255);
        self.rect = pygame.Rect(rect);
        self.image = pygame.Surface((self.rect.width, self.rect.height));
        pygame.draw.rect(self.image, self.color,
                         ((0, 0),(self.rect.width, self.rect.height)), 1);
        
        pygame.draw.line(self.image, self.color,
                         (0, 0),(self.rect.width-1, self.rect.height), 1);

        pygame.draw.line(self.image, self.color,
                         (self.rect.width-1, 0), (0, self.rect.height), 1);

    def update(self):
        """Updates wall object"""
