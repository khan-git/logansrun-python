## Kenneth Andersson
## Multimediaprogrammering i Python (DSV)

import pygame

class Hero(pygame.sprite.Sprite):
    """Logan him self."""
    def __init__(self, rect, color=(255,255,255)):
        pygame.sprite.Sprite.__init__(self);
        if(not isinstance(rect, pygame.Rect) and not isinstance(rect, tuple)):
            raise TypeError('Rect is neither a pygame.Rect nor a tuple');
        if(not isinstance(color, tuple)):
            raise TypeError('color is not a tuple');
        self.color = color;
        self.rect = pygame.Rect(rect);
        self.oldrect = self.rect;
        self.createImages();
        self.direction = 'left';
        self.image = self.baseImage
        self.fps = 0;

    def createImages(self):
        """Draw Logan."""
        self.baseImage = pygame.Surface((self.rect.width, self.rect.height));
        rect = self.baseImage.get_rect()

        ## Body
        pygame.draw.ellipse(self.baseImage, (50,150,50),
                               ((rect.width/4,0),(rect.width/4*2, rect.height)), 0);

        ## Arms
        pygame.draw.ellipse(self.baseImage, (50,150,50),
                               ((0,0),(rect.width/2, rect.height/3)), 0);
        pygame.draw.ellipse(self.baseImage, (50,150,50),
                               ((rect.width/2, rect.height/4*3), (rect.width/2, rect.height/3)), 0);

        ## Head
        pygame.draw.circle(self.baseImage, self.color, rect.center, rect.width/3, 0);
        

    def update(self, ticks):
        """Update ticks"""
        self.fps += ticks;


    def rotate(self, direction):
        """Rotates the hero."""
        if(not isinstance(direction, str)):
            raise TypeError('direction is not of type str');
        if(direction.lower() == 'left' and self.direction != 'left'):
            self.image = self.baseImage;
            self.direction = 'left';
        elif(direction.lower() == 'up' and self.direction != 'up'):
            self.image = pygame.transform.rotate(self.baseImage, 90)
            self.direction = 'up';


    def move(self, vector, group):
        """Move Logan and flip the image at certain intervals.
           Checks for collisions with sent group to validate move."""
        self.oldrect = self.rect;
        self.rect = self.rect.move(vector);
        if(pygame.sprite.spritecollideany(self, group) != None):
            self.rect = self.oldrect;
        elif(self.fps > 100):
            self.image = pygame.transform.flip(self.image, True, False);
            self.fps = 0;


    def inflate(self, x, y):
        """Resize rect on our hero."""
        self.oldFlate = self.rect;
        self.rect = self.rect.inflate(x,y);

    def deflate(self):
        """Restore size."""
        self.rect = self.oldFlate;
