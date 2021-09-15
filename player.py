def check_collision(obj1, obj2):
  x1, y1, w1, h1 = obj1
  x2, y2, w2, h2 = obj2
  return x1 + w1 > x2 and x1 < x2 + w2 and y1 + h1 > y2 and y1 < y2 + h2;

class Player:
  def __init__(self, image):
    self.image = image
    self.x = 50
    self.y = 50
    self.velocity_x = 2
    self.velocity_y = 4

  def update(self, delta_time, walls):
    new_x = self.x + self.velocity_x * delta_time
    new_y = self.y + self.velocity_y * delta_time
    flip_x = False
    flip_y = False

    for wall in walls:
      wall_x, wall_y = wall.get_position()
      if check_collision((new_x, self.y, 24, 32), (wall_x, wall_y, 32, 32)):
        flip_x = True
      if check_collision((self.x, new_y, 24, 32), (wall_x, wall_y, 32, 32)):
        flip_y = True

    if new_x <= 0 or new_x + 24 >= 640 or flip_x:
      self.velocity_x *= -1
    
    if new_y <= 0 or new_y + 32 >= 416 or flip_y:
      self.velocity_y *= -1

    self.x = new_x
    self.y = new_y

  def set_velocity(self, velocity_x, velocity_y):
    self.velocity_x = velocity_x
    self.velocity_y = velocity_y

  def reset(self, position, velocity):
    if position:
      self.x = position[0]
      self.y = position[1]
    else:
      self.x = 50
      self.y = 50

    if velocity:
      self.velocity_x = velocity[0]
      self.velocity_y = velocity[1]
    else:
      self.velocity_x = 0
      self.velocity_y = 0

  def get_position(self):
    return (self.x, self.y)

  def get_center_pos(self):
    return [self.get_position()[0] + 12, self.get_position()[1] + 16]

  def check_collision(self, obj):
    x, y, w, h = obj
    return check_collision((self.x, self.y, 24, 32), (x, y, w, h))