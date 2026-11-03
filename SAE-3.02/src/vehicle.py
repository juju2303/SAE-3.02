class Vehicle:
    def __init__(self,vehicle_id,x,y,direction,priority=False,turn="straight"):
        self.id = vehicle_id
        self.x = x
        self.y = y
        self.direction = direction
        self.priority = priority
        self.turn = turn
        self.speed = 3
        self.has_passed_light = False
        self.has_turned = False

    def move(self):
        if self.direction == "right":
            self.x += self.speed
        elif self.direction == "left":
            self.x -= self.speed
        elif self.direction == "down":
            self.y += self.speed
        elif self.direction == "up":
            self.y -= self.speed