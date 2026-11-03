class TrafficLight:
    def __init__(self):
        self.state = "RED"

    def change(self):
        if self.state == "RED":
            self.state = "GREEN"
        elif self.state == "GREEN":
            self.state = "ORANGE"
        else:
            self.state = "RED"