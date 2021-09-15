import pygame
import time
from math import sqrt, floor
from copy import deepcopy
from os import path

from player import Player
from planet import Planet
from levels import get_levels
from images import images

WIDTH, HEIGHT = 640, 480
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.font.init()
FONT72 = pygame.font.Font(path.join("assets", "font", "font.otf"), 72)
FONT48 = pygame.font.Font(path.join("assets", "font", "font.otf"), 48)
FONT32 = pygame.font.Font(path.join("assets", "font", "font.otf"), 32)
FONT24 = pygame.font.Font(path.join("assets", "font", "font.otf"), 24)
pygame.mixer.init()

pygame.display.set_caption('Gravitational')
icon = pygame.image.load(path.join("assets", "planet_30.png"))
pygame.display.set_icon(icon)

FPS = 60

BG_COLOR = (30, 30, 30)
BAR_COLOR = (255, 255, 255)
BLACK = (0, 0, 0)

clock = pygame.time.Clock()
get_framerate = lambda: clock.get_fps()


def get_distance(obj1, obj2):
  return sqrt((obj2[0] - obj1[0]) * (obj2[0] - obj1[0]) + (obj2[1] - obj1[1]) * (obj2[1] - obj1[1]))


def get_mouse_pos():
  return pygame.mouse.get_pos()


def get_planet_image(t):
  if t == 20:
    return images.PLANET_PLUTO
  elif t == 30:
    return images.PLANET_MARS
  elif t == 60:
    return images.PLANET_EARTH
  if t == 90:
    return images.PLANET_BIGBOY

  
def get_button(t):
  if t == 20:
    return images.PLUTO_BUTTON
  elif t == 30:
    return images.MARS_BUTTON
  elif t == 60:
    return images.EARTH_BUTTON
  if t == 90:
    return images.BIGBOY_BUTTON


def draw_ui(selected_planet, inventory, curr_level, level_amm, deaths):
  pygame.draw.rect(WINDOW, BLACK, (0, 416, 640, 4))
  pygame.draw.rect(WINDOW, BAR_COLOR, (0, 420, 640, 60))

  mouse_x, mouse_y = get_mouse_pos()
  for i in range(len(inventory)):
    t = inventory[i]
    image = get_button(t).copy()
    x = 10 + (60 * i)
    y = 427

    if selected_planet == i:
      image.set_alpha(150)
    elif mouse_x <= x + 50 and mouse_x >= x and mouse_y >= y and mouse_y <= y + 50:
      image.set_alpha(200)

    WINDOW.blit(image, (x - 5, y - 5, 60, 60))
  ui_borders = images.UI_BORDERS
  ui_borders.set_alpha(200)
  WINDOW.blit(ui_borders, (0, 385))
  level = FONT24.render(f"Level: {curr_level + 1}/{level_amm}", False, (255, 255, 255))
  dths = FONT24.render(f"Deaths: {deaths}", False, (255, 255, 255))

  skip_btn = images.SKIP_BUTTON
  retry_btn = images.RETRY_BUTTON
  WINDOW.blit(level, (8, 387))
  WINDOW.blit(dths, (500, 387))
  WINDOW.blit(retry_btn, (560, 421))
  WINDOW.blit(skip_btn, (576, 451))

def draw_level(level):
  for wall in level.walls:
    WINDOW.blit(images.WALL, wall.get_position())

  for spike in level.spikes:
    WINDOW.blit(images.SPIKE, spike.get_position())

  WINDOW.blit(images.STAR, level.star.get_position())


def get_formatted_time(tme):
  ms = tme * 1000
  seconds = floor((ms / 1000) % 60)
  minutes = floor((ms / (1000 * 60)) % 60)

  milliseconds = int(floor((ms - (seconds * 1000) - (minutes * 60 * 1000)) * 100) / 100)
  return f"{minutes if len(str(minutes)) > 1 else f'0{minutes}'}:{seconds if len(str(seconds)) > 1 else f'0{seconds}'}.{milliseconds}"


def draw_window(
  space_man_pos, selected_planet, level, planets, inventory, curr_level, level_amm, deaths, start_time
):
  # Print background
  WINDOW.fill(BG_COLOR)

  t = time.time() - start_time
  dths = FONT72.render(f"{get_formatted_time(t)}", False, (20, 20, 20))
  WINDOW.blit(dths, (190, 20))

  # Check if use has a planet selected
  if selected_planet != None and selected_planet >= 0 and get_mouse_pos()[1] <= 415:
    planet = inventory[selected_planet]
    image = get_planet_image(planet).copy()
    image.set_alpha(128)
    WINDOW.blit(image, (get_mouse_pos()[0] - planet, get_mouse_pos()[1] - planet))

  # Place character
  WINDOW.blit(images.PLAYER, space_man_pos)

  draw_level(level)

  # Place planets
  for planet in planets:
    WINDOW.blit(planet.image, planet.get_position())

  draw_ui(selected_planet, inventory, curr_level, level_amm, deaths)
  pygame.display.update()


def play_sound(sound):
  pygame.mixer.music.load(path.join("assets", "sfx", f"{sound}.wav"))
  pygame.mixer.music.set_volume(0.2)
  pygame.mixer.music.play()


def handle_mouse_click(selected_planet, planets, inventory):
  mouse_x, mouse_y = get_mouse_pos()
  if mouse_y >= 451 and mouse_y <= 479 and mouse_x >= 576 and mouse_x <= 637:
    return "Skip"
  elif mouse_y >= 421 and mouse_y <= 449 and mouse_x >= 560 and mouse_x <= 621:
    return "Retry"
  elif mouse_y < 416:
    if selected_planet != None and selected_planet >= 0:
      selected_p = inventory[selected_planet]
      p = Planet((mouse_x - selected_p, mouse_y - selected_p), get_planet_image(selected_p), selected_p)
      planets.append(p)
      del inventory[selected_planet]
      play_sound("place")
      return -1
  else:
    for i in range(len(inventory)):
      x = 10 + (60 * i)
      y = 427
      if mouse_x <= x + 50 and mouse_x >= x and mouse_y >= y and mouse_y <= y + 50:
        index = x // 70
        play_sound("click")
        return index
    return selected_planet


def main():
  levels = get_levels()
  player = Player(images.PLAYER)
  selected_planet = -1
  curr_level = -1
  level = False
  load_next_level = False
  reset_level = False
  finished = False
  deaths = 0
  planets = []
  inventory = []

  start_time = time.time()
  end_time = 0

  started = False

  running = True
  while running:
    frame_time_in_seconds = clock.tick(FPS)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
      if event.type == pygame.MOUSEBUTTONUP:
        if not started:
          if finished:
            curr_level = -1
            level = False
          started = True
        elif finished:
          curr_level = -1
          level = False
          load_next_level = False
          reset_level = False
          finished = False
          deaths = 0
          end_time = 0
          start_time = time.time()
          started = False
        else:
          selected_planet = handle_mouse_click(selected_planet, planets, inventory)
          if selected_planet == "Skip":
            selected_planet = -1
            play_sound("win")
            load_next_level = True
          elif selected_planet == "Retry":
            selected_planet = -1
            play_sound("dead")
            deaths += 1
            reset_level = True
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_1:
          if len(inventory) >= 1:
            selected_planet = 0
        if event.key == pygame.K_2:
          if len(inventory) >= 2:
            selected_planet = 1
        if event.key == pygame.K_3:
          if len(inventory) >= 3:
            selected_planet = 2
        if event.key == pygame.K_4:
          if len(inventory) >= 4:
            selected_planet = 3
        if event.key == pygame.K_5:
          if len(inventory) >= 5:
            selected_planet = 4
        if event.key == pygame.K_s:
          selected_planet = -1
          play_sound("win")
          load_next_level = True
        if event.key == pygame.K_r:
          selected_planet = -1
          play_sound("dead")
          deaths += 1
          reset_level = True
    try:
      if not level or load_next_level or reset_level:
        if not level or load_next_level:
          curr_level += 1
        planets = []
        level = levels[curr_level]
        inventory = deepcopy(level.inventory)
        player.reset(level.starting_pos, level.starting_vel)
        load_next_level = False
        reset_level = False
    except IndexError:
      if not finished:
        end_time = time.time()
      finished = True
      started = False
    
    if started and not finished:
      force_x = 0
      force_y = 0
      for planet in planets:
        p_mass = planet.get_radius() * 0.0005

        distance = get_distance(player.get_center_pos(), planet.get_center_pos())
        if distance < planet.get_radius():
          play_sound("dead")
          deaths += 1
          reset_level = True
          break

        force_x += (p_mass * (planet.get_center_pos()[0] - player.get_center_pos()[0])) / distance
        force_y += (p_mass * (planet.get_center_pos()[1] - player.get_center_pos()[1])) / distance

      delta_time = frame_time_in_seconds / 1000 * 60
      player.set_velocity(player.velocity_x + force_x * delta_time, player.velocity_y + force_y * delta_time)
      player.update(delta_time, level.walls)

      for spike in level.spikes:
        if player.check_collision((spike.get_x(), spike.get_y(), 32, 32)):
          play_sound("dead")
          deaths += 1
          reset_level = True

      if player.check_collision((level.star.get_x(), level.star.get_y(), 32, 32)):
        play_sound("win")
        load_next_level = True


      draw_window(player.get_position(), selected_planet, level, planets, inventory, curr_level, len(levels), deaths, start_time)
    elif finished:
      WINDOW.fill(BG_COLOR)
      WINDOW.blit(images.END_SCREEN, (0, 0))

      header = FONT48.render("You found your home!", False, (8, 8, 8))
      sub = FONT32.render(f"After {deaths} deaths!", False, (0, 0, 0))
      tme = FONT32.render(f"Time: {get_formatted_time(end_time - start_time)}", False, (0, 0, 0))
      click = FONT32.render(f"Click twice to restart!", False, (0, 0, 0))
      WINDOW.blit(header, (WIDTH/2 - 348/2, HEIGHT/2 - 15 - 30))
      WINDOW.blit(sub, (WIDTH/2 -195/2 + 20, HEIGHT/2 -13 + 30))
      WINDOW.blit(tme, (WIDTH/2 -195/2 + 20, HEIGHT/2 -15 + 60))
      WINDOW.blit(click, (WIDTH/2 -278/2 + 20, HEIGHT/2 -15 + 90))
      pygame.display.update()
    else:
      WINDOW.fill(BG_COLOR)
      WINDOW.blit(images.LOGO, (0, 0))

      header = FONT32.render("Click anywhere to start!", False, (8, 8, 8))
      creds_barj = FONT24.render("Art by BARJI", False, (20, 20, 20))
      creds_vig = FONT24.render("Game by VIGINTILLION", False, (20, 20, 20))
      WINDOW.blit(header, (WIDTH/2 - 250/2, HEIGHT/2 - 15 + 50))
      WINDOW.blit(creds_barj, (WIDTH/2 - 100/2, HEIGHT/2 - 15 + 180))
      WINDOW.blit(creds_vig, (WIDTH/2 - 180/2, HEIGHT/2 - 15 + 210))
      pygame.display.update()
  pygame.quit()


if __name__ == "__main__":
  main()