import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd
import seaborn as sns



all_cum_rew_arrays = [] 

trust_arr = []
help_arr = []
# online 10 runs
# path1 = "/home/volha/Desktop/MSc/MSC_data/experiment_results/online_cond1_06.01.23_cur_rew__not_cogn_cue_rew/"
# path2 = "/home/volha/Desktop/MSc/MSC_data/experiment_results/online_cond2_06.01.23_with_cogn_cue_rew/"
# path22 = "/home/volha/Desktop/MSc/MSC_data/experiment_results/online_cond2_12.01.23_lower_0_num/"
# wrong deceptive implementation path3 = "/home/volha/Desktop/MSc/MSC_data/experiment_results/online_cond3_06.01.23_cur_rew_not_cogn_cue_rew/"
# path3 = "/home/volha/Desktop/MSc/MSC_data/experiment_results/online_cond3_11.01.23_correct_decept_correct_cogn_cue/"
# path4 = "/home/volha/Desktop/MSc/MSC_data/experiment_results/online_cond4_06.01.23_cur_rew_not_cogn_cue_rew/"


path1 = "/home/volha/Desktop/MSc/MSC_data/experiment_results/20_online_cond1_20.02.23_10episodes_6runs/"
path2 = "/home/volha/Desktop/MSc/MSC_data/experiment_results/20_online_cond2_full_20.02.23_6runs_10_episodes/"
path3 = "/home/volha/Desktop/MSc/MSC_data/experiment_results/20_online_cond3_20.02.23_6runs_10episodes/"
path4 = "/home/volha/Desktop/MSc/MSC_data/experiment_results/20_online_cond4_20.02.23/"

# online 6 runs
#NUM_6 = 7
#path61 = "/home/volha/Desktop/MSc/MSC_data/experiment_results/online_cond1_6runs_combined/"
#path62 = "/home/volha/Desktop/MSc/MSC_data/experiment_results/online_cond2_6runs_combined/"
#path63 = "/home/volha/Desktop/MSc/MSC_data/experiment_results/online_cond3_6runs_combined/"
#path64 = "/home/volha/Desktop/MSc/MSC_data/experiment_results/online_cond4_6runs_combined/"

# offline
# path01 = "/home/volha/Desktop/MSc/MSC_data/experiment_results/offline_cond1_13.01.23/"
# path02 = "/home/volha/Desktop/MSc/MSC_data/experiment_results/offline_cond2_13.01.23/"
#path02_run2 = "/home/volha/Desktop/MSc/MSC_data/experiment_results/offline_cond2_13.01.23_run2/"
# path02_full = "/home/volha/Desktop/MSc/MSC_data/experiment_results/offline_cond2_run3_full_data_13.01.23/"
# path03 = "/home/volha/Desktop/MSc/MSC_data/experiment_results/offline_cond3_13.01.23/"
# path04 = "/home/volha/Desktop/MSc/MSC_data/experiment_results/offline_cond4_13.01.23/"

path01 = "/home/volha/Desktop/MSc/MSC_data/experiment_results/18_offline_cond1_FIXED_18.02.23/"
path02 = "/home/volha/Desktop/MSc/MSC_data/experiment_results/18_offline_cond2_18.02.23/"
path03 = "/home/volha/Desktop/MSc/MSC_data/experiment_results/18_offline_cond3_fixed_18.02.23/"
path04 = "/home/volha/Desktop/MSc/MSC_data/experiment_results/18_offline_cond4_19.02.23/"


path = path04
NUM = 11

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

def process_social_rew(i, length):
        name = str(i) + plots[3]
        #print(name)
        data = np.load(path +name)
        #print("LENGTH: ", length)
        # print("FULL: ", data)
        # print("CUT: ", data[:length])
        filename = "/home/volha/Desktop/MSc/MSC_data/experiment_results/social_reward/" +"%s_%s_social_reward_per_step_CUT.npy"  %("cond4_offline",str(i))
        np.save(filename, data[:length])
    
def process_cogn_rew(i, length):
        name = str(i) + plots[4]
        # print(name)
        data = np.load(path +name)
        # print("FULL: ", data)
        # print("CUT: ", data[:length])
        filename = "/home/volha/Desktop/MSc/MSC_data/experiment_results/social_reward/" +"%s_%s_cogn_reward_per_step_CUT.npy"  %("cond4_offline",  str(i))
        np.save(filename, data[:length])




# process cumulative reward
def cut_tails(results, num, pos):
    steps_stat = np.zeros(10)
    all_cum_rew_arrays_cut = []
    all_achieved_rew = []
    averaged_energy = []
    lenghts_of_runs = dict()
    DATA2 = []
    for i in range(1,num):
        name = str(i) + plots[pos]
        # print(name)
        data = np.load(path +name)
        ind = 0
        for d in reversed(data):
            if d == 0:
                ind += 1
            else:
                break
        DATA2 = data[0:-ind]
        steps_stat[i-1] = len(DATA2)
        #process_social_rew(i, len(DATA2))
        # process_cogn_rew(i, len(DATA2))
        if pos==0:
            line = "  " + str(i) + " cumulative reward :" + str(DATA2[-1])
            results.append(line + "\n")
            all_achieved_rew.append(DATA2[-1])
        elif pos == 1:
            line = "  " + str(i) + " cumulative energy :" + str(DATA2[-1])
            results.append(line + "\n")
            # only average
            # for energy
            all_achieved_rew.append(DATA2[-1]/len(DATA2))
            line = "  " + str(i) + " average cumulative energy :" + str(DATA2[-1]/len(DATA2))
            results.append(line)
            averaged_energy.append(DATA2[-1])
            
        # all_cum_rew_arrays.append(data)
        all_cum_rew_arrays_cut.append(DATA2)
        lenghts_of_runs[i] = len(DATA2)
        # np.save(path + str(i) + "_CUT_" + plots[pos], DATA2)
    # compute average final reward
    
    average_reward = np.mean(all_achieved_rew)
    std_calc = np.std(all_achieved_rew)
    results.append("STANDARD DEVIATION: " + str(std_calc))

    if pos==0:
        line = "TOTAL Average Reward: " + str(average_reward)
        results.append(line)
        #print("AVERAGE: ", np.average(steps_stat))
    elif pos==1:
        line = "TOTAL Average Enegry: " + str(average_reward)
        results.append("Length: " + str(all_achieved_rew) )
        results.append(line)
        results.append("Average energy: " + str(np.mean(averaged_energy)))
    results.append(str(lenghts_of_runs))
    # print("MIN LENGTH: ", min(list(lenghts_of_runs.values())))
    all_cum_rew_arrays_cut = add_average_col(all_cum_rew_arrays_cut,min(list(lenghts_of_runs.values())))

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

def add_average_col (array, length):
    df = pd.DataFrame(array)
    average = np.array(df.mean().round(2).to_list())[:length]
    np.save("/home/volha/Desktop/MSc/MSC_data/experiment_results/averages_reward/4_cond4_average_offline.npy", average)
    print("Average: ", average)
    array.append(average)
    
    return array


# - create a dataframe
# df = create_df(all_cum_rew_arrays)
# df.to_excel("all_cum_rew_online_cond2_12.01_cut.xlsx")

def find_lengths_of_lists(result, lst, name):
    list_len = [len(j) for j in lst]
    line = name + str(list_len)
    result.append(line)

def plot_td_errors():
    for i in range(1,11):    
        #data = np.load(file)
        img_name = path + str(i) + plots[-1]
        data = np.load(img_name)
        #plt.plot(data[0])
        plt.grid(True)
        plt.plot(data)
        plt.xlabel("Iteration", fontsize=16)
        plt.ylabel("Error", fontsize=16)
        filename = path + str(i) + plots[-1].replace("npy", "png")
        plt.savefig(filename)
    plt.close()

def plot_reward(arr, filename, x_label, y_label, legend_pos):
    plt.xticks(np.arange(0, 186, 20.0))
    plt.yticks(np.arange(-152, 142, 20.0))
    for i, m in enumerate(arr):    
        #data = np.load(file)
        img_name = path + filename
        #plt.plot(data[0])
        plt.grid(True)
        if i == (len(arr)-1):
            # print("Array length: ", m)
            plt.plot(m, 'b-', label="Average", linewidth=2.6)
            plt.legend(loc=legend_pos)
        else:
            plt.plot(m)
        plt.xlabel(x_label, fontsize=16)
        plt.ylabel(y_label, fontsize=16)
        plt.savefig(img_name)
    plt.close()

def process_rewards(results1):
    
    all_cum_rew_arrays_cut = cut_tails(results1, NUM, 0)
    find_lengths_of_lists(results1, all_cum_rew_arrays_cut, "REWARD -- List of lengths of runs: ")

    filename = "Cumulative_Reward_4_online_10runs_fixed.png"
    #title = "Cumulative Reward Offline Reliable Partner"
    x_label = "Iteration"
    y_label = "Reward"
    plot_reward(all_cum_rew_arrays_cut, filename, x_label, y_label, "upper right")

def process_energy(results1):
    all_cum_en_arrays_cut = cut_tails(results1, NUM, 1)
    filename = "Cumulative_Energy_2_offline_10runs.png"
    title = "Cumulative Energy Offline Reliable Partner"
    find_lengths_of_lists(results1, all_cum_en_arrays_cut, "ENERGY -- List of lengths of runs: ")
    x_label = "Step per Run"
    y_label = "Energy"
    plot_reward(all_cum_en_arrays_cut, filename, x_label, y_label, "upper left")





def main():
    results1 = process_numeric_values(NUM)
    cut_tails(results1, NUM, 0)
    process_rewards(results1)
    # process_energy(results1)
    metrics_to_file("OVERVIEW_4_10runs_offline.txt", results1)
    
    

if __name__=="__main__":
    main()