
import numpy as np
import matplotlib.pyplot as plt


PATH_OFF = "/home/volha/Desktop/ROMAN2023_resources/results/average_rewards_offline/"

PATH_ON = "/home/volha/Desktop/ROMAN2023_resources/results/average_rewards_online/"

PATH_comparison = "/home/volha/Desktop/MSc/MSC_data/experiment_results/averages_reward/part/"

def plot_reward(arr, filepath, x_label, y_label, legend_pos):
    # plt.xticks(np.arange(0, 136, 10.0))
    # plt.yticks(np.arange(-100, 82, 10.0))
    plt.grid(True)
    for file in arr:    
        data = np.load(file)
        img_name = filepath
        #plt.plot(data[0])
        
        if "cond1" in file:
            plt.plot(data, label="Reliable")
        elif "cond2" in file:
            plt.plot(data, label="Unreliable")
        elif "cond3" in file:
            plt.plot(data, label="Deceptive")
        else:
            plt.plot(data, label="Random")
        plt.legend(loc=legend_pos)
        plt.xlabel(x_label, fontsize=16)
        plt.ylabel(y_label, fontsize=16)
    plt.savefig(img_name)
    plt.close()


def read_all_from_file(filepath, setting_type):
    all_rewards = [];
    names = ["4_cond4_average_offline.npy", "4_cond4_average_online.npy"]
    for i in range(1,5):
        array = filepath + str(i) + '_cond'+ str(i) +'_average_' +setting_type+'.npy'
        # array = filepath + names[i]
        all_rewards.append(array)

    return all_rewards



def main():
	path_to_file = PATH_OFF
	plot_name = path_to_file + "average_plots_offline.png"

	array_of_aver_rewards = read_all_from_file(path_to_file, "offline")
	plot_reward(array_of_aver_rewards, plot_name, "Iteration", "Reward", "upper left")


if __name__ =="__main__":
    main() 
