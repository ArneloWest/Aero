import pygame
from sys import exit
from random import randint
from data.sprites import Player, Enemy, enemy_group, player_group, explosion_group
from data.settings import screen, clock, fps, start_time, score, last_shot, can_shoot, game_active


def display_score():
    curr_time = int(pygame.time.get_ticks() / 100) - start_time
    score_surf = font.render(f'{curr_time}', False, 'Black')
    score_rect = score_surf.get_rect(center=(240, 100))
    screen.blit(score_surf, score_rect)
    return curr_time


def collision():
    if pygame.sprite.spritecollide(player_group.sprite, enemy_group, False):
        enemy_group.empty()
        explosion_sound.play()
        return False
    else:
        return True


pygame.init()
pygame.display.set_caption("Aero")
font = pygame.font.Font('data/resources/font/Pixeltype.ttf', 50)
current_time = 0

# background
sky_surf = pygame.image.load('data/resources/graphics/sky/sky.png').convert()
sky_surf = pygame.transform.scale(sky_surf, (1100, 900))
cloud_surf = pygame.image.load('data/resources/graphics/sky/cloud.png').convert_alpha()
cloud_surf = pygame.transform.scale2x(cloud_surf)
cloud_rect = cloud_surf.get_rect(center=(randint(0, 480), -100))
cloud2_surf = pygame.image.load('data/resources/graphics/sky/cloud2.png').convert_alpha()
cloud2_surf = pygame.transform.scale2x(cloud2_surf)
cloud2_rect = cloud2_surf.get_rect(center=(randint(0, 480), -100))

# menu
title_surf = font.render('Aero', True, 'Black')
title_rect = title_surf.get_rect(center=(240, 50))

info_surf = font.render('SPACE TO START', True, 'Black')
info_rect = info_surf.get_rect(center=(240, 550))

controls_surf1 = font.render('Mouse - move left/right', True, 'Black')
controls_rect1 = controls_surf1.get_rect(center=(240, 650))
controls_surf2 = font.render('Mouse btn - shoot', True, 'Black')
controls_rect2 = controls_surf2.get_rect(center=(240, 700))

player_menu_surf = pygame.image.load('data/resources/graphics/sprites/player/player.png')
player_menu_surf = pygame.transform.scale2x(player_menu_surf)
player_menu_rect = player_menu_surf.get_rect(center=(240, 400))

# player
player_group.add(Player())
bullet_group = pygame.sprite.Group()

# timer
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 500)

difficulty_timer = pygame.USEREVENT + 2
pygame.time.set_timer(difficulty_timer, 5000)

# SFX
background_music = pygame.mixer.Sound('data/resources/audio/extremeaction.mp3')
propeller_sound = pygame.mixer.Sound('data/resources/audio/propeller.mp3')
reload_sound = pygame.mixer.Sound('data/resources/audio/reload.mp3')
explosion_sound = pygame.mixer.Sound('data/resources/audio/medium-explosion.mp3')

# SFX VOLUME
background_music.set_volume(0.01)
propeller_sound.set_volume(0.01)
reload_sound.set_volume(0.02)
explosion_sound.set_volume(0.02)


while True:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        # key binds
        if event.type == pygame.KEYDOWN and game_active == 0:
            if event.key == pygame.K_SPACE:
                background_music.play(loops=-1)
                propeller_sound.play(loops=-1)
                game_active = 1
                start_time = int(pygame.time.get_ticks() / 100)

        if game_active == 1:
            if event.type == enemy_timer:  # spawn enemy
                enemy_group.add(Enemy())

            if event.type == difficulty_timer:  # increase difficulty
                fps += 5

            if event.type == pygame.MOUSEBUTTONDOWN and can_shoot:  # shoot
                can_shoot = False
                bullet_group.add(Player().create_bullet())
                last_shot = pygame.time.get_ticks()

        # bullet timer
        current_time = pygame.time.get_ticks()
        if current_time - last_shot > 2000 and not can_shoot and game_active:
            reload_sound.play()
            can_shoot = True

    if game_active:

        mouse_motion = pygame.mouse.get_pos()
        pygame.mouse.set_visible(False)

        # background
        screen.blit(sky_surf, (0, 0))
        screen.blit(cloud_surf, cloud_rect)
        screen.blit(cloud2_surf, cloud2_rect)
        cloud_rect.y += 5
        if cloud_rect.y > 1000:
            cloud_rect.y = -100
            cloud_rect.x = randint(0, 480)

        cloud2_rect.y += 7
        if cloud2_rect.y > 1000:
            cloud2_rect.y = -100
            cloud2_rect.x = randint(0, 480)

        # player
        player_group.draw(screen)
        player_group.update()
        bullet_group.draw(screen)
        bullet_group.update()
        explosion_group.draw(screen)
        explosion_group.update()

        # enemy
        enemy_group.draw(screen)
        enemy_group.update()

        # collisions
        game_active = collision()

        # score
        score = display_score()

    else: # endgame
        propeller_sound.fadeout(0)
        background_music.fadeout(1000)
        enemy_group.empty()

        cloud_rect.y = cloud2_rect.y = -100
        pygame.mouse.set_visible(True)
        screen.fill(pygame.Color(167, 217, 252))

        end_score_surf = font.render(f'{score}', True, 'Black')
        end_score_rect = end_score_surf.get_rect(center=(240, 100))
        if score > 0:
            screen.blit(end_score_surf, end_score_rect)

        screen.blit(title_surf, title_rect)
        screen.blit(player_menu_surf, player_menu_rect)
        screen.blit(info_surf, info_rect)
        screen.blit(controls_surf1, controls_rect1)
        screen.blit(controls_surf2, controls_rect2)

    pygame.display.update()
    clock.tick(fps)
