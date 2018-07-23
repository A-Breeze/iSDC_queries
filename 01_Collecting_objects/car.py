import matplotlib.pyplot as plt
import weakref

""" The Car class defines a car's movement and keeps track of its state.

    The class includes init, move, and display functions.
    This class assumes a constant velocity motion model and the state
    of the car includes the car's position, and it's velocity.

    Attributes:
        state: A list of the car's current position [y, x] and velocity [vy, vx]
        world: The world that the car is moving within (a 2D list)
"""

class Car(object):
    
    all_the_cars = weakref.WeakValueDictionary() # Static attribute to keep track of cars
    
    def __init__(self, position, velocity, world, color = 'r'):
        """Initializes Car with some position, velocity, and a world to traverse."""
        # Initialise the attributes
        self.state = [position, velocity] # Position is a list [y, x] and so is velocity [vy, vx]
        self.world = world # world is a 2D list of values that range from 0-1
        self.color = color
        self.path = []
        self.path.append(position)
        
        # Additional code
        self.id = 'car_' + str(len(self.all_the_cars) + 1)
        self.all_the_cars[self.id] = self

    #def __del__(self):
    #    del self.all_the_cars[self.id]
    # Almost never a good idea to use __del__ 
    # as per: https://stackoverflow.com/questions/1481488/what-is-the-del-method-how-to-call-it
    
    def move(self, dt=1):
        """ The move function moves the car in the direction of the velocity and 
            updates the state.
            It assumes a circular world and a default dt = 1 (though dt can be any 
            non-negative integer).
            """
        height = len(self.world)
        width = len(self.world[0])
        position = self.state[0]
        velocity = self.state[1]

        # Predict the new position [y, x] based on velocity [vx, vy] and time, dt
        predicted_position = [
            (position[0] + velocity[0]*dt) % height, # default dt = 1
            (position[1] + velocity[1]*dt) % width
        ]
        self.state = [predicted_position, velocity] # Update the state
        self.path.append(predicted_position) # Every time the robot moves, add the new position to the path

    def turn_left(self):
        """ Turning left "rotates" the velocity values, so vy = -vx, and vx = vy.
        
            For example, if a car is going right at 1 world cell/sec this means 
            vy = 0, vx = 1, 
            and if it turns left, then it should be moving upwards on the world grid 
            at the same speed! 
            And up is vy = -1 and vx = 0
            """
        velocity = self.state[1] # Change the velocity
        predicted_velocity = [
            -velocity[1],
            velocity[0]
        ]
        self.state[1] = predicted_velocity # Update the state velocity
    
    def turn_right(self):
        """ Turning right "rotates" the velocity values, so vy = vx, and vx = -vy.
        
            For example, if a car is going right at 1 world cell/sec this means 
            vy = 0, vx = 1, 
            and if it turns right, then it should be moving downwards on the world grid 
            at the same speed! 
            And down is vy = 1 and vx = 0
            """
        velocity = self.state[1] # Change the velocity
        predicted_velocity = [
            velocity[1],
            -velocity[0]
        ]
        self.state[1] = predicted_velocity # Update the state velocity

    def display_world(self):
        """ 
        Helper function for displaying the world + robot position.
        Assumes the world in a 2D numpy array and position is in the form [y, x]
        path is a list of positions, and it's an optional argument.
        """
        position = self.state[0] # Store the current position of the car
        plt.matshow(self.world, cmap='gray') # Plot grid of values + initial ticks
        
        # Set minor axes in between the labels
        rows = len(self.world); cols = len(self.world[0])
        ax = plt.gca()
        ax.set_xticks([x-0.5 for x in range(1,cols)],minor=True )
        ax.set_yticks([y-0.5 for y in range(1,rows)],minor=True)
        plt.grid(which='minor',ls='-',lw=2, color='gray') # Plot grid on minor axes in gray (width = 2)

        # Create a 'x' character that represents the car
        # ha = horizontal alignment, va = verical
        ax.text(position[1], position[0], 'x', ha = 'center', va = 'center', color = self.color, fontsize = 30)
            
        # Draw path if it exists
        if(len(self.path) > 1):
            for pos in self.path: # loop through all path indices and draw a dot (unless it's at the car's location)
                if(pos != position):
                    ax.text(pos[1], pos[0], '.', ha = 'center', va = 'baseline', color = self.color, fontsize = 30)

        plt.show() # Display final result

    def __add__(self, other): # Overrides default function
        print('Adding two cars is an invalid operation!')
        return None

    
if __name__ == "__main__":
    import numpy as np
    
    world = np.zeros((4, 6))
    alan_car = Car([0, 0], [0, 1], world, 'm')
    bruce_car = Car([3, 3], [-2, 1], world, 'w')
    carla_car = Car([2, 4], [0, -1], world, 'r')
    
    # You can see that they all point to the same address
    print(Car.all_the_cars)
    print(alan_car.all_the_cars)
    print(bruce_car.all_the_cars)
    print(carla_car.all_the_cars)

    # Remove indivdual cars
    # Attempt 1
    del alan_car
    # Car.all_the_cars['car_1'] is gone
    print(dict(Car.all_the_cars))
    
    # Attempt 2
    print({key: item for key, item in Car.all_the_cars.items()})
    del bruce_car
    print(dict(Car.all_the_cars)) # Appears to work. But did not work in Jupyter notebook
    