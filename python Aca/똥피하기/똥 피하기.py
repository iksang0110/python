import pygame
import random
#########################################################
#기본 초기화 
pygame.init()

#화면 크기 설정
screen_width = 480 # 가로
screen_height = 640 # 세로  
screen = pygame.display.set_mode((screen_width, screen_height)) # 디스플레이 크기는 s_w s_h 값으로 설정한다

#화면 타이틀 설정
pygame.display.set_caption("똥 피하기") 

# FPS
clock = pygame.time.Clock()
##########################################################

# 1. 사용자 게임 초기화 (배경 화면, 게임 이미지, 좌표, 속도, 폰트)
background = pygame.image.load("/Users/02.011x/Documents/GitHub/21_study_group/18cm/Background.png")

character = pygame.image.load("/Users/02.011x/Documents/GitHub/21_study_group/18cm/character.png")
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width / 2) - (character_width / 2)
character_y_pos = screen_height - character_height


enemy = pygame.image.load("/Users/02.011x/Documents/GitHub/21_study_group/18cm/enemy.png")
enemy_size = enemy.get_rect().size
enemy_width = enemy_size[0]
enemy_height = enemy_size[0]
enemy_x_pos = random.randint(0,screen_width - enemy_width)
enemy_y_pos = 0

enemy2 = pygame.image.load("/Users/02.011x/Documents/GitHub/21_study_group/18cm/enemy.png")
enemy2_size = enemy.get_rect().size
enemy2_width = enemy_size[0]
enemy2_height = enemy_size[0]
enemy2_x_pos = random.randint(0,screen_width - enemy_width)
enemy2_y_pos = 0



# 이동할 좌표
to_x = 0

to_y = 0

# 캐릭터 속도
character_speed = 0.6

enemy_speed = 0.5

running = True # 게임 진행중인가
while running: 
    dt = clock.tick(30) # 게임화면의 초당 프레임 수를 설정

    # 2. 이벤트 처리 (키보드, 마우스 등)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            running = False 

        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_LEFT:
                to_x -= character_speed
            elif event.key == pygame.K_RIGHT:
                to_x += character_speed

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:            
                to_x = 0
    
        to_y = enemy_speed
        
            
    # 캐릭터 위치 정의
    
    character_x_pos += to_x * dt
    
    enemy_y_pos += to_y * dt

    enemy2_y_pos += to_y * dt

    # 가로 경계 처리
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    if enemy_y_pos > screen_height - enemy_height:
        enemy_y_pos = 0
        enemy_x_pos = random.randint(1, screen_width)

    if enemy2_y_pos > screen_height - enemy_height:
        enemy2_y_pos = 0
        enemy2_x_pos = random.randint(1, screen_width)
    
    # 4. 충돌 처리
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    enemy_rect = enemy.get_rect()
    enemy_rect.left = enemy_x_pos
    enemy_rect.top = enemy_y_pos

    enemy2_rect = enemy2.get_rect()
    enemy2_rect.left = enemy2_x_pos
    enemy2_rect.top = enemy2_y_pos

    if character_rect.colliderect(enemy_rect):
        print("게임 오버")
        running = False
        
    if character_rect.colliderect(enemy2_rect):
        print("게임 오버")
        running = False

    # 5. 화면에 그리기
    screen.blit(background, (0, 0))

    screen.blit(character, (character_x_pos, character_y_pos))

    screen.blit(enemy, (enemy_x_pos, enemy_y_pos))

    screen.blit(enemy2, (enemy2_x_pos, enemy2_y_pos))

    pygame.display.update() # 게임화면 다시 그리기*

pygame.quit()