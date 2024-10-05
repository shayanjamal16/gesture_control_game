import pygame
from sys import exit
from random import randint, choice, random
import cv2
import mediapipe as mp
import time
from directkeys import right_pressed, left_pressed, space_pressed

break_key_pressed = space_pressed
accelerato_key_pressed = right_pressed

time.sleep(2.0)
current_key_pressed = set()

mp_draw = mp.solutions.drawing_utils
mp_hand = mp.solutions.hands

tipIds = [4, 8, 12, 16, 20]

video = cv2.VideoCapture(0)

class Game:
    def gameInit(self):
        pygame.init()
        screen = pygame.display.set_mode((800, 400))
        # pygame.display.set_caption('Runner')

    def changeStateWhenActve(self):
        print("state changed when game Activ")

    def changeStateWhenNotActive(self):
        print("state changed when game not Active")

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0
        self.is_jumping = False
        self.jump_sound = pygame.mixer.Sound('./audio/jump.mp3')
        self.jump_sound.set_volume(0.5)

    def player_input(self, total):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_SPACE] or total == 5) and not self.is_jumping:
            self.is_jumping = True
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
            self.is_jumping = False

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self, total):
        self.player_input(total)
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == 'fly':
            fly_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210
        else:
            snail_1 = pygame.image.load('./graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('./graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

class Snail:
    def __init__(self):
        print("snail")

class Fly:
    def __init__(self):
        print("fly")


class GestureControl:
    def __init__(self):
        print("gesture control")

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'Score: {current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True

game = Game()
game.gameInit()
# pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('./audio/music.wav')
bg_music.play(loops=-1)

player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

sky_surface = pygame.image.load('graphics/sky.png').convert()
ground_surface = pygame.image.load('./graphics/ground.png').convert()

player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(400, 200))

game_name = test_font.render('Pixel Runner', False, (111, 196, 169))
game_name_rect = game_name.get_rect(center=(400, 80))

game_message = test_font.render('Welcome! To start game', False, (111, 196, 169))
game_message_rect = game_message.get_rect(center=(400, 330))

obstacle_timer = pygame.USEREVENT + 2 #1
pygame.time.set_timer(obstacle_timer, 2000) #1900

with mp_hand.Hands(min_detection_confidence=0.5,
                   min_tracking_confidence=0.5) as hands:

    while True:
        total = 0
        ret, image = video.read()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        lmList = []
        if results.multi_hand_landmarks:
            for hand_landmark in results.multi_hand_landmarks:
                myHands = results.multi_hand_landmarks[0]
                for id, lm in enumerate(myHands.landmark):
                    h, w, c = image.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append([id, cx, cy])
                mp_draw.draw_landmarks(image, hand_landmark, mp_hand.HAND_CONNECTIONS)
        fingers = []
        if len(lmList) != 0:
            if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
            for id in range(1, 5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            total = fingers.count(1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if game_active:
                if event.type == obstacle_timer:
                    obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))
            else:
                if total == 5:
                    game_active = True
                    start_time = int(pygame.time.get_ticks() / 1000)
        if game_active:
            game.changeStateWhenActve();
            screen.blit(sky_surface, (0, 0))
            screen.blit(ground_surface, (0, 300))
            score = display_score()
            player.draw(screen)
            player.update(total)
            obstacle_group.draw(screen)
            obstacle_group.update()
            game_active = collision_sprite()
        else:
            game.changeStateWhenNotActive()
            screen.fill((94, 129, 162))
            screen.blit(player_stand, player_stand_rect)
            score_message = test_font.render(f'Your score: {score}', False, (111, 196, 169))
            score_message_rect = score_message.get_rect(center=(400, 330))
            screen.blit(game_name, game_name_rect)
            if score == 0:
                screen.blit(game_message, game_message_rect)
            else:
                screen.blit(score_message, score_message_rect)
        pygame.display.update()
        clock.tick(60)
        cv2.imshow("Runner", image)
        k = cv2.waitKey(1)
        if k == ord('q'):
            break

input("Press Enter to exit...")