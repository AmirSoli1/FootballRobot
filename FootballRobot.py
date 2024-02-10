import math

class Goalkeeper:
    def __init__(self, FIELD_LENGTH, FIELD_WIDTH, ROBOT_RADIUS, BALL_RADIUS):
        self.field_length = FIELD_LENGTH
        self.field_width = FIELD_WIDTH
        self.robot_radius = ROBOT_RADIUS
        self.ball_radius = BALL_RADIUS
        self.goalkeeper_position = (0, self.field_width / 2)  # Initial position of the goalkeeper
        self.goalkeeper_angle = 0  # Initial angle of the goalkeeper

    def run_goalkeeper(self):
        while True:
            # Assume that the following functions are implemented
            ball_position = get_ball_position()
            teamate_position = get_teammate_position()
            
            # If the ball is close to the goal, move towards it
            if self.is_ball_close_to_goal(ball_position):
                self.move_towards_ball(ball_position)
                self.kick_ball(ball_position, teamate_position)
            else:
                # If the ball is far from the goal, position the goalkeeper in front of the goal
                self.position_goalkeeper()


    # This function calculates the angle between the goalkeeper and the target position
    def calculate_angle_to_target(self, target_position):
        goalkeeper_x, goalkeeper_y = self.goalkeeper_position
        target_x, target_y = target_position
        
        # Calculate the angle using trigonometry
        # source: https://www.mathsisfun.com/algebra/trig-finding-angle-right-triangle.html
        angle_radians = math.atan2(target_y - goalkeeper_y, target_x - goalkeeper_x)
        angle_degrees = math.degrees(angle_radians)
        
        return angle_degrees

    # This function rotates the goalkeeper to face the target angle
    def rotate_to_target(self, target_angle):
        
        current_angle = self.goalkeeper_angle
        degrees_to_rotate = current_angle - target_angle
        
        # Assume that the rotate functions are implemented
        if degrees_to_rotate < 0 and degrees_to_rotate > -180:
            rotate_left(math.abs(degrees_to_rotate))
        elif degrees_to_rotate < -180:
            rotate_right(360 + degrees_to_rotate)
        else:
            rotate_right(degrees_to_rotate)

    # This function is called when an object needs to move to a specific position (target_position)
    def move_to_position(self, current_position, target_position, is_goalkeeper = True):
        distance = math.sqrt((target_position[0] - current_position[0])**2 + (target_position[1] - current_position[1])**2)
        target_angle = self.calculate_angle_to_target(target_position)
        self.rotate_to_target(target_angle)

        # Assume that the move functions are implemented
        if is_goalkeeper:
            move_forward(distance - self.robot_radius - self.ball_radius)
        else:
            move_ball(distance - self.robot_radius)
           
    # This function checks if the ball is close to the goal
    def is_ball_close_to_goal(self, ball_position):
        goal_center = (0, self.field_width / 2)
        distance = math.sqrt((ball_position[0] - goal_center[0])**2 + (ball_position[1] - goal_center[1])**2)
        if distance < self.field_length / 4:
            return True
        else:
            return False
    

    #This function moves the goalkeeper towards the ball
    def move_towards_ball(self, ball_position):
        self.move_to_position(self.goalkeeper_position, ball_position)

    #This function kicks the ball towards the teammate
    def kick_ball(self,ball_position, teammate_position):
        self.move_to_position(ball_position, teammate_position, is_goalkeeper = False)

    #This function positions the goalkeeper in front of the goal
    def position_goalkeeper(self):
        goal_center = (0, self.field_width / 2)
        self.move_to_position(goal_center)
        self.rotate_to_target(0) # Rotate the goalkeeper to face the field
