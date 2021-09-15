from pygame import image
from os import path


def get_image(name):
  return image.load(path.join("assets", f"{name}.png"))


class images:
  PLAYER = get_image("player")
  PLANET_PLUTO = get_image("planet_20") # Pluto : R = 20
  PLANET_MARS = get_image("planet_30") # Mars : R = 30
  PLANET_EARTH = get_image("planet_60") # Earth : R = 60
  PLANET_BIGBOY = get_image("planet_90") # Big Boy : R = 90

  PLUTO_BUTTON = get_image("button_20") # End Screen
  MARS_BUTTON = get_image("button_30") # End Screen
  EARTH_BUTTON = get_image("button_60") # End Screen
  BIGBOY_BUTTON = get_image("button_90") # End Screen
  RETRY_BUTTON = get_image("retry_button")
  SKIP_BUTTON = get_image("skip_button")

  STAR = get_image("star") # Star
  WALL = get_image("wall") # Wall
  SPIKE = get_image("spike") # Spike

  END_SCREEN = get_image("endscreen") # End Screen
  UI_BORDERS = get_image("ui_borders") # UI Borders
  LOGO = get_image("logo") # Logo
