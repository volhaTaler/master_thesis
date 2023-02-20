import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd
import seaborn as sns



all_cum_rew_arrays = [] 

trust_arr = []
help_arr = []
# online
path1 = "/home/volha/Desktop/MSc/MSC_data/experiment_results/online_cond1_06.01.23_cur_rew__not_cogn_cue_rew/"
path2 = "/home/volha/Desktop/MSc/MSC_data/experiment_results/online_cond2_06.01.23_with_cogn_cue_rew/"
path22 = "/home/volha/Desktop/MSc/MSC_data/experiment_results/online_cond2_12.01.23_lower_0_num/"
# wrong deceptive implementation path3 = "/home/volha/Desktop/MSc/MSC_data/experiment_results/online_cond3_06.01.23_cur_rew_not_cogn_cue_rew/"
path3 = "/home/volha/Desktop/MSc/MSC_data/experiment_results/online_cond3_11.01.23_correct_decept_correct_cogn_cue/"
path4 = "/home/volha/Desktop/MSc/MSC_data/experiment_results/online_cond4_06.01.23_cur_rew_not_cogn_cue_rew/"
NUM_O = 4

# online 6 runs
NUM_6 = 7
path61 = "/home/volha/Desktop/MSc/MSC_data/experiment_results/online_cond1_6runs_combined/"
path62 = "/home/volha/Desktop/MSc/MSC_data/experiment_results/online_cond2_6runs_combined/"
path63 = "/home/volha/Desktop/MSc/MSC_data/experiment_results/online_cond3_6runs_combined/"
path64 = "/home/volha/Desktop/MSc/MSC_data/experiment_results/online_cond4_6runs_combined/"

# offline
path01 = "/home/volha/Desktop/MSc/MSC_data/experiment_results/offline_cond1_13.01.23/"
path02 = "/home/volha/Desktop/MSc/MSC_data/experiment_results/offline_cond2_13.01.23/"
path02_run2 = "/home/volha/Desktop/MSc/MSC_data/experiment_results/offline_cond2_13.01.23_run2/"
path02_full = "/home/volha/Desktop/MSc/MSC_data/experiment_results/offline_cond2_run3_full_data_13.01.23/"
path03 = "/home/volha/Desktop/MSc/MSC_data/experiment_results/offline_cond3_13.01.23/"
path04 = "/home/volha/Desktop/MSc/MSC_data/experiment_results/offline_cond4_13.01.23/"
NUM_OFF = 11

path = path62
NUM = NUM_6

metrics = ["_trust.npy", "_energy.npy", "_help.npy",]
plots = ["_cum_rew.npy", "_cum_en.npy", "_reward_state.npy", "_social_reward_per_step.npy", "_cogn_reward_per_step.npy", "_state_visits.npy", "_energy_state.npy", "_td.npy"]
# plots_states = ["_state_visits.npy", "_energy_state.npy"]
# plots_hist = [ "_social_reward_per_step.npy", "_cogn_reward_per_step.npy"]


# write numeric values
def process_numeric_values(num):
    results =[]
    for m in metrics:
        for i in range(1, num):
            name = str(i) + m
            file = path + name
            data = np.load(file)
            if m == "_trust.npy":
                trust_arr.append(data)
            elif m == "_help.npy":
                help_arr.append(data)
            line = name + ": " + str(data)
            results.append(line)
    results.append("AVERAGE Trust: " + str(sum(trust_arr)/len(trust_arr)) + "\n")
    results.append("AVERAGE Help: " + str(sum(help_arr)/len(help_arr)) + "\n")
    return results

# process cumulative reward
def cut_tails(results, num, pos):
    all_cum_rew_arrays_cut = []
    all_achieved_rew = []
    DATA2 = []
    for i in range(1,num):
        name = str(i) + plots[pos]
        print(name)
        data = np.load(path +name)
        ind = 0
        for d in reversed(data):
            if d == 0:
                ind += 1
            else:
                break
        DATA2 = data[0:-ind]
        print(data)
        print(DATA2)
        if pos==0:
            line = "  " + str(i) + " cumulative reward :" + str(DATA2[-1])
            results.append(line)
        else:
            line = "  " + str(i) + " cumulative energy :" + str(DATA2[-1])
            results.append(line)
        results.append("\n")
        # only average
        all_achieved_rew.append(DATA2[-1])
        # all_cum_rew_arrays.append(data)
        all_cum_rew_arrays_cut.append(DATA2)
        

    # compute average final reward
    average_reward = np.mean(all_achieved_rew)
    if pos==0:
        line = "TOTAL Average Reward: " + str(average_reward)
        results.append(line)
    elif pos==1:
        line = "TOTAL Average Enegry: " + str(average_reward)
        results.append(line)
    return all_cum_rew_arrays_cut



# store metrics to file
def metrics_to_file(f_name, results):
    metrics_file = path + f_name
    with open(metrics_file, 'a') as f:
        for l in results:
            f.write(l)
            f.write('\n')

# REWARD

#- calculate the average run
# average = np.mean(np.array(all_cum_rew_arrays), axis=0)
# all_cum_rew_arrays.append(average)

def add_average_col (array):
    df = pd.DataFrame(array)
    array.append(np.array(df.mean().round(2).to_list()))
    return array


# - create a dataframe
# df = create_df(all_cum_rew_arrays)
# df.to_excel("all_cum_rew_online_cond2_12.01_cut.xlsx")

def find_lengths_of_lists(result, lst, name):
    list_len = [len(j) for j in lst]
    line = name + str(list_len)
    result.append(line)


def plot_reward(arr, filename, title, x_label, y_label, legend_pos):

    for i, m in enumerate(arr):    
        #data = np.load(file)
        img_name = path + filename
        #plt.plot(data[0])
        if i == (len(arr)-1):
            print("Average ENERGY: " + str(i))
            plt.plot(m, 'g-', label="Average", linewidth=2.0)
            plt.legend(loc=legend_pos)
        else:
            plt.plot(m)
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.savefig(img_name)
        #plt.show()

def process_rewards(results1):
    
    all_cum_rew_arrays_cut = cut_tails(results1, NUM_6, 0)
    find_lengths_of_lists(results1, all_cum_rew_arrays_cut, "REWARD -- List of lengths of runs: ")
    array = add_average_col(all_cum_rew_arrays_cut)
    filename = "Cumulative_Reward_4_online_6runs.png"
    title = "Cumulative Reward Online Random Partner"
    x_label = "Iteration"
    y_label = "Reward"
    plot_reward(array, filename, title, x_label, y_label, "upper right")

def process_energy(results1):
    all_cum_en_arrays_cut = cut_tails(results1, NUM_6, 1)
    filename = "Cumulative_Energy_1_online_6runs.png"
    title = "Cumulative Energy Online Reliable Partner"
    find_lengths_of_lists(results1, all_cum_en_arrays_cut, "ENERGY -- List of lengths of runs: ")
    array2 = add_average_col(all_cum_en_arrays_cut)
    x_label = "Step per Run"
    y_label = "Energy"
    plot_reward(array2, filename, title, x_label, y_label, "upper left")

#TODO redo: find out where to cut based on the lengths of the actual reward lists. 
def process_rewards_per_step(array_of_partial_rew, filename, num):
    #array_of_partial_rew  = np.array([])
    #for i in range(1, num):
    #    file = path + str(i) + array
    #    array_of_partial_rew = np.concatenate((array_of_partial_rew, np.load(file)), axis=None)
    print(filename, sum(array_of_partial_rew))
    print("Number of 0: ", len([i for i in array_of_partial_rew if i == 0]))
    print("Number of 1: ", len([i for i in array_of_partial_rew if i == 1]))
    print("Number of -1: ", len([i for i in array_of_partial_rew if i == -1]))
    print("Number of 2: ", len([i for i in array_of_partial_rew if i == 2]))
    print("Number of -2: ", len([i for i in array_of_partial_rew if i == -2]))



def main():
    #results1 = process_numeric_values(NUM_6)
    #process_rewards(results1)
    #process_energy(results1)
    #metrics_to_file("OVERVIEW_4_6runs_online.txt", results1)
    results = []
    array = cut_tails(results, NUM_6, 3)
    array2 = cut_tails(results, NUM_6, 4)
    process_rewards_per_step(array, "Social Reward ", NUM_6)
    process_rewards_per_step(plots[4], "Cognitive Reward ", NUM_6)
    
    

if __name__=="__main__":
    main()

# energy

# steps
# for m in plots:
#     for i in range(1, NUM_OFF):
#         name = str(i) + m
#         file = path + name
    
#         data = np.load(file)
#         img_name = file.replace("npy","png")
#         #plt.plot(data[0])
#         plt.plot(data)
#         plt.title(name)
#         plt.xlabel("Iteration")
#         plt.ylabel("Reward/ Energy")
#         plt.savefig(img_name)
#         plt.show()

# for m in plots_states:
#     for i in range(1, NUM_OFF):
#         name = str(i) + m
#         file = path + name
    
#         data = np.load(file)
#         img_name = file.replace("npy","png")
#         #plt.plot(data[0])
#         plt.plot(data)
#         plt.title(name)
#         bins = [1 ,2, 3, 4, 5, 6, 7, 8, 9, 10]
#         plt.hist(data, bins, alpha=1, label=name)
#         plt.legend(loc='upper right')
#         plt.xlabel("State")
#         plt.ylabel("Visits / energy")
#         plt.savefig(img_name)
#         plt.show()

# for m in plots_hist:
#     for i in range(1, NUM_OFF):
#         name = str(i) + m
#         file = path + name
    
#         data = np.load(file)
#         img_name = file.replace("npy","png")
#         #plt.plot(data[0])
#         plt.title(name)
#         bins = [-1, 0, 1]
#         plt.hist(data, bins, alpha=1, label=name)
#         plt.legend(loc='upper right')
#         plt.savefig(img_name)
#         plt.show()


