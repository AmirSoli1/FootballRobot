import math

class Goalkeeper:
    def __init__(self, FIELD_LENGTH, FIELD_WIDTH, GOAL_LENGTH, GOAL_WIDTH, ROBOT_RADIUS, BALL_RADIUS):
        self.field_length = FIELD_LENGTH
        self.field_width = FIELD_WIDTH
        self.goal_length = GOAL_LENGTH
        self.goal_width = GOAL_WIDTH
        self.robot_radius = ROBOT_RADIUS
        self.ball_radius = BALL_RADIUS
        self.goalkeeper_position = (0, self.field_width / 2)  # Initial position of the goalkeeper
        self.goalkeeper_angle = 0  # Initial angle of the goalkeeper


    # This function calculates the angle between the goalkeeper and the target position
    def calculate_angle_to_target(self, target_position):
        goalkeeper_x, goalkeeper_y = self.goalkeeper_position
        target_x, target_y = target_position
        
        # Calculate the angle using trigonometry
        # source: https://www.mathsisfun.com/algebra/trig-finding-angle-right-triangle.html
        angle_radians = math.atan((target_y - goalkeeper_y) / (target_x - goalkeeper_x))
        angle_degrees = math.degrees(angle_radians)
        
        return angle_degrees

    # This function rotates the goalkeeper to face the target angle
    def rotate_to_target(self, target_angle):
        
        current_angle = self.goalkeeper_angle
        degrees_to_rotate = current_angle - target_angle
        
        if degrees_to_rotate < 0 and degrees_to_rotate > -180:
            rotate_left(math.abs(degrees_to_rotate))
        elif degrees_to_rotate < -180:
            rotate_right(360 + degrees_to_rotate)
        else:
            rotate_right(degrees_to_rotate)

    # This function is called when the goalkeeper needs to move to a specific position (target_position)
    def move_to_position(self, target_position):
        current_position = self.goalkeeper_position
        distance_to_target = math.sqrt((target_position[0] - current_position[0])**2 + (target_position[1] - current_position[1])**2)

        target_angle = self.calculate_angle_to_target(target_position)
        self.rotate_to_target(target_angle)
        
        while distance_to_target > 0:
            move_forward()
            current_position = self.goalkeeper_position
            distance_to_target = math.sqrt((target_position[0] - current_position[0])**2 + (target_position[1] - current_position[1])**2)

