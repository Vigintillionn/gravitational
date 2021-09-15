class LevelProp:
  def __init__(self, position):
    self.x = position[0]
    self.y = position[1]
  
  def get_position(self):
    return (self.x, self.y)

  def get_x(self):
    return self.x

  def get_y(self):
    return self.y

class Wall(LevelProp):
  def __init__(self, position):
    super().__init__(position)

class Spike(LevelProp):
  def __init__(self, position):
    super().__init__(position)

class Star(LevelProp):
  def __init__(self, position):
    super().__init__(position)

  


class Level:
  def __init__(self, walls, spikes, star, inventory, starting_pos = None, starting_vel = None):
    self.walls = self.load_walls(walls)
    self.spikes = self.load_spikes(spikes)
    self.star = Star(star)
    self.inventory = inventory or [20]
    self.starting_pos = starting_pos
    self.starting_vel = starting_vel

  def load_walls(self, walls):
    result = []
    for position in walls:
      w = Wall(position)
      result.append(w)
    return result

  def load_spikes(self, spikes):
    result = []
    for position in spikes:
      s = Spike(position)
      result.append(s)
    return result


def get_levels():
  levels = []
  levels.append( # Level 1
    Level(
      [], # Walls
      [], # Spikes
      (580 - 64, 420 - 64 - 61), # Star
      [60], # Inventory
    )
  )
  levels.append( # Level 2
    Level(
      [], # Walls
      [(320 -16, 64 + 100), (320 -16, 96 + 100)], # Spikes
      (580 - 64, 420 - 64 - 61), # Star
      [20, 60], # Inventory
    )
  )
  levels.append( # Level 3
    Level(
      [], # Walls
      [(320 -16, 0), (320 -16, 32), (320 -16, 64), (320 -16, 96)], # Spikes
      (580 - 64, 50), # Star
      [30, 60, 60], # Inventory
    )
  )
  levels.append( # Level 4
    Level(
      [], # Walls
      [(320 -16, 64 + 116), (320 -16 - 100, 64 + 116 - 50 + 75 + 48),
       (320 -16 + 100, 64 + 116 + 50 + 100 - 48), (320 -16 - 100, 64 + 116 - 50 - 100 + 48),
       (320 -16 + 100, 64 + 116 + 50 - 75 - 48)], # Spikes
      (580 - 64, 420 - 64 - 61), # Star
      [30, 30, 30, 30, 30], # Inventory
    )
  )
  levels.append( # Level 5
    Level(
      [], # Walls
      [(320 -16, 64 + 100), (320 -16, 96 + 100), (100, 100)], # Spikes
      (580 - 64, 420 - 64 - 61), # Star
      [20, 60], # Inventory
    )
  )
  levels.append( # Level 6
    Level(
      [], # Walls
      [(128 + 16, 0), (128 + 16, 32), (128 + 16, 64), (128 + 16, 96),
       (128 + 16, 128), (128 + 16, 160), (128 + 16, 192), (128 + 16, 222)], # Spikes
      (580 - 64, 50), # Star
      [20, 90], # Inventory
    )
  )
  levels.append(
    Level(
      [], # Walls
      [(60  + 100, 60 + (80)+ 60), (60  + 100, 60 - (80)+ 60), (60  + 150, 60 + (80)+ 90), 
       (60  + 150, 60 - (80)+ 90), (60  + 200, 60 + (80)+ 120), (60  + 200, 60 - (80)+ 120),
       (60  + 250, 60 + (80)+ 150), (60  + 250, 60 - (80) + 150), (60  + 300, 60 + (80)+ 180),
       (60  + 300, 60 - (80) + 180), (60  + 350, 60 + (80)+ 210), (60  + 350, 60 - (80) + 210),
       (60  + 400, 60 + (80)+ 240), (60  + 400, 60 - (80) + 240), (60  + 450, 60 + (80)+ 270),
       (60  + 450, 60 - (80) + 270), (60  + 500, 60 + (80)+ 300), (60  + 500, 60 - (80) + 300),
       (60  + 550, 60 + (80)+ 330), (60  + 550, 60 - (80) + 330)], # Spikes
      (60  + 550, 60 + 330), # Star
      [30, 30], # Inventory
    )
  )

  # levels.append( # Level 7   Buggy level - Need to fix
  #   Level(
  #     [(32*3, 128), (32*7, 128), (32*11, 128)], # Walls
  #     [(0, 128), (32, 128), (32*2, 128), (32*4, 128),
  #      (32*5, 128), (32*6, 128), (32*8, 128), (32*9, 128),
  #      (32*10, 128)], # Spikes
  #     (580 - 64, 420 - 64 - 61), # Star
  #     [90], # Inventory
  #   )
  # )

  return levels