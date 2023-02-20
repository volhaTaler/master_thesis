from hopfieldnetwork import *
from grid import *
from nao_speech import *
from nao_imagecapture import *
from PIL import Image
from audio import *
from recaudio import *
import random
from wn import *
import datetime

import image_integration

'''This script contains the Sarsa algorithm embedded with robot actions for visual audio game.
 It contains the reward functions that is based on the Hopfield energy and an epsilon greedy state decision policy.
 The visual audio images are concatenated. So the training needs to be done with visual and audio data.'''

def generate_reward(train_images, current_state, current_action, img_c, img_f):
    """ Generates reward based on the energy used in the Hopfield network.
    Parameters
    -----------
    train_images: bipolar array
    the training images for the Hopfield Network
    current_state: integer
    number of chosen image
    current_action: integer
    number of image to move to
    rsize: tuple
    preferred size of the individual pictures

    Return
    -------
    reward : positive reward for low energy images
    energy_state: energy of current state
    energy_action: energy of future state
    """

    # run the image through the hopfield to generate an energy
    weights_h = calc_weights(train_images)
    
    filename_1 = constants.store_gameimages + '%s.png' % img_c
    print(filename_1)
    filename_2 = constants.store_gameimages+ '%s.png' % img_f
    print(filename_2)

    current_pattern = bipolarize_pattern_robot(filename_1)
    future_pattern = bipolarize_pattern_robot(filename_2)
    print("checkpoint reward 1")
    new_s1, changed_bits1, state_changes1, epochs1 = calc_stateupdate_async(current_pattern, weights_h, 1000, 1000)
    new_s2, changed_bits2, state_changes2, epochs2 = calc_stateupdate_async(future_pattern, weights_h, 1000, 1000)
    print("checkpoint reward 2")
    energy_state = changed_bits1
    energy_action = changed_bits2
    if energy_state < energy_action:
        reward = -1
    else:
       reward = 1
    
    print("new reward; ", reward)


    return reward, energy_state, energy_action


def update_q(train_images, start_location, start_img, max_iter,  q, cumulative_reward, cumulative_energy, total_reward, total_energy, no_of_state_visits, total_energy_by_state, total_reward_by_state, td_storage, i, condition, trust_value,
            help_requests, rew_each_step_cogn_cue, rew_each_step_social_cue):
    """Calculates q value, updates in each iteration based on a specified policy and reward function
     Parameters
    -----------
    prepath: filepath
    the path where the images to display are located
    postpath: filepath
    the path where the captured images are to be stored
    train_images: bipolar array
    the training images for the Hopfield Network
    start_location: integer
    number of starting image on grid
    grid_width: integer
    number of images in the vertical direction of the grid
    grid_length: integer
    number of images in the horizontal direction of the grid
    max_iter: integer
    maximum number of iterations
    rsize: tuple
    size of the individual pictures

    Return
    -------
    position to move to
    Q-value of the chosen position

    The function takes more inputs and return but the ones mentioned are the relevant ones to functionality.
    """

    state_no = start_location

    current_q, current_action = eps_greedy(q, state_no)

    current_iter = 0

    r_current = 0

    help = 0
    cue_reward = 0



    image_current = start_img


    while current_iter < max_iter:

        current_iter += 1

        print('reward: ', r_current)
        no_of_state_visits[state_no] += 1
        image_future = random.randint(0, constants.ntrainimgs - 1)
        while image_future == image_current:
            image_future = random.randint(0, constants.ntrainimgs -1)
            print('still in the loop')

        ''' uncomment the next line for a  realistic interaction with speech '''

        #speech_choose_image(current_action)

        display_image(constants.store_grids, 'yellowgrid%s' % current_action, constants.time3)

        '''apply noise to next image, first image noise it applied before start of algorithm'''

        noise_img = sp_noise(constants.get_gameimages, image_future, constants.probabilities[current_action])
        filename = constants.store_imageswnoise  + '%s' % image_future + '.png'
        cv2.imwrite(filename, noise_img)
        time.sleep(constants.time7)
        finish_display_image()


        display_image(constants.store_imageswnoise , image_future, constants.time2)
        time.sleep(constants.time6)
        result, image = capture_robot_camera_nao(constants.IP, constants.PORT)
        time.sleep(constants.time6)
        img = Image.fromarray(image)
        print("checkpoint 2")
        img_res = img.crop((constants.left, constants.top, constants.right, constants.bottom))
        print("checkpoint 3")
        filename = constants.store_captured + '%s' % image_future + '.png'
        img_res.save(filename)
        filename_vis = '%s.png' % image_future
        img_res.save(filename_vis)
        # dt = datetime.datetime.now()
        # timestamp = '%s-%s-%s_%s:%s:%s' % (dt.month, dt.day, dt.year, dt.hour, dt.minute, dt.second)
        # img_name = '/home/volha/Desktop/MSc/master_thesis/trail/test_captured/' + timestamp + '_captured.png' 
        # img_res.save(img_name)
        concat_audio_visual2('/home/volha/Desktop/MSc/master_thesis/robot-playground-main/multimodal_trust/', constants.store_gameimages, image_future)
        time.sleep(0.5)
        finish_display_image()
        print("checkpoint 1")

        ''' assistant providing audio depending on reward gained '''

        if r_current < 0:
            speech_other("I am not doing so well, please help me.")
            # speech_other2("I will tell you what that is.")

            # we are are in online mode, then we do not need this plit because the human interaction partner will take care of it
            if(constants.experiment_online):
                cue_reward = image_integration.predict_intention(offline_mode=False)
            else:
                if condition == 1: #helpful assistant
                    cue_reward = image_integration.predict_intention(condition=1, offline_mode=True)
                    
                if condition == 2: #unhelpful assistant
                    cue_reward = image_integration.predict_intention(condition=2, offline_mode=True)

                if condition == 3:
                    cue_reward = image_integration.predict_intention(condition=3, offline_mode=True)

                if condition == 4: #random assistant, this assistant will be deceptive one which gives wrong action suggestion but reliable social cues. 
                    value = np.random.uniform(low=0, high=1, size=1)

                    if value >= 0.5:
                        cue_reward = image_integration.predict_intention(condition=1, offline_mode=True)
                    else:
                        cue_reward = image_integration.predict_intention(condition=2, offline_mode=True)


        # concat_audio_visual(constants.store_captured, constants.store_vagameimgs, image_future)

        ''' pass current and futute states into the reward function '''
        

        r_current, energy_current, energy_future = generate_reward(train_images, state_no, current_action, image_current, image_future)
        print("cue_reward ", cue_reward)
        rew_each_step_cogn_cue[i] = r_current
        r_current += int(cue_reward)
        rew_each_step_social_cue[i] = int(cue_reward)
        cue_reward = 0
        print("checkpoint 4")
        ''' generate the trust value if help was requested in the previous state '''

        if help == 1:
            trust_value += r_current - r_old
            print('trust: ', trust_value)
            help_requests += 1

        help = 0  # reset help value

        ''' add info to saving matrices '''

        total_energy_by_state[state_no] += energy_current
        total_reward += r_current
        total_energy += energy_current
        total_reward_by_state[state_no] += r_current
        cumulative_reward[i] = total_reward
        cumulative_energy[i] = total_energy
        
        

        i += 1
        print('iter:', i)

        ''' update states and image '''

        future_state = current_action
        image_current = image_future

        ''' this codes function behaviour if final state is reached this run '''

        final_states = (0, 10)
        if future_state == final_states[0] or future_state == final_states[1]:

            #print('Final state is reached. It is: ', future_state)

            if future_state ==  final_states[0]:
                r_current = 10 # 1000
                total_reward += r_current
                total_reward_by_state[future_state] += r_current

                cumulative_reward[i] = total_reward
                td_error = r_current + constants.gamma * q[future_state,future_state] - q[state_no, current_action]
                delta_q = constants.epsilon * (td_error)
                q[state_no, current_action] += delta_q
                print('The current state: ', state_no, 'the chosen action: ', current_action, 'the q value ',  q[state_no, current_action])

                state_no = future_state

                no_of_state_visits[state_no] += 1
            if future_state ==  final_states[1]:
                r_current = -10 # -1000
                total_reward += r_current
                total_reward_by_state[future_state] += r_current

                cumulative_reward[i] = total_reward
                td_error = r_current + constants.gamma * q[future_state, future_state] - q[state_no, current_action]
                delta_q = constants.epsilon * (td_error)
                q[state_no, current_action] += delta_q
                print('The current state: ', state_no, 'the chosen action: ', current_action, 'the q value ',
                      q[state_no, current_action])

                state_no = future_state

                no_of_state_visits[state_no] += 1


            return future_state, q, total_energy_by_state, no_of_state_visits, total_reward, total_energy, cumulative_reward, cumulative_energy, total_reward_by_state, td_storage, i, trust_value, help_requests, rew_each_step_cogn_cue, rew_each_step_social_cue


        ''' Dynamic desicion . minimum iterations that are required
        sarsa sabilisation

        '''
        ''' assistant suggesting direction if the reward is negative '''

        if r_current < 0:
            help = 1

            if condition == 1: # helpful assistant
                future_action = current_action - 1
            if condition == 2 or condition== 3: # unhelpful assistant
                future_action = current_action + 1
            if condition == 4: # random assistant and deceptive assistant
                value = np.random.uniform(low=0, high=1, size=1)

                if value >= 0.5:
                    future_action = current_action - 1
                else:
                    future_action = current_action + 1
            r_old = r_current

            ''' or the agent choosing ita future action '''

        else:
            future_q, future_action = eps_greedy(q, future_state)

        ''' updates other storage matrices '''

        td_error = r_current + constants.gamma * q[future_state, future_action] - q[state_no, current_action]
        td_storage[i] = td_error

        delta_q = constants.epsilon * (td_error)
        q[state_no, current_action] += delta_q

        ''' update states'''

        state_no = future_state

        current_action = future_action


    return future_state, q, total_energy_by_state, no_of_state_visits, total_reward, total_energy, cumulative_reward, cumulative_energy, total_reward_by_state, td_storage, i, trust_value, help_requests, rew_each_step_cogn_cue, rew_each_step_social_cue


def eps_greedy(q, state):
    """Generates chosen position based on an epsilon greedy policy
        Parameters
    -----------
    q: matrix
    Q-values
    state: integer
    current state
    epsilon: floatE
    chance of choosing random action

    Return
    -------
    action: position to move to
    action_q: Q-value of the chosen position
    """
    value = np.random.uniform(low=0, high=1, size=1)
    state = int(state)

    move_up = int(state + 1)
    move_down = int(state - 1)

    if value >= constants.epsilon:

        action_q = np.max((q[state, move_down], q[state, move_up]))
        if action_q == q[state, move_down]:
            action = move_down
        else:
            action = move_up

        action = np.array(action).flatten()[0]


    else:
        move = np.random.choice([move_up, move_down])
        action_q = q[state, move]
        action = move

        action = np.array(action).flatten()[0]

    return action_q, action

