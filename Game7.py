'''
Function:
    크롬 공룡 게임
Author:
    Charles
'''
import cfg
import sys
import random
import pygame
from modules import *
from modules.sprites import dinosaur_2


'''main'''
def main(highest_score, second_score, third_score):
    # 게임초기화
    pygame.init()
    screen = pygame.display.set_mode(cfg.SCREENSIZE)
    pygame.display.set_caption('T-Rex Rush —— 오픈소스 2조')
    # 모든 소리파일 가져오기
    sounds = {}
    for key, value in cfg.AUDIO_PATHS.items():
        sounds[key] = pygame.mixer.Sound(value)
    # 게임 시작화면
    GameStartInterface(screen, sounds, cfg)
    # 게임에 필요한 요소와 변수들 정의
    score = 0
    score_board = Scoreboard(cfg.IMAGE_PATHS['numbers'], position=(534, 15), bg_color=cfg.BACKGROUND_COLOR)
    highest_score = highest_score
    second_score = second_score
    third_score = third_score
    highest_score_board = Scoreboard(cfg.IMAGE_PATHS['numbers'], position=(435, 15), bg_color=cfg.BACKGROUND_COLOR, is_highest=True)
    dino = Dinosaur(cfg.IMAGE_PATHS['dino'])
    dino_2 = dinosaur_2.Dinosaur_2(cfg.IMAGE_PATHS['dino_2'])
    ground = Ground(cfg.IMAGE_PATHS['ground'], position=(0, cfg.SCREENSIZE[1]))
    cloud_sprites_group = pygame.sprite.Group()
    cactus_sprites_group = pygame.sprite.Group()
    ptera_sprites_group = pygame.sprite.Group()
    apple_sprites_group = pygame.sprite.Group()
    add_obstacle_timer = 0
    score_timer = 0
    
    
    #음악구현(1)
    BGM = pygame.mixer.Sound("resources/audios/bgm.mp3")
    BGM_level2 = pygame.mixer.Sound("resources/audios/bgm_level2.mp3")
    BGM_level3 = pygame.mixer.Sound("resources/audios/bgm_level3.mp3")
    BGM_level4 = pygame.mixer.Sound("resources/audios/bgm_level4.mp3")
    BGM_level5 = pygame.mixer.Sound("resources/audios/bgm_level5.mp3")
    #구현 끝
    
    
    
    # 게임 루프
    setting_mode=-1
    print("Hello")
    while setting_mode == -1:
        pygame.display.set_caption('1인용은 s키를, 2인용은 m키를 눌러주세요.')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                print("0")

                if event.key == pygame.K_s:
                    setting_mode = 1
                    print("mode 1")
                    print(setting_mode)
                elif event.key == pygame.K_m:
                    setting_mode = 2
                    print("mode 2")
                    print(setting_mode)


    clock = pygame.time.Clock()
    pygame.display.set_caption('T-Rex Rush —— 오픈소스 2조')

    while setting_mode==1:
        if (score>=200):
            BGM.play(-1)
        if (score>=300):
            BGM.stop()
            BGM_level2.play(-1)
        if (score>=500):
            BGM_level2.stop()
            BGM_level3.play(-1)
        if (score>=1000):
            BGM_level3.stop()
            BGM_level4.play(-1)
        if (score>=1300):
            BGM_level4.stop()
            BGM_level5.play(-1) 
            
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    dino.jump(sounds)
                elif event.key == pygame.K_DOWN:
                    dino.duck()
            elif event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
                dino.unduck()
        screen.fill(cfg.BACKGROUND_COLOR)
        # --무작위 구름 추가
        if len(cloud_sprites_group) < 5 and random.randrange(0, 300) == 10:
            cloud_sprites_group.add(Cloud(cfg.IMAGE_PATHS['cloud'], position=(cfg.SCREENSIZE[0], random.randrange(30, 75))))
            cloud_sprites_group.add(Cloud(cfg.IMAGE_PATHS['cloud'], position=(cfg.SCREENSIZE[0], random.randrange(0, 35))))
        # --선인장/익룡 무작위 추가
        add_obstacle_timer += 1
        if add_obstacle_timer > random.randrange(60, 150):
            add_obstacle_timer = 0
            random_value = random.randrange(0, 11)
            #print(random_value)
            if random_value >= 7 and random_value <= 10:
                cactus_sprites_group.add(Cactus(cfg.IMAGE_PATHS['cacti']))
            elif random_value <= 5:
                position_ys = [cfg.SCREENSIZE[1]*0.80, cfg.SCREENSIZE[1]*0.65, cfg.SCREENSIZE[1]*0.60, cfg.SCREENSIZE[1]*0.20]
                ptera_sprites_group.add(Ptera(cfg.IMAGE_PATHS['ptera'], position=(900, random.choice(position_ys))))
            elif random_value == 6:
                position_ys = [cfg.SCREENSIZE[1]*0.60, cfg.SCREENSIZE[1]*0.60, cfg.SCREENSIZE[1]*0.40, cfg.SCREENSIZE[1]*0.10]
                apple_sprites_group.add(Apple(cfg.IMAGE_PATHS['apple'], position=(900, random.choice(position_ys))))
        # --게임 요소 업데이트
        dino.update()
        ground.update()
        apple_sprites_group.update()
        cloud_sprites_group.update()
        cactus_sprites_group.update()
        ptera_sprites_group.update()
        score_timer += 1
        if score_timer > (cfg.FPS//12):
            score_timer = 0
            score += 1
            score = min(score, 99999)
            if score > highest_score:
                third_score = second_score
                second_score = highest_score
                highest_score = score
            elif score > second_score:
                third_score = second_score
                second_score = score
            elif score > third_score:
                third_score = score
            if score % 100 == 0:
                sounds['point'].play()
            if (200<=score<300):
                ground.speed -= 0.3
                for item in cloud_sprites_group:
                    item.speed -= 3
                for item in cactus_sprites_group:
                    item.speed -= 0.1
                for item in ptera_sprites_group:
                    item.speed -= 0.1
                for item in apple_sprites_group:
                    item.speed-=0.1
            if (300<=score<500):
                ground.speed-=0.4
                for item in cloud_sprites_group:
                    item.speed-=4
                for item in cactus_sprites_group:
                    item.speed-=0.2
                for item in ptera_sprites_group:
                    item.speed-=0.2
                for item in apple_sprites_group:
                    item.speed-=0.3
            if (500<=score<1000):
                ground.speed-=0.5
                for item in cloud_sprites_group:
                    item.speed-=5
                for item in cactus_sprites_group:
                    item.speed-=0.4
                for item in ptera_sprites_group:
                    item.speed-=0.4
                for item in ptera_sprites_group:
                    item.speed-=0.5
            if (1000<=score<1300):
                ground.speed-=0.7
                for item in cloud_sprites_group:
                    item.speed-=7
                for item in cactus_sprites_group:
                    item.speed-=0.6
                for item in ptera_sprites_group:
                    item.speed-=0.6
                for item in ptera_sprites_group:
                    item.speed-=0.7
            if (1300<=score):
                ground.speed-=0.8
                for item in cloud_sprites_group:
                    item.speed-=0.9
                for item in cactus_sprites_group:
                    item.speed-=0.9
                for item in ptera_sprites_group:
                    item.speed-=0.9
                for item in ptera_sprites_group:
                    item.speed-=0.9
        # --충돌 체크
        for item in cactus_sprites_group:
            if pygame.sprite.collide_mask(dino, item):
                dino.die(sounds)
        for item in ptera_sprites_group:
            if pygame.sprite.collide_mask(dino, item):
                dino.die(sounds)
        for item in apple_sprites_group:
            if pygame.sprite.collide_mask(dino, item):
                score += 50
                apple_sprites_group.empty()
                
        # --게임 요소 화면에 그리기
        dino.draw(screen)
        ground.draw(screen)
        cloud_sprites_group.draw(screen)
        cactus_sprites_group.draw(screen)
        apple_sprites_group.draw(screen)
        ptera_sprites_group.draw(screen)
        score_board.set(score)
        highest_score_board.set(highest_score)
        score_board.draw(screen)
        highest_score_board.draw(screen)
        # --화면 업데이트
        pygame.display.update()
        clock.tick(cfg.FPS)
        # --게임 종료 여부 체크
        if dino.is_dead:
            BGM.stop()
            BGM_level2.stop()
            BGM_level3.stop()
            BGM_level4.stop()
            BGM_level5.stop()
            score_board.save_rankscore(score)
            break
    
    
    ###멀티
    while setting_mode==2:
        
        if (score>=200):
            BGM.play(-1)
        if (score>=300):
            BGM.stop()
            BGM_level2.play(-1)
        if (score>=500):
            BGM_level2.stop()
            BGM_level3.play(-1)
        if (score>=1000):
            BGM_level3.stop()
            BGM_level4.play(-1)
        if (score>=1300):
            BGM_level4.stop()
            BGM_level5.play(-1) 
            
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    dino_2.jump(sounds)
                elif event.key == pygame.K_DOWN:
                    dino_2.duck()
                if event.key == pygame.K_w:
                    dino.jump(sounds)
                elif event.key == pygame.K_s:
                    dino.duck()
            elif event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
                dino.unduck()
                dino_2.unduck()
        screen.fill(cfg.BACKGROUND_COLOR)
        # --무작위 구름 추가
        if len(cloud_sprites_group) < 5 and random.randrange(0, 300) == 10:
            cloud_sprites_group.add(Cloud(cfg.IMAGE_PATHS['cloud'], position=(cfg.SCREENSIZE[0], random.randrange(30, 75))))
            cloud_sprites_group.add(Cloud(cfg.IMAGE_PATHS['cloud'], position=(cfg.SCREENSIZE[0], random.randrange(0, 35))))
        # --선인장/익룡 무작위 추가
        add_obstacle_timer += 1
        if add_obstacle_timer > random.randrange(60, 150):
            add_obstacle_timer = 0
            random_value = random.randrange(0, 11)
            #print(random_value)
            if random_value >= 7 and random_value <= 10:
                cactus_sprites_group.add(Cactus(cfg.IMAGE_PATHS['cacti']))
            elif random_value <= 5:
                position_ys = [cfg.SCREENSIZE[1]*0.80, cfg.SCREENSIZE[1]*0.65, cfg.SCREENSIZE[1]*0.60, cfg.SCREENSIZE[1]*0.20]
                ptera_sprites_group.add(Ptera(cfg.IMAGE_PATHS['ptera'], position=(900, random.choice(position_ys))))
            elif random_value == 6:
                position_ys = [cfg.SCREENSIZE[1]*0.60, cfg.SCREENSIZE[1]*0.60, cfg.SCREENSIZE[1]*0.40, cfg.SCREENSIZE[1]*0.10]
                apple_sprites_group.add(Apple(cfg.IMAGE_PATHS['apple'], position=(900, random.choice(position_ys))))
        # --게임 요소 업데이트
        dino.update()
        dino_2.update()
        ground.update()
        apple_sprites_group.update()
        cloud_sprites_group.update()
        cactus_sprites_group.update()
        ptera_sprites_group.update()
        score_timer += 1
        if score_timer > (cfg.FPS//12):
            score_timer = 0
            score += 1
            score = min(score, 99999)
            if score > highest_score:
                third_score = second_score
                second_score = highest_score
                highest_score = score
            elif score > second_score:
                third_score = second_score
                second_score = score
            elif score > third_score:
                third_score = score
            if score % 100 == 0:
                sounds['point'].play()
            if (200<=score<300):
                ground.speed -= 0.3
                for item in cloud_sprites_group:
                    item.speed -= 3
                for item in cactus_sprites_group:
                    item.speed -= 0.1
                for item in ptera_sprites_group:
                    item.speed -= 0.1
                for item in apple_sprites_group:
                    item.speed-=0.1
            if (300<=score<500):
                ground.speed-=0.4
                for item in cloud_sprites_group:
                    item.speed-=4
                for item in cactus_sprites_group:
                    item.speed-=0.2
                for item in ptera_sprites_group:
                    item.speed-=0.2
                for item in apple_sprites_group:
                    item.speed-=0.3
            if (500<=score<1000):
                ground.speed-=0.5
                for item in cloud_sprites_group:
                    item.speed-=5
                for item in cactus_sprites_group:
                    item.speed-=0.4
                for item in ptera_sprites_group:
                    item.speed-=0.4
                for item in ptera_sprites_group:
                    item.speed-=0.5
            if (1000<=score<1300):
                ground.speed-=0.7
                for item in cloud_sprites_group:
                    item.speed-=7
                for item in cactus_sprites_group:
                    item.speed-=0.6
                for item in ptera_sprites_group:
                    item.speed-=0.6
                for item in ptera_sprites_group:
                    item.speed-=0.7
            if (1300<=score):
                ground.speed-=0.8
                for item in cloud_sprites_group:
                    item.speed-=0.9
                for item in cactus_sprites_group:
                    item.speed-=0.9
                for item in ptera_sprites_group:
                    item.speed-=0.9
                for item in ptera_sprites_group:
                    item.speed-=0.9
        # --충돌 체크
        for item in cactus_sprites_group:
            if pygame.sprite.collide_mask(dino, item):
                dino.die(sounds)
        for item in ptera_sprites_group:
            if pygame.sprite.collide_mask(dino, item):
                dino.die(sounds)
        for item in apple_sprites_group:
            if pygame.sprite.collide_mask(dino, item):
                score += 50
                apple_sprites_group.empty()
        
        # --충돌 체크(2)
        for item in cactus_sprites_group:
            if pygame.sprite.collide_mask(dino_2, item):
                dino_2.die(sounds)
        for item in ptera_sprites_group:
            if pygame.sprite.collide_mask(dino_2, item):
                dino_2.die(sounds)
        for item in apple_sprites_group:
            if pygame.sprite.collide_mask(dino_2, item):
                score += 50
                apple_sprites_group.empty()
                
        
                
        # --게임 요소 화면에 그리기
        dino.draw(screen)
        dino_2.draw(screen)
        ground.draw(screen)
        cloud_sprites_group.draw(screen)
        cactus_sprites_group.draw(screen)
        apple_sprites_group.draw(screen)
        ptera_sprites_group.draw(screen)
        score_board.set(score)
        highest_score_board.set(highest_score)
        score_board.draw(screen)
        highest_score_board.draw(screen)
        # --화면 업데이트
        pygame.display.update()
        clock.tick(cfg.FPS)
        # --게임 종료 여부 체크
        if dino.is_dead and dino_2.is_dead:
            BGM.stop()
            BGM_level2.stop()
            BGM_level3.stop()
            BGM_level4.stop()
            BGM_level5.stop()
            score_board.save_rankscore(score)
            break

    # 게임 종료 인터페이스
    return GameEndInterface(screen, cfg), highest_score, second_score, third_score


#최종 실행
if __name__ == '__main__':
    highest_score = 0
    second_score = 0
    third_score = 0
    attempt = 0
    while True:
        attempt += 1
        if attempt == 1:
            flag, highest_score, second_score, third_score = main(highest_score, 0, 0)
        elif attempt == 2:
            flag, highest_score, second_score, third_score = main(highest_score, second_score, 0)
        else:
            flag, highest_score, second_score, third_score = main(highest_score, second_score, third_score)
