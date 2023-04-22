from pygame import *
from random import randint

WHITE = (225, 225, 225)

mixer.init()
mixer.music.load('musicfon.ogg')
mixer.music.play(-1)
fire_sound = mixer.Sound('fire.ogg')


font.init()
font2 = font.Font(None, 36)

all_sprites = sprite.Group()
lasers = sprite.Group()


img_back = "background.jpg"  
img_hero = "raketa.png" 
img_enemy = "nlo.png"    
   

score = 0  
lost = 0  


class GameSprite(sprite.Sprite):

    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)


        self.image = transform.scale(
            image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Laser(sprite.Sprite):

    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((10, 20))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
    def update(self):
        self.rect.y += self.speedy
        # убить, если он заходит за верхнюю часть экрана
        if self.rect.bottom < 0:
            self.kill()


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed


    def fire(self):
        bullet = Laser(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        lasers.add(bullet)
        



class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost

        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1


win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

win_sceen = Surface((700, 500))

ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)


monsters = sprite.Group()
for i in range(1, 16):  
    monster = Enemy(img_enemy, randint(
        80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

lose = font2.render("ВИ ПРОГРАЛИ!!!", 1, (225, 0, 0))
win = font2.render('ВИ ВИГРАЛИ!!!', 1, (0, 225, 0))

win_game = False
lose_game = False

run = True 


while run:

    keys = key.get_pressed()    

    for e in event.get():
        if e.type == QUIT:
            run = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                ship.fire()

    if not lose_game and not win_game : 
        window.blit(background, (0, 0))


        if sprite.groupcollide(monsters, all_sprites, True, True):    
            score +=1 
        text = font2.render("Рахунок: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))

        if sprite.spritecollide(ship, monsters, True):
            lose_game = True
            window.blit(lose, (10, 50))


        if lost >= 15:
            lose_game = True
            window.blit(win, (10, 50))
 
        if score == 14:
            win_game = True


        ship.update()
        monsters.update()
        all_sprites.update()
    
        ship.reset()
        all_sprites.draw(window)
        monsters.draw(window)
        display.update()


    elif not win_game and lose_game: 
        win_sceen.blit(lose, (250,250))   
        display.update()
    elif win_game and not lose_game:
        win_sceen.blit(win, (250,250))   
        display.update()
    time.delay(50)




     








