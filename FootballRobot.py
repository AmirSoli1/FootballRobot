import math

class Goalkeeper:
    def __init__(self, FIELD_LENGTH, FIELD_WIDTH, ROBOT_RADIUS, BALL_RADIUS, TEAM):
        self.field_length = FIELD_LENGTH
        self.field_width = FIELD_WIDTH
        self.robot_radius = ROBOT_RADIUS
        self.ball_radius = BALL_RADIUS
        self.team = TEAM
        if self.team == "LEFT":
            self.goalkeeper_position = (self.robot_radius, self.field_width / 2)
            self.goalkeeper_angle = 0
        elif self.team == "RIGHT":
            self.goalkeeper_position = (self.field_length - self.robot_radius, self.field_width / 2)
            self.goalkeeper_angle = 180

    def run_goalkeeper(self):
        while True:
            # Assume that the following functions are implemented
            # The functions return the (x, y) position of the specified object
            ball_position = self.get_ball_position()
            teamate_position = self.get_teammate_position()
            
            # If the ball is close to the goal, move towards it
            if self.is_ball_close_to_goal(ball_position):
                self.move_towards_ball(ball_position)
                self.kick_ball(ball_position, teamate_position)
            else:
                # If the ball is far from the goal, position the goalkeeper in front of the goal
                self.position_goalkeeper()


    # This function calculates the angle between 2 positions
    def calculate_angle_to_target(self, current_position, target_position):
        current_x, current_y = current_position
        target_x, target_y = target_position
        
        # Calculate the angle using trigonometry
        # source: https://www.mathsisfun.com/algebra/trig-finding-angle-right-triangle.html
        angle_radians = math.atan2(target_y - current_y, target_x - current_x)
        angle_degrees = math.degrees(angle_radians)
        
        return angle_degrees

    # This function rotates the goalkeeper to face the target angle
    def rotate_to_target(self, target_angle):
        
        current_angle = self.goalkeeper_angle
        degrees_to_rotate = current_angle - target_angle
        
        # Assume that the rotate functions are implemented
        # The functions rotate the goalkeeper for the specified degress
        if degrees_to_rotate < 0 and degrees_to_rotate > -180:
            self.rotate_left(math.abs(degrees_to_rotate))
        elif degrees_to_rotate < -180:
            self.rotate_right(360 + degrees_to_rotate)
        else:
            self.rotate_right(degrees_to_rotate)

    def calculate_distance_to_target(self, current_position, target_position):
        current_x, current_y = current_position
        target_x, target_y = target_position
        distance = math.sqrt((target_x - current_x)**2 + (target_y - current_y)**2)
        return distance

    # This function is called when the goalkeeper needs to move to a specific position (target_position)
    def move_to_position(self, target_position):
        current_position = self.goalkeeper_position
        target_distance = self.calculate_distance_to_target(current_position, target_position)
        target_angle = self.calculate_angle_to_target(self.goalkeeper_position, target_position)
        self.rotate_to_target(target_angle)

        # Assume that the move_forward function is implemented
        # The function moves the goalkeeper forwards for the specified distance at a constant speed
        self.move_forward(target_distance)
           
    # This function checks if the ball is close to the goal
    def is_ball_close_to_goal(self, ball_position):
        goal_center = (0, self.field_width / 2)
        distance = self.calculate_distance_to_target(ball_position, goal_center)
        if distance < self.field_length / 4:
            return True
        else:
            return False
    
    # This function checks if the position is within the field bounds and corrects it if necessary
    def check_and_correct_position(self, position):
        x, y = position
        if x < 0:
            x = self.robot_radius
        elif x > self.field_length:
            x = self.field_length - self.robot_radius
        if y < 0:
            y = self.robot_radius
        elif y > self.field_width:
            y = self.field_width - self.robot_radius
        return (x, y)

    # This function moves the goalkeeper towards the ball
    def move_towards_ball(self, ball_position):
        if self.team == "LEFT": # Move to the left of the ball if possible and face it
            position = self.check_and_correct_position((ball_position[0] - self.ball_radius - self.robot_radius, ball_position[1]))
            self.move_to_position(position)
            self.rotate_to_target(0)

        elif self.team == "RIGHT": # Move to the right of the ball if possible and face it
            position = self.check_and_correct_position((ball_position[0] + self.ball_radius + self.robot_radius, ball_position[1]))
            self.move_to_position(position)
            self.rotate_to_target(180) 

    # This function kicks the ball towards the teammate
    def kick_ball(self, ball_position, teammate_position):
        distance = self.calculate_distance_to_target(ball_position, teammate_position)
        teamate_angle = self.calculate_angle_to_target(ball_position, (teammate_position[0] + self.ball_radius + self.robot_radius, teammate_position[1]))

        # Assume that the move_ball function is implemented
        # The function moves the ball for the specified distance towards the angle of the teammate at a constant speed
        self.move_ball(distance, teamate_angle)

    # This function positions the goalkeeper in front of the goal
    def position_goalkeeper(self):
        if self.team == "LEFT":
            goal_center = (self.robot_radius, self.field_width / 2)
        elif self.team == "RIGHT":
            goal_center = (self.field_length - self.robot_radius, self.field_width / 2)
        self.move_to_position(goal_center)
        self.rotate_to_target(0) # Rotate the goalkeeper to face the field
