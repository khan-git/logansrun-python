## Kenneth Andersson
## Multimediaprogrammering i Python (DSV)

import os, sys, pygame, math, cPickle, time, datetime, scriptutil, random
from pygame.locals import *
from Hero import *
from Wall import *
from Message import *
from Scores import *

class LogansRun():
    """The game Logans Run."""

    
    def __init__(self, size=(800,800), objectsize=20):
        """Initialize the class."""
        if(not isinstance(size, tuple)):
            raise TypeError('size is not a tuple');
        if(not isinstance(objectsize, int)):
            raise TypeError('objectsize is not an int');
        pygame.init();
        pygame.mixer.init();
        pygame.display.set_caption("Logans Run");
        pygame.display.set_mode(size);
        self.screen = pygame.display.get_surface();
        self.objectsize = objectsize;
        self.clock = pygame.time.Clock();
        self.background = pygame.Surface(self.screen.get_rect().size);
        self.background.fill((0,0,0));
        self.level = GameLevel();
        self.centeroffset = 0.4;
        pygame.event.set_allowed(None);
        self.walls = pygame.sprite.RenderPlain();
        self.badwalls = pygame.sprite.RenderPlain();
        self.hero = pygame.sprite.GroupSingle(Hero(pygame.Rect((100,100),(self.objectsize, self.objectsize))));
        self.map = None;
        self.name = None;
        self.scores = Scores();
        pygame.mixer.init();
        self.music = Music();
        


    def run(self):
        """Run the game."""
        self.music.playMusic('./audio/bgmusic.mp3');
        self.name = self.askUserInput('Enter your name:');

        self.titleSprite = pygame.sprite.GroupSingle(
            Message(("Logans Run",), fontsize=140, ));
        self.titleSprite.sprite.image.set_alpha(255);

        self.menuSprite = pygame.sprite.GroupSingle(
            Message(("1. Play",
                     "2. Play a Single map",
                     "3. Score List",
                     "4. Instructions",
                     "5. Create Map",
                     "6. Edit Map",
                     "Q. Quit"),
                    "Select a menu option:"));
        self.menuSprite.sprite.image.set_alpha(0);
        self.titleSprite.sprite.rect.midbottom = self.menuSprite.sprite.rect.midtop;
        
        pygame.event.set_allowed((KEYDOWN, pygame.QUIT));
        pygame.event.clear();

        ## Directs the alpha change on titleSprite
        alpha = True;
        
        ## Master Loop
        done = False;
        while(not done):
            self.screen.fill((0,0,0));
            self.titleSprite.draw(self.screen);
            self.menuSprite.draw(self.screen);
            pygame.display.flip();

            for event in self.getEvents():
                if(event.type == KEYDOWN):
                    if(event.key == K_1): self.playLevels();
                    elif(event.key == K_2): self.playSingleMap();
                    elif(event.key == K_3): self.scoreList();
                    elif(event.key == K_4): self.printInstructions();
                    elif(event.key == K_5): self.createMap();
                    elif(event.key == K_6): self.editExistingMap();

            ## Lets handle som cool effects
            if(alpha == True):
                self.titleSprite.sprite.image.set_alpha(self.titleSprite.sprite.image.get_alpha()-1);
                self.menuSprite.sprite.image.set_alpha(self.menuSprite.sprite.image.get_alpha()+1);
            else:
                self.titleSprite.sprite.image.set_alpha(self.titleSprite.sprite.image.get_alpha()+1);
                self.menuSprite.sprite.image.set_alpha(self.menuSprite.sprite.image.get_alpha()-1);

            if(self.titleSprite.sprite.image.get_alpha() <= 1): alpha = False;
            elif(self.titleSprite.sprite.image.get_alpha() >= 254): alpha = True;
            
            self.clock.tick(50);

    def scoreList(self):
        """Print the scorelist of each map."""
        maps = scriptutil.ffind('./maps', ('*.map',))
        maps.sort();
        self.screen.fill((0,0,0));
        for map in maps:
            msgSprite = self.scores.printScores(map);
            msgSprite.draw(self.screen);
            pygame.display.flip();
            done = False;
            while(not done):
                for event in self.getEvents(exitKey=None):
                    if(event.type == KEYDOWN):
                        if(event.key == K_RETURN or event.key == K_SPACE):
                            done = True;
                        elif(event.key == K_q):
                            msgSprite.clear(self.screen, self.background);
                            return;
            msgSprite.clear(self.screen, self.background);
    
    def editExistingMap(self):
        """Edit an existing map."""
        self.selectMap();
        if(self.map != None):
            self.loadMap();
            self.editMap();

    def selectMap(self, prefix=''):
        """Let user select a map."""
        maps = scriptutil.ffind('./maps', (prefix+'*.map',))
        userFil = './maps/'+self.askUserInput('Enter map name')+'.map';

        if(userFil in maps):
            self.map = userFil;
        else:
            self.printMessageWOption(("",), title="Couldn't find the map!");
            return None;
        
              
    def selectLevel(self):
        """Set diffculty. Decreases the surrounding view"""
        msgSprite = pygame.sprite.GroupSingle(
            Message((self.level.levels),
                    "Select level", vector=(10,0)));
        self.screen.fill((0,0,0));
        msgSprite.draw(self.screen);
        pygame.display.flip();
        pygame.event.set_allowed((KEYDOWN, pygame.QUIT));
        pygame.event.clear();
        while(True):
            for event in self.getEvents():
                if(event.type == KEYDOWN and event.key >= K_1 and event.key <= K_3):
                    self.level.set(event.key - K_0)
                    msgSprite.clear(self.screen, self.background);
                    return
            self.clock.tick(50);


    
    def play(self):
        """The actual game play loop."""
        pygame.event.set_allowed((KEYDOWN, pygame.QUIT));
        pygame.mixer.music.fadeout(500);
        self.music.playMusic();

        ## Save start time
        playTime = time.time();
        done = False;
        while(not done):
            for event in self.getEvents(exitKey=None):
                ## Suicide option
                if(event.type == KEYDOWN and event.key == K_q):
                    if(self.askQuestion(("Quitting the game! Are you sure?",
                                         "Y(es)    N(o)"),
                                        (K_y, K_n)) == K_y):
                        pygame.mixer.music.fadeout(1000);
                        self.music.playMusic('./audio/bgmusic.mp3');
                        return False;
                        
            ## Check keys and move Logan
            self.hero.update(self.clock.get_time());

            keys = pygame.key.get_pressed();
            if(keys[pygame.K_LEFT]):
                self.hero.sprite.rotate('left');
                self.hero.sprite.move((-2,0), self.walls);

            if(keys[pygame.K_RIGHT]):
                self.hero.sprite.rotate('left');
                self.hero.sprite.move((2,0), self.walls);
                    
            if(keys[pygame.K_UP]):
                self.hero.sprite.rotate('up');
                self.hero.sprite.move((0,-2), self.walls);
                    
            if(keys[pygame.K_DOWN]):
                self.hero.sprite.rotate('up');
                self.hero.sprite.move((0,2), self.walls);
                
            ## Find surrounding walls according to level
            self.hero.sprite.inflate(self.level.size, self.level.size);
            wallPaint = pygame.sprite.RenderPlain(pygame.sprite.spritecollide(self.hero.sprite, self.walls, False));
            self.hero.sprite.deflate();
            self.walls.clear(self.screen, self.background);
            wallPaint.draw(self.screen);
            self.hero.clear(self.screen, self.background);
            self.hero.draw(self.screen);

            ## Add clock in corner
            clockSprite = self.printClock(time.time()-playTime);
            clockSprite.draw(self.screen);

            pygame.display.flip();

            self.clock.tick(50);

            ## End the game if Logan is outside the screen
            if(self.screen.get_rect().contains(self.hero.sprite.rect) == False):
                break;

        ## Calculate game duration
        playTime = time.time() - playTime;

        self.screen.fill((0,0,0));
        
        ## Change music
        pygame.mixer.music.fadeout(1000);
        self.music.playMusic('./audio/bgmusic.mp3');

        ## Save the score
        self.scores.addScore(self.map, self.name, playTime, self.level.text);

        ## Tell the player how good they are
        self.printMessageWOption((str.format("You helped Logan escape in {0} minutes and {1} seconds.",
                                             time.strftime("%M", time.localtime(playTime)),
                                             time.strftime("%S", time.localtime(playTime))),
                                  "What will wait for him on the other side."),
                                 str.format("Congratulations, {0}!", self.name));

        ## Print scores and show the player how bad they are
        self.printMessageWOption(self.scores.printScores(self.map));
        return True;

    def playLevels(self):
        """Play each level in turn."""
        self.selectLevel();
        maps = scriptutil.ffind('./maps', ('Level*.map',))
        maps.sort();
        for map in maps:
            self.map = map;
            self.loadMap();
            self.screen.fill((0,0,0));
            self.walls.draw(self.screen);
            pygame.event.clear();
            if(self.play() == False):
                break;
            
        self.printEndGame();
        
    def playSingleMap(self):
        """Play just a single map selected from a list."""
        maps = scriptutil.ffind('./maps', ('*.map',));
        maps.sort();
        i = 0;

        ## The list lenght. Increase to show more maps on each page.
        listLen = 3;
        ## Change this to the same number as listLen.
        lastKey = K_3;
        
        mapNo = 0;

        ## Outer loop to create map lists
        done = False;
        while(not done):
            msg = [];
            lastIndex = i+listLen if(len(maps) > i+listLen) else len(maps);
            for j in range(i, lastIndex):
                msg.append(str.format("{0} - {1}", j-i+1, os.path.basename(maps[j][0:-4])));
            self.screen.fill((0,0,0));
            msgSprite = self.printMessage(msg, "Select map: P(revious) N(ext)", align = Message.align_left);

            ### Inner loop for selection
            doneKey = False;
            while(not doneKey):
                for event in self.getEvents(exitKey=None, allowed = (KEYDOWN, pygame.QUIT)):
                    if(event.type == KEYDOWN):
                        if(event.key == K_q):
                            return;
                        elif(event.key == K_n):
                            i = i+listLen if(i+listLen < len(maps)) else i;
                            doneKey = True;
                            break;
                        elif(event.key == K_p):
                            i -= listLen if(i >listLen+1) else i;
                            doneKey = True;
                            break;
                        elif(event.key >= K_1 and event.key <= lastKey):
                            mapNo = i + event.key - K_0;
                            doneKey = True;
                            self.map = maps[mapNo-1];
                            self.loadMap();
                            self.screen.fill((0,0,0));
                            self.walls.draw(self.screen);
                            pygame.event.clear();
                            doneKey = False;
                            self.selectLevel();
                            self.play();
                            self.screen.fill((0,0,0));
                            msgSprite.draw(self.screen);

                pygame.display.flip();
                self.clock.tick(50);
            msgSprite.clear(self.screen, self.background);


    def printEndGame(self):
        """Print the end message."""
        self.screen.fill((0,0,0));
        self.printMessageWOption(("You helped Logan escape!",
                   "He will be a free man now, thanks to you!"),
                  "FREEDOM at LAST!");

            
    def printText(self, msgs, ((x,y),(z,v))):
        """Creates messages and print them on the screen.
           msgs: Message list
           xy,zv: start (x,y), move each msg (z,v)"""
        if(not isinstance(msgs, tuple)):
           raise TypeError('msgs is not of type tuple');
        if(not isinstance(x, int) or
           not isinstance(y, int) or
           not isinstance(z, int) or
           not isinstance(v, int) ):
            raise TypeError('x,y,z or v is not of type int');
        
        i = 0;
        textList = [];
        for msg in msgs:
            # Create text
            font = pygame.font.Font(None, 20);
            text = font.render(msg, True, (255,255, 255));
            textRect = text.get_rect();

            # Center the rectangle
            textRect.x = x;
            textRect.y = y;
            textRect = textRect.move((z*i,v*i));
            textList.append((text,textRect));
            i+=1;
        return textList;

    def createMap(self):
        """Create a Map."""
        self.walls.empty();
        self.badwalls.empty();
        self.hero.sprite.rect = pygame.Rect((-100,-100),(self.objectsize,self.objectsize));
        
        ## Fill the screen with walls
        scR = pygame.display.get_surface().get_rect();
        width_limit = scR.width/self.objectsize;
        height_limit = scR.height/self.objectsize;
        for x in range(width_limit):
            for y in range(height_limit):
                wall = Wall(((x*self.objectsize,y*self.objectsize),(self.objectsize,self.objectsize)));
                self.walls.add(wall);
        self.editMap();

    def editMap(self):
        """Edit a map."""
        pygame.event.set_allowed((KEYDOWN, pygame.QUIT, MOUSEBUTTONDOWN));

        self.screen.fill((0,0,0));
        self.printMessageWOption(("Click on the walls you don't want.",
                           "Click again to restore a wall.",
                           "Press S when you are done."));

        self.walls.draw(self.screen);
        done = False;
        while(not done):
            for event in self.getEvents():
                if(event.type == KEYDOWN and event.key == K_s):
                    key = self.askQuestion(("Are you done?",
                                       "Y(es)    N(o)"), (K_y, K_n));
                    if(key == K_y):
                        done = True;
                        break;
                            
                elif(event.type == MOUSEBUTTONDOWN):
                    pos = pygame.mouse.get_pos()
                    walle = Wall(pygame.Rect((pos),(1,1)));
                    badWall = pygame.sprite.spritecollideany(walle, self.walls);
                    if(badWall != None):
                        badWall.remove(self.walls);
                        self.badwalls.add(badWall);
                    else:
                        badWall = pygame.sprite.spritecollideany(walle, self.badwalls);
                        self.walls.add(badWall);
                        badWall.remove(self.badwalls);
                        
            self.badwalls.clear(self.screen, self.background);
            self.walls.clear(self.screen, self.background);
            self.walls.draw(self.screen);

            pygame.display.flip();
            self.clock.tick(50);

        self.walls.draw(self.screen);
        self.printMessageWOption(("Click where the hero should start.",));

        if(pygame.sprite.spritecollideany(self.hero.sprite, self.walls) != None):
            ## Put the hero off screen
            hero.rect.topleft = ((-100,-100));
        self.hero.draw(self.screen);

        self.hero.draw(self.screen);        
        self.walls.draw(self.screen);

        done = False;
        while(not done):
            for event in self.getEvents():
                if(event.type == MOUSEBUTTONDOWN):
                    oldpos = self.hero.sprite.rect.topleft;
                    self.hero.clear(self.screen, self.background);
                    self.hero.sprite.rect.topleft = self.adjustposition(pygame.mouse.get_pos());
                    if(pygame.sprite.spritecollideany(self.hero.sprite, self.walls) != None):
                        self.hero.sprite.rect.topleft = oldpos
                    self.hero.draw(self.screen);
                    
                elif(event.type == KEYDOWN and event.key == K_s):
                    key = self.askQuestion(("Are you done?",
                                             "Y(es)    N(o)"), (K_y, K_n));

                    if(key == K_y):
                        key = self.askQuestion(("Do you want to save the map?",
                                                 "Y(es)    N(o)"), (K_y, K_n));
                        if(key == K_y):
                            self.map = self.askUserInput('Save as:');
                            self.saveMap();
                        done = True;
                        break;
                                  
            pygame.display.flip();
            self.clock.tick(50);
            

    def saveMap(self):
        """Saves positions of all object on a map."""
        self.map = "maps/"+self.map+".map";
        wall_rects = [];
        for wall in self.walls:
            wall_rects.append(wall.rect);
        badwall_rects = [];
        for wall in self.badwalls:
            badwall_rects.append(wall.rect);
            
        try:
            sFile = open(self.map, "w");
            try:
                cPickle.dump(self.hero.sprite.rect, sFile);
                cPickle.dump(wall_rects, sFile);
                cPickle.dump(badwall_rects, sFile);
            finally:
                sFile.close();
        except IOError:
            pass;


    def loadMap(self):
        """Load a Map from file.
           Returns self.walls, self.hero, self.badwalls"""
        try:
            lFile = open(self.map, "r");
            try:
                self.hero.sprite.rect = cPickle.load(lFile);
                wall_rects = cPickle.load(lFile);
                badwall_rects = cPickle.load(lFile); 
            finally:
                lFile.close();
        except IOError:
            print(str.format("Error: unable to open file {0}", self.map));
            sys.exit();

        self.walls.empty();
        for rect in wall_rects:
            wall = Wall(rect);
            self.walls.add(wall);

        self.badwalls.empty();
        for rect in badwall_rects:
            wall = Wall(rect);
            self.badwalls.add(wall);

    def askUserInput(self, question, transparent=255):
        """Ask a question and get user reply in text."""
        if(not isinstance(question, str)):
            raise TypeError('question is not a string');
        pygame.event.set_allowed((KEYDOWN, pygame.QUIT));
        scR = self.screen.get_rect();
        textQ = self.printText((question,),((0,0),(0,0)));

        textSurf = pygame.Surface((textQ[0][1].width+20, textQ[0][1].height*3));
        textSurf.set_alpha(transparent);
        
        surfRect = textSurf.get_rect();
        surfRect.center = scR.center;

        qRect = textQ[0][1];
        qRect.center = scR.center;
        qRect = qRect.move(0,-textQ[0][1].height);


        uInputStr = '';
        
        while(1):
            self.screen.fill((0,0,0));
            self.screen.blit(textSurf, surfRect);
            self.screen.blit(textQ[0][0], qRect);
            uInput = self.printText((uInputStr,),((0,0),(0,0)));
            uInputRect = uInput[0][1];
            uInputRect.center = scR.center;
            uInputRect.move(0,uInputRect.height);
            self.screen.blit(uInput[0][0], uInputRect);
            pygame.display.flip();
            event = pygame.event.wait();
            if(event.type == KEYDOWN):
                if(event.key == K_RETURN or event.key == K_KP_ENTER):
                    return(uInputStr);
                elif(event.key >= K_a and event.key <= K_z or
                     event.key >= K_0 and event.key <= K_9 or
                     event.key == K_SPACE or
                     event.key == K_PERIOD or
                     event.key == K_MINUS or
                     event.key == K_UNDERSCORE):
                    uInputStr += event.unicode;
                elif(event.key == K_BACKSPACE or event.key == K_DELETE):
                    uInputStr = uInputStr[0:-1];


    def adjustposition(self, position):
        """Adjusts the position."""
        return self.grid2pos(self.pos2grid(position));
    
    def pos2grid(self, position):
        """Calculates the grid coordinate from a position."""
        if(not isinstance(position, tuple)):
            raise TypeError("position is not of type tuple.");
        return (position[0]/self.objectsize, position[1]/self.objectsize);

    def grid2pos(self, grid):
        """Calculates the position coordinate from a grid."""
        if(not isinstance(grid, tuple)):
            raise TypeError("grid is not of type tuple.");
        return (grid[0]*self.objectsize, grid[1]*self.objectsize);

    def printInstructions(self):
        """Write the instructions."""
        self.screen.fill((0,0,0));
        self.printMessageWOption(("Logan is on the run.",
                           "He needs to find a way out.",
                           "Use up, down, left and right to guide him out.",
                           "Good luck!",""), "Instructions");

    def printMessageWOption(self, msg, title=None, align=Message.align_center, wait=True):
        if(not isinstance(msg, pygame.sprite.GroupSingle)):
           msg += ("Click on screen or", "press return to continue");
        msgSprite = self.printMessage(msg, title, align);
        if(wait == True):
            while(True):
                for event in self.getEvents():
                    if(event.type == MOUSEBUTTONDOWN or
                       (event.type == KEYDOWN and event.key == K_RETURN)):
                        msgSprite.clear(self.screen, self.background);
                        return
                self.clock.tick(50);

    def printMessage(self, msg, title=None, align=Message.align_center):
        pygame.event.set_allowed((KEYDOWN, pygame.QUIT, MOUSEBUTTONDOWN));
        if(not isinstance(msg, pygame.sprite.GroupSingle)):
            msgSprite = pygame.sprite.GroupSingle(
                Message(msg, title=title, align=align));
        else:
            msgSprite = msg;
        msgSprite.draw(self.screen);
        pygame.display.flip();
        return msgSprite;

    def printClock(self, seconds):
        """Creates a sprite with the minute and seconds types."""
        msgSprite = pygame.sprite.GroupSingle(
            Message((time.strftime("%M:%S", time.localtime(seconds)),)));
        msgSprite.sprite.rect.topleft = self.screen.get_rect().topleft;
        return msgSprite;
        
    def getEvents(self, exitKey = K_q, allowed = (KEYDOWN, pygame.QUIT, MOUSEBUTTONDOWN)):
        """Handles the normal options.
           Returns a list of events."""
        eventList = pygame.event.get();
        for event in eventList:
            if(event.type == pygame.QUIT):
                sys.exit();
            if(event.type == KEYDOWN and event.key == exitKey):
                sys.exit();
        return eventList;

    def askQuestion(self, msg, keyOptions):
        msgSprite = pygame.sprite.GroupSingle( Message(msg, align=Message.align_center));
        msgSprite.draw(self.screen);
        pygame.display.flip();
        done = False;
        while(not done):
            for event in self.getEvents():
                for key in keyOptions:
                    if(event.type == KEYDOWN and event.key == key):
                        msgSprite.clear(self.screen, self.background);
                        return key;

       
class GameLevel(object):
    """A game level class."""
    levels = "1. Expert", "2. Medium","3. Beginner";
    
    def __init__(self):
        self.number = 1;
        self.text = 'Expert';
        self.size = 100;

    def set(self, level):
        if(level == 1):
            self.number = 1;
            self.text = 'Expert';
            self.size = int(math.pow(self.number, 4) * 20);
        elif(level == 2):
            self.number = 2;
            self.text = 'Medium';
            self.size = int(math.pow(self.number, 4) * 10);
        elif(level == 3):
            self.number = 3;
            self.text = 'Beginner';
            self.size = pygame.display.get_surface().get_rect().width*2;

class Music(object):
    """ Plays selected audio files or picks a random file named music*.mp3."""
    def __init__(self):
        self.music = {};
        musicF = scriptutil.ffind('./audio', ('music*.mp3',));
        for mus in musicF:
            self.music[mus] = False;
        if len(self.music) == 0:
            print "No music found. Music disabled!";
            self.disabled = True;
        else:
            self.disabled = False;
        
    def playMusic(self, music=None):
        if self.disabled:
            return;
        if(music == None):
            while(True):
                music = self.music.keys();
                music = music[random.randrange(len(music))];
                if(self.music[music] == False):
                    self.music[music] = True;
                    break;
                free = False;
                for mu in self.music:
                    if(self.music[mu] == False):
                        free = True;
                        break;
                if(free == False): self.resetPlayed();
        try:
            pygame.mixer.music.load(music);
            pygame.mixer.music.play(-1);
        except:
            print(str.format("Error loading music:  {0}.", music));
            sys.exit();

    def resetPlayed(self):
        if self.disabled:
            return;
        for mus in self.music:
            self.music[mus] = False;
    
        
