
# here we proccess collected data: total reward, energy, number of steps, number of help requests,
# as well as number of the generated social cues  

import numpy as np
import matplotlib.pyplot as plt



path01 = "/home/Desktop/MSc/path1"
path02 = "/home/Desktop/MSc/path2"
path03 = "/home/Desktop/MSc/path3"
path04 = "/home/Desktop/MSc/path4"


path1 = "/home/Desktop/MSc/path5"
path2 = "/home/Desktop/MSc/path6"
path3 = "/home/Desktop/MSc/path7"
path4 = "/home/Desktop/MSc/path8"


all_files = [path1, path2, path3, path4, path01, path02, path03, path04]

title = ['Trustworthy with a physical partner', 'Non-Trustworthy with a physical partner', 'Deceptive with a physical partner', 'Random with a physical partner', 'Trustworthy with a virtual partner', 'Non-Trustworthy with a virtual partner', 'Deceptive with a virtual partner', 'Random with a virtual partner']

total_rew_array = np.zeros(10)
steps_array = np.zeros(10)
social_negative_reward_ar = np.zeros(10)
social_positive_reward_ar = np.zeros(10)
total_en_array = np.zeros(10)
total_trust_array = np.zeros(10)
help_array = np.zeros(10)
array_of_cut_rew = []

def print_stast_rew():
   for i, filepath in enumerate(all_files):
        
        for repeat in np.arange(1, 11):
            cumulative_reward = np.load(filepath + '%s_cum_rew.npy' % repeat)
            cumulative_reward_plot = cumulative_reward[cumulative_reward != 0]
            last_ind = len(cumulative_reward_plot)
            total_reward = cumulative_reward_plot[int(last_ind)-1]
            total_rew_array[repeat-1] = total_reward


        min = np.min(total_rew_array)
        max = np.max(total_rew_array)
        std = np.std(total_rew_array)
        avr = np.average(total_rew_array)

        print(title[i], "   cumulative reward: ",  'min: ', min, 'max: ', max, 'std: ', std, 'average: ', avr)
        print('\n')

print_stast_rew()

def print_stast_en():
  for i, filepath in enumerate(all_files):
        average_per_step = np.zeros(10)
        too_much_en = 0
        
        for repeat in np.arange(1, 11):
            cumulative_energy = np.load(filepath + '%s_cum_en.npy' % repeat)
            cumulative_energy_plot = cumulative_energy[cumulative_energy != 0]
            last_ind = len(cumulative_energy_plot)
            average_per_step[repeat-1] = cumulative_energy_plot[-1]/last_ind
            total_energy = cumulative_energy_plot[int(last_ind)-1]
            total_en_array[repeat-1] = total_energy
            #if('Trustworthy' in title[i]):
                # print("Array of steps: ", str(repeat), ": ", str(cumulative_energy))
            
            for j in range(1, last_ind):
                if (cumulative_energy_plot[j] - cumulative_energy_plot[j-1]) > 900:
                    too_much_en += 1


        min = np.min(total_en_array)
        max = np.max(total_en_array)
        std = np.std(total_en_array)
        avr = np.average(total_en_array)
        avr_per_step = np.average(average_per_step) 

        print(title[i], " : ", "energy", ": ",  'min: ', min, 'max: ', max, 'std: ', std, 'average: ', avr, ' average per step: ', avr_per_step)
        print(" number of too much energy: ", too_much_en)
        print('\n')

print_stast_en()




def print_steps():
   for i, filepath in enumerate(all_files):
        
        for repeat in np.arange(1, 11):
            cumulative_reward = np.load(filepath + '%s_cum_rew.npy' % repeat)
            cumulative_reward_plot = cumulative_reward[cumulative_reward != 0]
            cumulative_reward_plot = cumulative_reward[::-1]
            zeros = np.where(cumulative_reward_plot != 0)[0]
            steps_array[repeat-1] = len(cumulative_reward[:-zeros[0]])
            
        
        avr = np.average(steps_array)
       

        print(title[i], ": ",  'steps: ', avr)
        print('\n')


print_steps()

def print_help():
    
    for i, filepath in enumerate(all_files):
        
        for repeat in np.arange(1, 11):
            help = np.load(filepath + '%s_help.npy' % repeat)

            help_array[repeat-1] = help

        avr = np.average(help_array)

        print(title[i], ": ", " Help requests", ": ",  'help: ', avr)
        print('\n')


print_help()


def print_social_cue_reward():

   for i, filepath in enumerate(all_files):
        ones = 0
        minus_ones = 0
        
        for repeat in np.arange(1, 11):
            cumulative_reward = np.load(filepath + '%s_cum_rew.npy' % repeat)
            social_reward = np.load(filepath + '%s_social_reward_per_step.npy' % repeat)
            cumulative_reward_plot = cumulative_reward[::-1]
            zeros = np.where(cumulative_reward_plot != 0)[0]
            cumulative_reward_plot = cumulative_reward[:-zeros[0]]
            #cumulative_reward_plot = cumulative_reward[cumulative_reward != 0]
            duration = len(cumulative_reward_plot)
            cut_social_reward = social_reward[:duration]
            ones = len(cut_social_reward[cut_social_reward==1])
            minus_ones =len(cut_social_reward[cut_social_reward==-1])
            social_positive_reward_ar[repeat-1] = ones
            social_negative_reward_ar[repeat-1] = minus_ones
        avr_social_pos = np.average(social_positive_reward_ar)
        avr_social_neg = np.average(social_negative_reward_ar)
        

        print(title[i], ": ",  'social cues positive: ', avr_social_pos)
        print(title[i], ": ",  'social cues negative: ', avr_social_neg)
        print('\n')


print_social_cue_reward()
