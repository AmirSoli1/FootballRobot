'''
This implementaion of the goalkeeper works under the assumption that the following functions are implemented:
get_teammate_position() - returns the (x, y) position of the teammate
get_teammate_message() - returns True if the teammate is asking the goalkeeper to intervene, and False otherwise
get_ball_position() - returns the (x, y) position of the ball
move_forward(distance) - moves the robot forward the specified distance at a constant speed
rotate_left(degress) - rotates the robbot left for the specified degrees
rotate_right(degrees) - rotates the robbot right for the specified degrees
move_ball(distance, angle) - moves the ball to the specified angle for the specified distance at a constant speed
'''

import math
import time

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
            time.sleep(0.001)
            # Assume that the following functions are implemented
            # The functions return the (x, y) position of the specified object
            teamate_position = get_teammate_position()
            ball_position = get_ball_position()

            # Assume that the following function is implemented
            # The function returns True if the teammate is sending a message asking for help
            is_teammate_asking_for_help = get_teammate_message()
            
            # If the ball is in the danger zone and the teammate is asking for help, move towards the ball and kick it
            if self.is_ball_in_danger_zone(ball_position) and is_teammate_asking_for_help:
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

    # **This function is called only when the target is inside the goalkeeper's forward laser
    # The function calculates the distance between goalkeeper and the target
    def forward_laser(self, current_position, target_position):
        current_x, current_y = current_position
        target_x, target_y = target_position
        distance = math.sqrt((target_x - current_x)**2 + (target_y - current_y)**2)
        return distance

    # This function is called when the goalkeeper needs to move to a specific position (target_position)
    def move_to_position(self, target_position):
        current_position = self.goalkeeper_position
        target_angle = self.calculate_angle_to_target(self.goalkeeper_position, target_position)

        self.rotate_to_target(target_angle) # rotate to the target so the robot can use the forward laser
        target_distance = self.forward_laser(current_position, target_position)

        # Assume that the move_forward function is implemented
        # The function moves the goalkeeper forwards for the specified distance at a constant speed
        self.move_forward(target_distance)
           
    # This function checks if the ball is close to the goal
    # By default the danger zone is 1/4 of the field length
    def is_ball_in_danger_zone(self, ball_position, relative_danger=4):
        danger_zone = self.field_length / relative_danger
        return ball_position[0] < danger_zone
    
    # This function checks if the position is within the field bounds and corrects it if necessary
    def check_and_correct_position(self, position, ball_position):
        #**Add/Subtract the radiuses so the goalkeeper doesn't stand on the ball
        x, y = position
        if x < 0:
            x = ball_position[0] + self.ball_radius + self.robot_radius
        elif x > self.field_length:
            x = ball_position[0] - self.ball_radius - self.robot_radius
        if y - self.robot_radius < 0:
            y = ball_position[1] + self.ball_radius + self.robot_radius
        elif y + self.robot_radius > self.field_width:
            y = ball_position[1] - self.ball_radius - self.robot_radius
        return (x, y)

    # This function moves the goalkeeper towards the ball
    def move_towards_ball(self, ball_position):
        # Move to the left or right of the ball (depends on team), check for bounds and correct them if neccesary
        # **Add/Subtract the radiuses so the goalkeeper doesn't stand on the ball
        if self.team == "LEFT": 
            position = self.check_and_correct_position((ball_position[0] - self.ball_radius - self.robot_radius, ball_position[1]),
                                                       ball_position)
            self.move_to_position(position)
            self.rotate_to_target(0)

        elif self.team == "RIGHT": # Move to the right of the ball if possible and face it
            position = self.check_and_correct_position((ball_position[0] + self.ball_radius + self.robot_radius, ball_position[1]),
                                                       ball_position)
            self.move_to_position(position)
            self.rotate_to_target(180) 

    # This function kicks the ball towards the teammate
    def kick_ball(self, ball_position, teammate_position):
        # Kick the ball to the right or left of the teammate (depends on team)
        # add/subtract the radiuses so the ball ends up in front of the teammate
        if self.team == "LEFT":
            teamate_angle = self.calculate_angle_to_target(ball_position, (teammate_position[0] + self.ball_radius + self.robot_radius,
                                                                       teammate_position[1]))
        elif self.team == "RIGHT":
            teamate_angle = self.calculate_angle_to_target(ball_position, (teammate_position[0] - self.ball_radius - self.robot_radius,
                                                                       teammate_position[1]))
        # Rotate to the target so the robot can use the forward laser
        self.rotate_to_target(teamate_angle) 
        # Calculate the distance between the ball and the teammate
        distance = self.forward_laser(self.goalkeeper_position + self.robot_radius + self.ball_radius, teammate_position)

        # Assume that the move_ball function is implemented
        # The function moves the ball for the specified distance towards the angle of the teammate at a constant speed
        move_ball(distance, teamate_angle)

    # This function positions the goalkeeper in front of the goal
    def position_goalkeeper(self):
        # Calculate the center of the goal depending on the team
        if self.team == "LEFT":
            goal_center = (self.robot_radius, self.field_width / 2)
        elif self.team == "RIGHT":
            goal_center = (self.field_length - self.robot_radius, self.field_width / 2)

        self.move_to_position(goal_center)

        # Rotate the goalkeeper to face the field
        if self.team == "LEFT":
            goal_center = self.rotate_to_target(0)
        elif self.team == "RIGHT":
            goal_center = self.rotate_to_target(180)