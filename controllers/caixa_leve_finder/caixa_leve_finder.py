import os
import random
from controller import Robot, Motor, DistanceSensor, LED

DISTANCE_SENSORS_NUMBER = 8
distance_sensors_names = ["ps0", "ps1", "ps2", "ps3", "ps4", "ps5", "ps6", "ps7"]
distance_sensors = []

LEDS_NUMBER = 10
leds_names = ["led0", "led1", "led2", "led3", "led4", "led5", "led6", "led7", "led8", "led9"]
leds = []

MAX_SPEED = 6.28
LEFT = 0
RIGHT = 1

robot = Robot()

timestep = int(robot.getBasicTimeStep())

def init_devices():
    global left_motor, right_motor
    for i in range(DISTANCE_SENSORS_NUMBER):
        distance_sensors.append(robot.getDevice(distance_sensors_names[i]))
        distance_sensors[i].enable(timestep)
    
    for i in range(LEDS_NUMBER):
        leds.append(robot.getDevice(leds_names[i]))
    
    left_motor = robot.getDevice("left wheel motor")
    right_motor = robot.getDevice("right wheel motor")
    left_motor.setPosition(float('inf'))
    right_motor.setPosition(float('inf'))
    left_motor.setVelocity(0.0)
    right_motor.setVelocity(0.0)

def step():
    if robot.step(timestep) == -1:
        exit()

def random_turn():
    turn_duration = random.uniform(0.5, 2.0) 
    turn_speed = MAX_SPEED * random.choice([-0.5, 0.5])  
    start_time = robot.getTime()
    while robot.getTime() - start_time < turn_duration:
        left_motor.setVelocity(turn_speed)
        right_motor.setVelocity(-turn_speed)
        step()

def main():
    print("E-puck iniciado com sucesso...")
    init_devices()

    # Caso não funcione alterar o file_path abaixo para do seu computador
    file_path = "C:/tmp/caixa_movida.txt"
    if os.path.exists(file_path):
        os.remove(file_path)

    move_counter = 0  

    while True:
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                message = f.read()
                if "Caixa leve encontrada" in message:
                    left_motor.setVelocity(0)
                    right_motor.setVelocity(0)
                    leds[0].set(1)
                    print("Caixa leve foi encontrada e movida!")
                    break

        ps_values = [sensor.getValue() for sensor in distance_sensors]
        right_obstacle = ps_values[0] > 80.0 or ps_values[1] > 80.0 or ps_values[2] > 80.0
        left_obstacle = ps_values[5] > 80.0 or ps_values[6] > 80.0 or ps_values[7] > 80.0

        left_speed = MAX_SPEED * 0.5
        right_speed = MAX_SPEED * 0.5

        if left_obstacle:
            left_speed += MAX_SPEED * 0.5
            right_speed -= MAX_SPEED * 0.5
        elif right_obstacle:
            left_speed -= MAX_SPEED * 0.5
            right_speed += MAX_SPEED * 0.5

        left_motor.setVelocity(left_speed)
        right_motor.setVelocity(right_speed)

        move_counter += 1
        if move_counter > 200:  # A cada 200 ciclos
            random_turn()
            move_counter = 0

        step()

if __name__ == "__main__":
    main()