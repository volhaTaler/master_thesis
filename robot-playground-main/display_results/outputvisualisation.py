# more deteiled analysis of robot's movements during the experimental sessions

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


path01 = "/home/path1"
path02 = "/home/path2"
path03 = "/home/path3"
path04 = "/home/path4"


path1 = "/home/path5"
path2 = "/home/path6"
path3 = "/home/path7"
path4 = "/home/path8"


all_files = [path1, path2, path3, path4, path01, path02, path03, path04]

title = ['Trustworthy with a physical partner', 'Non-Trustworthy with a physical partner', 'Deceptive with a physical partner', 'Random with a physical partner', 'Trustworthy with a virtual partner', 'Non-Trustworthy with a virtual partner', 'Deceptive with a virtual partner', 'Random with a virtual partner']


for i, stats in enumerate(all_files):
    average_state_visits = np.zeros(11)
    average_state_energy = np.zeros(11)
    for repeat in np.arange(1, 11, 1):
        cumulative_reward = np.load(stats + '%s_cum_rew.npy' % repeat )
        state_visits = np.load(stats + '%s_state_visits.npy' % repeat )
        average_state_visits = np.add(average_state_visits, state_visits)
        energy_by_state = np.load(stats + '%s_energy_state.npy' % repeat )
        average_state_energy = np.add(average_state_energy, energy_by_state)
        final_q =  np.load(stats + '%s_end_q.npy' % repeat )
        print(repeat, final_q)
        state_visits_div = np.where((state_visits==0), 1, state_visits)
        temporal_difference = np.load(stats + '%s_td.npy' % repeat )
        no_iterations = int(state_visits.sum()-1)

        energy_average = np.reshape(energy_by_state/state_visits_div,  (1,11))

        print('Average energy by state at the end of the repeat %s: ' % repeat ,     energy_by_state/state_visits_div)
        print('Number of times each state was visited during repeat %s: ' % repeat , state_visits)
    



    ######################## heatmap of visits frequencies #################################
    average_state_visits = np.divide(average_state_visits, 10)
    states = np.reshape(average_state_visits,  (1,11))
    fig, ax = plt.subplots(1,1)
    img = ax.imshow(states, extent=[0,10,0,1])
    ax.set_yticks([]) 
    # ax.set_yticklabels(y_label_list)
    x_label_list = ['L5', 'L4', 'L3', 'L2', 'L1', '0', 'R1', 'R2', 'R3', 'R4', 'R5']
    ax.set_xticks([0.5, 1.3, 2.1, 3.2, 4.1, 5.0, 5.9, 6.8, 7.7, 8.6, 9.5])
    ax.set_xticklabels(x_label_list)
    cbar = fig.colorbar(img, orientation="horizontal")
    cbar.set_label("Scale of total number of visits")
    plt.title('Game grid based on the frequency of visits by the robot')
    plt.xlabel('State')
    plt.savefig('/home/path/plots/%s_visits.png' % title[i] )
    plt.show()
    plt.figure()
    plt.close()
    

    ################### histogram #######################################
    average_state_visits = np.divide(average_state_visits, 10)
    x = ['L5', 'L4', 'L3', 'L2', 'L1', '0', 'R1', 'R2', 'R3', 'R4', 'R5']# or, simpler, x = np.arange(len(x1)) + 1
    df = pd.DataFrame({'Visits': average_state_visits, 'States': x})
    # df_long = df.melt('States')
    ax = sns.barplot(x='States', y='Visits', data=df)
    ax.set(ylabel='Visits', xlabel='States')
    ax.bar_label(ax.containers[0], fmt='%.2f')
    plt.show()
    fig = ax.get_figure()
    # plt.xticks(states, ['L5','L4','L3', 'L2', 'L1', '0', 'R1', 'R2', 'R3', 'R4', 'R5'])
    fig.savefig('/home/path/plots/%s_visits_hist.png' % title[i])
    plt.close()
    
