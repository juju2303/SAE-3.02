from PyQt6.QtCore import QObject, QTimer, pyqtSignal
from traffic_light import TrafficLight
from vehicle import Vehicle


class Simulation(QObject):
    updated = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.running = False
        self.priority_vehicle = None
        self.vehicles = []
        self.next_id = 1
        self.north = TrafficLight()
        self.south = TrafficLight()
        self.east = TrafficLight()
        self.west = TrafficLight()
        self.north.state = "GREEN"
        self.south.state = "GREEN"
        self.east.state = "RED"
        self.west.state = "RED"
        self.light_timer = QTimer()
        self.light_timer.timeout.connect(self.change_lights)
        self.light_timer.start(4000)
        self.vehicle_timer = QTimer()
        self.vehicle_timer.timeout.connect(self.update_vehicles)

    def start(self):
        self.running = True
        self.vehicle_timer.start(50)
        self.updated.emit()

    def stop(self):
        self.running = False
        self.vehicle_timer.stop()
        self.updated.emit()

    def change_lights(self):
        if self.priority_vehicle is not None:
            if self.priority_vehicle in self.vehicles:
                self.set_priority_lights(self.priority_vehicle)
                self.updated.emit()
                return
            else:
                self.priority_vehicle = None
        if self.north.state == "GREEN":
            self.north.state = "ORANGE"
            self.south.state = "ORANGE"
        elif self.north.state == "ORANGE":
            self.north.state = "RED"
            self.south.state = "RED"
            self.east.state = "GREEN"
            self.west.state = "GREEN"
        elif self.east.state == "GREEN":
            self.east.state = "ORANGE"
            self.west.state = "ORANGE"
        else:
            self.east.state = "RED"
            self.west.state = "RED"
            self.north.state = "GREEN"
            self.south.state = "GREEN"
        self.updated.emit()

    def add_vehicle(self):
        vehicle = self.create_vehicle(priority=False)
        if not self.start_position_occupied(vehicle):
            self.vehicles.append(vehicle)
            self.updated.emit()
        return vehicle

    def add_priority_vehicle(self):
        vehicle = self.create_vehicle(priority=True)
        if not self.start_position_occupied(vehicle):
            self.vehicles.append(vehicle)
            self.priority_vehicle = vehicle
            self.set_priority_lights(vehicle)
            self.updated.emit()
        return vehicle

    def create_vehicle(self, priority=False):
        vehicle_id = self.next_id
        self.next_id += 1
        direction_number = ((vehicle_id - 1) % 4)
        if direction_number == 0:
            direction = "right"
            x = -30
            y = 230
        elif direction_number == 1:
            direction = "left"
            x = 805
            y = 205
        elif direction_number == 2:
            direction = "down"
            x = 375
            y = -30
        else:
            direction = "up"
            x = 410
            y = 465
        turn_number = vehicle_id % 3
        if turn_number == 0:
            turn = "straight"
        elif turn_number == 1:
            turn = "left"
        else:
            turn = "right"
        return Vehicle(vehicle_id,x,y,direction,priority,turn)

    def update_vehicles(self):
        for vehicle in list(self.vehicles):
            self.check_light_crossing(vehicle)
            if not vehicle.has_passed_light:
                if vehicle.priority:
                    can_move = True
                else:
                    if self.light_allows_vehicle(vehicle):
                        can_move = True
                    else:
                        can_move = self.can_move_to_light(vehicle)
            else:
                can_move = True
            if can_move:
                if self.would_collide(vehicle):
                    can_move = False
            if can_move:
                vehicle.move()
            self.check_light_crossing(vehicle)
            self.apply_turn(vehicle)
        self.remove_finished_vehicles()
        if self.priority_vehicle is not None:
            if self.priority_vehicle not in self.vehicles:
                self.priority_vehicle = None
        self.updated.emit()

    def light_allows_vehicle(self, vehicle):
        if vehicle.direction == "right":
            return self.west.state == "GREEN"
        elif vehicle.direction == "left":
            return self.east.state == "GREEN"
        elif vehicle.direction == "down":
            return self.north.state == "GREEN"
        elif vehicle.direction == "up":
            return self.south.state == "GREEN"
        return False

    def can_move_to_light(self, vehicle):
        stop_position = self.get_stop_position(vehicle)
        if stop_position is None:
            return False
        margin = 5
        if vehicle.direction == "right":
            return (vehicle.x + vehicle.speed < stop_position - margin)
        elif vehicle.direction == "left":
            return (vehicle.x - vehicle.speed > stop_position + margin)
        elif vehicle.direction == "down":
            return (vehicle.y + vehicle.speed < stop_position - margin)
        elif vehicle.direction == "up":
            return (vehicle.y - vehicle.speed > stop_position + margin)
        return False

    def get_stop_position(self, vehicle):
        if vehicle.direction == "right":
            return 295
        elif vehicle.direction == "left":
            return 460
        elif vehicle.direction == "down":
            return 145
        elif vehicle.direction == "up":
            return 275
        return None

    def check_light_crossing(self, vehicle):
        if vehicle.has_passed_light:
            return
        if vehicle.direction == "right":
            if vehicle.x >= 320:
                vehicle.has_passed_light = True
        elif vehicle.direction == "left":
            if vehicle.x <= 435:
                vehicle.has_passed_light = True
        elif vehicle.direction == "down":
            if vehicle.y >= 160:
                vehicle.has_passed_light = True
        elif vehicle.direction == "up":
            if vehicle.y <= 255:
                vehicle.has_passed_light = True

    def would_collide(self, vehicle):
        next_x = vehicle.x
        next_y = vehicle.y
        if vehicle.direction == "right":
            next_x += vehicle.speed
        elif vehicle.direction == "left":
            next_x -= vehicle.speed
        elif vehicle.direction == "down":
            next_y += vehicle.speed
        elif vehicle.direction == "up":
            next_y -= vehicle.speed
        width = 25
        height = 15
        left = next_x
        right = next_x + width
        top = next_y
        bottom = next_y + height
        for other in self.vehicles:
            if other == vehicle:
                continue
            other_left = other.x
            other_right = other.x + width
            other_top = other.y
            other_bottom = other.y + height
            collision = (left < other_right and right > other_left and top < other_bottom and bottom > other_top)
            if collision:
                return True
        return False

    def apply_turn(self, vehicle):
        if vehicle.has_turned:
            return
        if vehicle.direction == "right":
            if vehicle.x >= 390:
                if vehicle.turn == "left":
                    vehicle.direction = "up"
                    vehicle.x = 410
                    vehicle.y = 230
                elif vehicle.turn == "right":
                    vehicle.direction = "down"
                    vehicle.x = 375
                    vehicle.y = 230
                vehicle.has_turned = True
        elif vehicle.direction == "left":
            if vehicle.x <= 390:
                if vehicle.turn == "left":
                    vehicle.direction = "down"
                    vehicle.x = 375
                    vehicle.y = 205
                elif vehicle.turn == "right":
                    vehicle.direction = "up"
                    vehicle.x = 410
                    vehicle.y = 205
                vehicle.has_turned = True
        elif vehicle.direction == "down":
            if vehicle.y >= 205:
                if vehicle.turn == "left":
                    vehicle.direction = "left"
                    vehicle.x = 375
                    vehicle.y = 205
                elif vehicle.turn == "right":
                    vehicle.direction = "right"
                    vehicle.x = 375
                    vehicle.y = 230
                vehicle.has_turned = True
        elif vehicle.direction == "up":
            if vehicle.y <= 230:
                if vehicle.turn == "left":
                    vehicle.direction = "left"
                    vehicle.x = 410
                    vehicle.y = 205
                elif vehicle.turn == "right":
                    vehicle.direction = "right"
                    vehicle.x = 410
                    vehicle.y = 230
                vehicle.has_turned = True

    def set_priority_lights(self, vehicle):
        if vehicle.direction == "right":
            self.west.state = "GREEN"
            self.east.state = "RED"
            self.north.state = "RED"
            self.south.state = "RED"
        elif vehicle.direction == "left":
            self.east.state = "GREEN"
            self.west.state = "RED"
            self.north.state = "RED"
            self.south.state = "RED"
        elif vehicle.direction == "down":
            self.north.state = "GREEN"
            self.south.state = "RED"
            self.east.state = "RED"
            self.west.state = "RED"
        elif vehicle.direction == "up":
            self.south.state = "GREEN"
            self.north.state = "RED"
            self.east.state = "RED"
            self.west.state = "RED"

    def start_position_occupied(self, vehicle):
        for other in self.vehicles:
            horizontal_distance = abs(vehicle.x - other.x)
            vertical_distance = abs(vehicle.y - other.y)
            if (horizontal_distance < 35 and vertical_distance < 25):
                return True
        return False

    def remove_finished_vehicles(self):
        remaining = []
        for vehicle in self.vehicles:
            if (vehicle.x < -60 or vehicle.x > 860 or vehicle.y < -60 or vehicle.y > 520):
                continue
            remaining.append(vehicle)
        self.vehicles = remaining