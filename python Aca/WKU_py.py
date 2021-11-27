'''
import pygame #파이 게임 모듈 임포트
from random import randint
import sys
import time
from pygame.locals import QUIT,MOUSEBUTTONDOWN,KEYDOWN,K_SPACE

pygame.init() #파이 게임 초기화
WIDTH = 600
HEIGHT = 600
Large_Font = pygame.font.SysFont(None, 60)
Small_Font = pygame.font.SysFont(None, 36)
pygame.display.set_caption('두더지잡기')
SURFACE = pygame.display.set_mode((WIDTH, HEIGHT)) #화면 크기 설정
FPSCLOCK = pygame.time.Clock()

def main():
    Start_Time = int(time.time())
    GiveTime = 60
    Score = 0
    Miss = 0
    Game_Start = False
    Game_Over = False
    Start_image = pygame.image.load('FrontHaedal.png')
    End_image = pygame.image.load('BackHaedal.png')
    Sit_image = pygame.image.load('SitHaedal.png')
    Haedal = Sit_image.get_rect(left= randint(0,WIDTH - Sit_image.get_width()),top = randint(30,HEIGHT - Sit_image.get_height()))
    Start_Message = Small_Font.render("Game_Start : SpaceBar",True,(0,0,0))
    Over_Message = Large_Font.render("GAME_OVER",True,(0,0,0))
    while True: #게임 루프
        Score_Message = Small_Font.render("Score : {}".format(Score),True,(255,255,255))
        MissCount_Message = Small_Font.render("Miss : {}".format(Miss),True,(255,255,255))
        Score_End_Message = Large_Font.render("Total Score : {}".format(Score - Miss), True, (0, 0, 0))
        Time_Message = Small_Font.render("Time : {}".format(GiveTime), True, (255, 255, 255))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    Game_Start = True
            elif event.type == MOUSEBUTTONDOWN:
                if Game_Start:
                    if Haedal.collidepoint(event.pos):
                        Score += 1
                    else:
                        Miss += 1
                    Haedal = Sit_image.get_rect(left=randint(0, WIDTH - Sit_image.get_width()),
                                                top=randint(30, HEIGHT - Sit_image.get_height()))

        #게임이 시작되기전 대기 화면
        if Game_Start == False and Game_Over == False:
            Loading_Time = int(time.time())
            SURFACE.fill((255,255,255))
            SURFACE.blit(Start_image,(WIDTH/2 +100, HEIGHT/2))
            SURFACE.blit(Start_Message,(WIDTH/2-200,HEIGHT/2))

        #게임이 시작
        elif Game_Start == True and Game_Over == False:
            Current_Time = int(time.time())
            SURFACE.fill((0,0,0))
            SURFACE.blit(Sit_image,Haedal)
            SURFACE.blit(Score_Message,(15,15))
            SURFACE.blit(MissCount_Message, (WIDTH/2-30, 15))
            SURFACE.blit(Time_Message,(WIDTH-130,15))
            GiveTime = 60 - (Current_Time - Start_Time) + (Loading_Time - Start_Time)
            #제한 시간 오버
            if GiveTime <= 0:
                Game_Over = True
                Game_Start = False
                GiveTime = 0
        elif Game_Over ==True:
            SURFACE.fill((255,255,255))
            SURFACE.blit(Over_Message,(WIDTH/2-200,HEIGHT/2))
            SURFACE.blit(Score_End_Message, (WIDTH/2-150,HEIGHT/2-100))
            SURFACE.blit(End_image,(WIDTH/2 +100, HEIGHT/2))


        pygame.display.update()
        FPSCLOCK.tick(15)

if __name__ == '__main__':
    main()
'''

import pygame #파이 게임 모듈 임포트
import random
import time

pygame.init() #파이 게임 초기화
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #화면 크기 설정
clock = pygame.time.Clock() 

#변수

BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
large_font = pygame.font.SysFont('malgungothic', 72)
small_font = pygame.font.SysFont('malgungothic', 36)
score = 0
start_time = int(time.time()) #1970년 1월 1일 0시 0분 0초 부터 현제까지 초 
remain_second = 90
penalty_second = 0
game_over = False

mole_image = pygame.image.load('/Users/02.011x/Documents/GitHub/python/resources/mole.png')
mole_image = pygame.transform.scale(mole_image,(150,100))
moles = []
for i in range(2):
    mole = mole_image.get_rect(left=random.randint(0, SCREEN_WIDTH - mole_image.get_width()), top=random.randint(0, SCREEN_HEIGHT - mole_image.get_height()))
    after_second = random.randint(0, 3)
    during_second = random.randint(1, 3)
    appear_time = int(time.time()) + after_second
    disappear_time = int(time.time()) + after_second + during_second
    moles.append((mole, appear_time, disappear_time))



while True: #게임 루프
    screen.fill(BLACK) #단색으로 채워 화면 지우기

    #변수 업데이트

    event = pygame.event.poll() #이벤트 처리
    if event.type == pygame.QUIT:
        break
    elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
        print(event.pos[0], event.pos[1])
        for mole, appear_time, disappear_time in moles:
            if mole.collidepoint(event.pos):
                print(mole)
                moles.remove((mole, appear_time, disappear_time))
                mole = mole_image.get_rect(left=random.randint(0, SCREEN_WIDTH - mole_image.get_width()), top=random.randint(0, SCREEN_HEIGHT - mole_image.get_height()))
                after_second = random.randint(0, 3)
                during_second = random.randint(1, 3)
                appear_time = int(time.time()) + after_second
                disappear_time = int(time.time()) + after_second + during_second
                moles.append((mole, appear_time, disappear_time))
                score += 1
                

    if not game_over:       
        current_time = int(time.time())
        remain_second = 90 - (current_time - start_time) - penalty_second

        if remain_second <= 0:
            game_over = True
            for mole, appear_time, disappear_time in moles:
                current_time = int(time.time())
                if appear_time > current_time:  
                    moles.remove((mole, appear_time, disappear_time))
            pygame.mixer.music.stop()
         

        for mole, appear_time, disappear_time in moles:
            current_time = int(time.time())
            if current_time > disappear_time:  
                moles.remove((mole, appear_time, disappear_time))
                mole = mole_image.get_rect(left=random.randint(0, SCREEN_WIDTH - mole_image.get_width()), top=random.randint(0, SCREEN_HEIGHT - mole_image.get_height()))
                after_second = random.randint(0, 3)
                during_second = random.randint(1, 3)
                appear_time = int(time.time()) + after_second
                disappear_time = int(time.time()) + after_second + during_second
                moles.append((mole, appear_time, disappear_time))
                if remain_second >= 2:
                    penalty_second += 2

    #화면 그리기

    for mole, appear_time, disappear_time in moles:
        current_time = int(time.time())
        if  current_time >= appear_time:  
            screen.blit(mole_image, mole)

    score_image = small_font.render('점수 {}'.format(score), True, YELLOW)
    screen.blit(score_image, (10, 10))

    remain_second_image = small_font.render('남은 시간 {}'.format(remain_second), True, YELLOW)
    screen.blit(remain_second_image, remain_second_image.get_rect(right=SCREEN_WIDTH - 10, top=10))

    if game_over:
        game_over_image = large_font.render('게임 종료', True, RED)
        screen.blit(game_over_image, game_over_image.get_rect(centerx=SCREEN_WIDTH // 2, centery=SCREEN_HEIGHT // 2))

    pygame.display.update() #모든 화면 그리기 업데이트
    clock.tick(30) #30 FPS (초당 프레임 수) 를 위한 딜레이 추가, 딜레이 시간이 아닌 목표로 하는 FPS 값

pygame.quit()