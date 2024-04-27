from pygame import *
from random import randint
window = display.set_mode((700,500))
display.set_caption('shooter game')
background = transform.scale(image.load('galaxy.jpg'),(700,500))

class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x, player_y, speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(60,60))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.speed = speed
    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


bullets = sprite.Group()

#rocket creation
class Rocket(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x> 0:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 600:
           self.rect.x += self.speed
    def fire(self):
        sfaira = Bullet("bullet.png",self.rect.x,445,10)
        bullets.add(sfaira) 
         
#ufo creation
class UFO(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global missed
        if self.rect.y >= 500:
            self.rect.x = randint(0,650) 
            self.speed = randint(1,5)
            self.rect.y = 0
            missed +=1

#bullet creation
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed

        

#main music
mixer.init()
mixer.music.load("space.ogg")
# fonts
font.init()
font1 = font.Font(None,50)
lose = font1.render('You Lose!! (to play again press p)',1,(255,0,0))
win = font1.render("You Won!!",1,(255,255,51))

#rocket-ufos draw
rocket = Rocket('rocket.png',12,445,10)
ufos = sprite.Group()
for i in range(6):
    ufo1 = UFO("ufo.png",randint(0,650),100,3)
    ufos.add(ufo1)



FPS = 60
clock = time.Clock()
volume =  0.5
game = True
score = 0
missed = 0
finish = False
Pause1 = False
#game loop
while game:
   
    clock.tick(FPS)
    mixer.music.play()
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                rocket.fire()
    
    
    #when ufos colide bullets
    colide = sprite.groupcollide(ufos,bullets,True,True)
    for i in colide:
        score+=1
        ufo1 = UFO("ufo.png",randint(0,650),100,3)
        ufos.add(ufo1)
        
        
    if score >= 10:
        window.blit(win,(200,200))
        finish = True



    #game base
    if finish == False:
        window.blit(background,(0,0))
        rocket.draw()
        rocket.update()
        ufos.draw(window)
        ufos.update()
        bullets.draw(window)
        bullets.update()
    
    
    if sprite.spritecollide(rocket, ufos, False):
        finish = True
        window.blit(lose,(100,200))
        
    font.init()
    font1 = font.Font(None,36)
    keys_pressed = key.get_pressed()
    Pause = font1.render('Pause',1,(255,255,255))
    resume = font1.render("Resume",1,(255,255,255))
    #pause-resume-reset buttons
    if keys_pressed[K_ESCAPE]:
        finish = True  
        window.blit(Pause,(200,200))
    if keys_pressed[K_r]:
        finish = False
        window.blit(resume,(200,200))
    if keys_pressed[K_p]:
        finish = False
        score = 0
        missed = 0
        for ufo in ufos:
            ufo.rect.y = 0
            
    #volume buttons
    keys_pressed = key.get_pressed()
    if keys_pressed[K_u]  and volume < 1:
        volume += 0.01
        mixer.music.set_volume(volume)
        mixer.music.play()
        

    if keys_pressed[K_d] and volume > 0:
        volume -= 0.01 
        mixer.music.set_volume(volume)
        mixer.music.play()
        

    font.init()
    font1 = font.Font(None,36)
    #score
    score3 = font1.render("Score:"+ str(score),1,(255,255,255))
    window.blit(score3,(10,20))
    missed3 = font1.render("Missed:"+str(missed),1,(255,255,255)) 
    window.blit(missed3,(10,50))

    
    display.update()