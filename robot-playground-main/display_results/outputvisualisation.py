import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


path01 = "/home/volha/Desktop/MSc/MSC_data/experiment_results/18_offline_cond1_FIXED_18.02.23/"
path02 = "/home/volha/Desktop/MSc/MSC_data/experiment_results/18_offline_cond2_18.02.23/"
path03 = "/home/volha/Desktop/MSc/MSC_data/experiment_results/18_offline_cond3_fixed_18.02.23/"
path04 = "/home/volha/Desktop/MSc/MSC_data/experiment_results/18_offline_cond4_19.02.23/"


path1 = "/home/volha/Desktop/MSc/MSC_data/experiment_results/20_online_cond1_20.02.23_10episodes_6runs/"
path2 = "/home/volha/Desktop/MSc/MSC_data/experiment_results/20_online_cond2_full_20.02.23_6runs_10_episodes/"
path3 = "/home/volha/Desktop/MSc/MSC_data/experiment_results/20_online_cond3_20.02.23_6runs_10episodes/"
path4 = "/home/volha/Desktop/MSc/MSC_data/experiment_results/20_online_cond4_20.02.23/"


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

        # plot of cumulative rewards over iteration steps
        # cumulative_reward_plot = cumulative_reward[cumulative_reward != 0]
        # name = stats.split("/")[-1]
        # iterations = np.arange(0,len(cumulative_reward_plot),1)
        # plt.figure()
        # plt.plot(iterations, cumulative_reward_plot)
        # plt.title('Cumulative reward')
        # plt.xlabel('Iteration')
        # plt.ylabel('Total Reward')
        # plt.savefig('/home/volha/Desktop/MSc/MSC_data/experiment_results/plots/' + name+ '_out_repeat%s_cum_rew.png' % repeat )
        #plt.close()
        #plt.show()
        # plt.figure()
        # plt.close()


        energy_average = np.reshape(energy_by_state/state_visits_div,  (1,11))

        # fig, ax = plt.subplots(1,1)
        # img = ax.imshow(energy_average, extent=[0,9,0,1])
        #y_label_list = ['0', '1', '2']
        # ax.set_yticks([])
        # ax.set_yticklabels(y_label_list)
        # x_label_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        # ax.set_xticks([0.4, 1.25, 2.05, 2.90, 3.70, 4.6, 5.405, 6.15, 6.95, 7.8, 8.6])
        # ax.set_xticklabels(x_label_list)
        # cbar = fig.colorbar(img, orientation="horizontal")
        #cbar.set_label("Total Energy")
        #plt.title('Energy by state')
        #plt.xlabel('State')
        #plt.savefig('/home/volha/Desktop/MSc/MSC_data/experiment_results/plots/output_repeat%s_energy.png' % repeat )
        #plt.show()
        #plt.figure()
        #plt.imshow(final_q, extent=[0,20,0,20])
        #plt.title('Q Matrix Heatmap')
        #plt.tick_params(left=False,
        #            bottom=False,
        #             labelleft=False,
        #            labelbottom=False)
        #cbar = plt.colorbar(img, orientation="horizontal")
        #cbar.set_label("Q-value")
        #plt.savefig('/home/volha/Desktop/MSc/MSC_data/experiment_results/plots/output_repeat%s_q.png' % repeat )
       
        #plt.show()
   
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
    plt.savefig('/home/volha/Desktop/MSc/MSC_data/experiment_results/plots/%s_visits.png' % title[i] )
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
    fig.savefig('/home/volha/Desktop/MSc/MSC_data/experiment_results/plots/%s_visits_hist.png' % title[i])
    plt.close()
    