import pygame

class Message(pygame.sprite.Sprite):
    """A class som simplify message writing."""
    align_left = 'left';
    align_right = 'right';
    align_center = 'center';
    
    def __init__(self, msglist, title=None, rect=None, vector=(0,0), align=align_left, linepadding=0.1,
                 padding=0.1, fontsize=20, fontname=None, center=None, 
                 fgcolor=pygame.Color(255,255,255,255), bgcolor=pygame.Color(0,0,0,255)):
        """rect: pygame.Rect
           msglist: tuple or list of strings
           vector: tuple, coordinates added for each msg
           align: alignet on the surface
           padding: space aroung the text
           fontsize:
           fontname:
           center:
           fgcolor: pygame.Color
           bgcolor: pygame.Color"""
        
        pygame.sprite.Sprite.__init__(self);
        if(rect != None and not isinstance(rect, pygame.Rect) and not isinstance(rect, tuple)):
            raise TypeError('Rect is neither a pygame.Rect nor a tuple');
        if(not isinstance(fgcolor, pygame.Color) and not isinstance(bgcolor, pygame.Color)):
            raise TypeError('fg/bgcolor is not a pygame.Color');
        if(not isinstance(fontsize, int)):
            raise TypeError('font is not an int');
        if(not isinstance(msglist, tuple) and not isinstance(msglist, list)):
            raise TypeError('msglist is neither a list nor a tuple');
        if(not isinstance(vector, tuple)):
            raise TypeError('vector is not a tuple');
        self.rect = pygame.Rect(rect) if(rect != None) else pygame.Rect(((1,1),(1,1)));
        if(center == None and rect == None):
            scR = pygame.display.get_surface().get_rect();
            self.center = (scR.centerx, scR.centery -scR.centery*0.3);
        else:
            self.center = center;
        self.msglist = msglist;
        self.vector = vector;
        self.image = pygame.Surface(self.rect.topleft);
        self.align = align;
        self.font = pygame.font.Font(fontname, fontsize);
        self.fgcolor = fgcolor;
        self.bgcolor = bgcolor;
        self.padding = padding;
        self.title = title;
        self.linepadding = linepadding;
        self.update();

    def update(self):
        """Create a surface with the actual text."""
        self.image.fill(self.bgcolor);
        textList = [];
        if(self.title != None):
            self.font.set_underline(True);
            self.font.set_bold(True);
            textList.append(self.font.render(self.title, True, self.fgcolor));
            self.font.set_underline(False);
            self.font.set_bold(False);
        for msg in self.msglist:
            # Create text
            textList.append(self.font.render(msg, True, self.fgcolor));

        ##  Find the widest one
        width = 0;
        height = 0;
        for txt in textList:
            if(txt.get_rect().width > width): width = txt.get_rect().width;
            if(self.vector[1] == 0): height += txt.get_rect().height;

        width += self.vector[0]*len(textList);
        height += self.vector[1]*len(textList);

        ## Rescale the surface to fit the whole text
        self.image = pygame.transform.scale(self.image, (width+int(width*self.padding*2), height+int(height*self.padding*2)));
        self.rect.size = self.image.get_rect().size;
        
        ## Set rect as left aligned. We might change it later.
        tmpRect = pygame.Rect(((int(width*self.padding),int(height*self.padding)),(0,0)));

        imgRect = self.image.get_rect();
        for txt in textList:
            ## Make the text aligned right
            if(self.align == self.align_right):
                print(str.format("--- tmpRect {0} {1} {2}", tmpRect, tmpRect.left, tmpRect.right));
                tmpRect.left = int(imgRect.width - txt.get_rect().width - imgRect.width*self.padding);
                print(str.format("=== tmpRect {0} {1} {2}", tmpRect,  tmpRect.left, tmpRect.right));

            ## Make the text aligned center
            if(self.align == self.align_center):
                tmpRect.left = int(self.image.get_rect().width/2 - txt.get_rect().width/2);
                
            self.image.blit(txt, tmpRect.topleft);
            if(self.vector[1] == 0):
                self.vector = (self.vector[0],int(txt.get_rect().height*(1+self.linepadding)));
            tmpRect = tmpRect.move(self.vector);

        ## Set the whole sprite to requested center
        if(self.center != None):
            self.rect.center = self.center;
            
