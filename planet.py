class Planet:
  def __init__(self, pos, image, radius):
    self.position = pos
    self.image = image
    self.radius = radius # Radius = radius pixels && "type"

  def get_mass(self):
    return self.mass

  def get_position(self):
    return self.position
  
  def get_radius(self):
    return self.radius

  def get_center_pos(self):
    return [self.position[0] + self.get_radius(), self.position[1] + self.get_radius()]