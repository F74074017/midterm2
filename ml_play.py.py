"""
The template of the script for the machine learning process in game pingpong
"""

# Import the necessary modules and classes
from mlgame.communication import ml as comm

def ml_loop(side: str):
    """
    The main loop for the machine learning process

    The `side` parameter can be used for switch the code for either of both sides,
    so you can write the code for both sides in the same script. Such as:
    ```python
    if side == "1P":
        ml_loop_for_1P()
    else:
        ml_loop_for_2P()
    ```

    @param side The side which this script is executed for. Either "1P" or "2P".
    """

    # === Here is the execution order of the loop === #
    # 1. Put the initialization code here
    ball_served = False
    result = []
    # 2. Inform the game process that ml process is ready
    comm.ml_ready()
    blocker_speed = 3
    last_blocker_pos = [85]
    # 3. Start an endless loop
    while True:
        # 3.1. Receive the scene information sent from the game process
        scene_info = comm.recv_from_game()

        # 3.2. If either of two sides wins the game, do the updating or
        #      resetting stuff and inform the game process when the ml process
        #      is ready.
        if scene_info["status"] != "GAME_ALIVE":
            result.append(scene_info['frame'])
            # Do some updating or resetting stuff
            ball_served = False
            # 3.2.1 Inform the game process that
            #       the ml process is ready for the next round
            comm.ml_ready()
            sum = 0
            for i in result:
                sum += i
            print(sum / len(result))
            continue

        # 3.3 Put the code here to handle the scene information

        # 3.4 Send the instruction for this frame to the game process
        #print(scene_info)

        
        blocker_speed = scene_info['blocker'][0] - last_blocker_pos[0]
        #print(scene_info['blocker'])
        #print(blocker_speed)
        if side == "1P":
            ml_loop_for_1P(scene_info, blocker_speed)
        else:
            ml_loop_for_2P(scene_info, blocker_speed)
        last_blocker_pos = scene_info["blocker"]
        


def ml_loop_for_1P(scene_info, blocker_speed):
    if(blocker_speed > 0):
        blocker_speed = 3
    else:
        blocker_speed = -3
    check_position1 = []
    check_position1 = calculate_ball_position_platform1(scene_info, blocker_speed)
    '''
    if(420 - scene_info['ball'][1] <= scene_info['ball_speed'][1]):
        if(scene_info['blocker'][0] > 130):
            comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_LEFT"})
        elif(scene_info['blocker'][0] < 30):
            comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_RIGHT"})
        elif(blocker_speed > 0):
            comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_RIGHT"})
        else:
            comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_LEFT"})
    '''
    if(check_position1[0] - 25 > scene_info["platform_1P"][0]):
        comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_RIGHT"})
    elif(check_position1[0] - 25  < scene_info["platform_1P"][0] ):
        comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_LEFT"})
def ml_loop_for_2P(scene_info, blocker_speed):
    if(blocker_speed > 0):
        blocker_speed = 3
    else:
        blocker_speed = -3
    check_position2 = []
    check_position2 = calculate_ball_position_platform2(scene_info, blocker_speed)    
    '''
    if(scene_info['ball'][1] - 80 <= scene_info['ball_speed'][1]):
        if(scene_info['blocker'][0] > 100):
            comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_LEFT"})
        else:
            comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_RIGHT"})
    '''
    if(check_position2[0] - 25 > scene_info["platform_2P"][0]):
        comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_RIGHT"})
    elif(check_position2[0] - 25  < scene_info["platform_2P"][0] ):
        comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_LEFT"})        
        
def calculate_ball_position_platform2(scene_info, blocker_speed):
    if(scene_info["ball_speed"][1] == 0):
        return scene_info["ball"]
    x = scene_info["ball"][0]
    y = scene_info["ball"][1]
    ball_speed = list(scene_info["ball_speed"])
    frame = scene_info['frame']
    blocker = list(scene_info['blocker'])
    while(y > 80):
        blocker[0] += blocker_speed
        if(blocker[0] > 160):
            blocker[0] = 160
            blocker_speed *= -1
        elif(blocker[0] < 0):
            blocker[0] = 0
            blocker_speed *= -1
        if((frame) -  150 % 200 == 0):
            if(ball_speed[0] > 0):
                ball_speed[0] += 1
            else:
                ball_speed[0] -= 1
            if(ball_speed[1] > 0):
                ball_speed[1] += 1
            else:
                ball_speed[1] -= 1
        frame += 1
        if(x <= blocker[0] + 25 and x >= blocker[0] - 5 and y <= blocker[1] + 15 and y >= blocker[1] - 5):
                gap1 = x - blocker[0]
                gap2 = blocker[0] + 30 - x
                gap3 = y - blocker[1]
                gap4 = blocker[1] + 20 - y
                
                f_gap = min([gap1, gap2, gap3, gap4])
                if(f_gap == gap1):
                    #x = blocker[0] - 5
                    y = blocker[1] - 5
                    ball_speed[0] *= -1
                elif(f_gap == gap2):
                    #x = blocker[0] + 35
                    y = blocker[1] - 5
                    ball_speed[0] *= -1
                elif(f_gap == gap3):
                    y = blocker[1] - 5
                    ball_speed[1] *= -1
                else:
                    y = blocker[1] + 20
                    ball_speed[1] *= -1
                
                
                
                '''
                if(y-ball_speed[1] <= blocker[1]):
                    ball_speed[1] *= -1
                    y = blocker[1]
                elif(gap1 > gap2  and y-ball_speed[1] <= blocker[1] + 30):
                    x = blocker[0] + 40
                    ball_speed[0] *= -1
                elif(gap2 >= gap1 and  y-ball_speed[1] <= blocker[1] + 30):
                    x = blocker[0]
                    ball_speed[0] *= -1
                else:
                    y = blocker[1] + 30
                    ball_speed[1] *= -1
                '''
        x += ball_speed[0]
        y += ball_speed[1]
        if(x < 0):
            x = 0
            ball_speed[0] *= -1
        elif(x > 195):
            x = 195
            ball_speed[0] *= -1   
        if(y > 415):
            y = 415
            ball_speed[1] *= -1
        #print(x, y, blocker)

    return [x, y]
def calculate_ball_position_platform1(scene_info, blocker_speed):
    if(scene_info["ball_speed"][1] == 0):
        return scene_info["ball"]
    x = scene_info["ball"][0]
    y = scene_info["ball"][1]
    frame = scene_info['frame']
    ball_speed =list(scene_info["ball_speed"])
    blocker = list(scene_info['blocker'])
    while(y < 415):
        blocker[0] += blocker_speed
        if(blocker[0] > 160):
            blocker[0] = 160
            blocker_speed *= -1
        elif(blocker[0] < 0):
            blocker[0] = 0
            blocker_speed *= -1
        if(frame > 2960):
            pass#print(x, y)
        if((frame) -  150 % 200 == 0):
            if(ball_speed[0] > 0):
                ball_speed[0] += 1
            else:
                ball_speed[0] -= 1
            if(ball_speed[1] > 0):
                ball_speed[1] += 1
            else:
                ball_speed[1] -= 1
        frame += 1
        if(x <= blocker[0] + 25 and x >= blocker[0] - 5 and y <= blocker[1] + 15 and y >= blocker[1] - 5):
                #print("hit", x, y)
                
                gap1 = x - blocker[0]
                gap2 = blocker[0] + 30 - x
                gap3 = y - blocker[1]
                gap4 = blocker[1] + 20 - y
                
                f_gap = min([gap1, gap2, gap3, gap4])
                if(f_gap == gap1):
                    #x = blocker[0]
                    y = blocker[1] + 15
                    ball_speed[1] *= -1
                elif(f_gap == gap2):
                    #x = blocker[0] + 40
                    y = blocker[1] + 15
                    ball_speed[1] *= -1
                elif(f_gap == gap3):
                    y = blocker[1] + 15
                    ball_speed[1] *= -1
                else:
                    y = blocker[1] + 15
                    ball_speed[1] *= -1
                
                '''
                if(y-ball_speed[1] >= blocker[1]+30):
                    ball_speed[1] *= -1
                    y = blocker[1]+30
                elif(gap1 > gap2 and y-ball_speed[1] >= blocker[1]):
                    x = blocker[0] + 40
                    ball_speed[0] *= -1
                elif(gap2 >= gap1 and y-ball_speed[1] >= blocker[1]):
                    x = blocker[0]
                    ball_speed[0] *= -1
                else:
                    y = blocker[1]
                    ball_speed[1] *= -1
                
                '''
        x += ball_speed[0]
        y += ball_speed[1]
        if(y < 80):
            ball_speed[1] *= -1
            y = 80
        if(x < 0):
            x = 0
            ball_speed[0] *= -1
        elif(x > 195):
            x = 195
            ball_speed[0] *= -1   

    return [x, y]