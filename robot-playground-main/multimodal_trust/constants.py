
# file locations
# audio_path = '/home/volha/desktop/msc/master_thesis/robot-playground-main/multimodal_trust/store_audio/'
get_gameimages = '/home/volha/Desktop/MSc/master_thesis/robot-playground-main/multimodal_trust/gameimg/'  # bipolar, low res images for game play are saved here, need to be named with integer numbers (e.g. 1.png)
store_imageswnoise = '/home/volha/Desktop/MSc/master_thesis/robot-playground-main/multimodal_trust/store_imgwnoise/'  # image storage for Nao captures
store_gameimages = '/home/volha/Desktop/MSc/master_thesis/robot-playground-main/multimodal_trust/store_gameimg/' # concat image storage game, used in Hopfield

store_grids = '/home/volha/Desktop/MSc/master_thesis/robot-playground-main/multimodal_trust/gamegrid/'  # location of all grids
get_trainimgs = '/home/volha/Desktop/MSc/master_thesis/robot-playground-main/multimodal_trust/trainimg/' # location of training images
store_vtrainimgs = '/home/volha/Desktop/MSc/master_thesis/robot-playground-main/multimodal_trust/store_trainimg/' # location of training images
store_vatrainimgs = '/home/volha/Desktop/MSc/master_thesis/robot-playground-main/multimodal_trust/store_train_audioimg/' # location of training images visual audio

store_captured = '/home/volha/Desktop/MSc/master_thesis/robot-playground-main/multimodal_trust/store_captured/'
outputs_location = '/home/volha/Desktop/MSc/master_thesis/robot-playground-main/multimodal_trust/outputs/phase/'
store_audio = '/home/volha/Desktop/MSc/master_thesis/robot-playground-main/multimodal_trust/store_audio/' # image storage for human speech training

# Nao set up
IP = "192.168.0.131" # '141.23.190.106' #'172.20.10.5' #  # Nao's IP address, read nao_tutorial1 for more
IP2 = "192.168.0.141" # '141.23.190.106' #'172.20.10.5' #  # Nao's IP address, read nao_tutorial1 for more
PORT = 9559  # Nao port, should remain unchanged

# The coordinates for cropping the image to the correct frame (manually generated from a captured example) for offline strategy
# left =  4 #70  # x left
# top = 6 #55  # y top
# right = 234 #265 #255  # x right
# bottom = 236 #240  # y bottom
# Cropping for online strategy
left =  6  # x left
top = 95  # y top
right = 81 #265 #255  # x right
bottom = 167 #240  # y bottom
# the coordinates to crop images with social cues from pepper
p_left =  20 #70  # x left
p_top = 40 #55  # y top
p_right = 570 #265 #255  # x right
p_bottom = 440 

# time variables these are magic numbers that I trialled
time1 = 0.5  # time sleep after grid is shown
time2 = 0.5  # time to wait after image display
time3 = 0.3 # time wait after grid display. the initial value was 2, ewduce to 1
time4 = 0.3 # the initial value was 2, reduce to 1.
time5 = 0.5 # 5
time6 = 0.5
time7 = 1


length = 11  # the length of the game grid
# Note: width x length images need to be located in get_gameimages, named 0.png to width x length in integers
nruns = 10 # number of runs -- episodes
iterations = 20 # iteration to run the SARSA for
repeats = 6 # new repeat = new q-matrix for this 'run'. We set repeats to 3 for online experiments, and to 10 for offline experiments.
rsize = (32, 32)  # size of the images, the images displayed on screen should be in the same format
ntrainimgs = 5  # number of images that the Hopfield net is trained with
epsilon = 0.3  # exploration parameter
gamma = 0.4  # discounting
probabilities = (0, 0.05, 0.1, 0.2, 0.25, 0.5, 0.6, 0.75, 0.7, 0.8, 0.85)
state_numbers = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
experiment_online=True


#audio constants
fs = 44100  # Sample rate
seconds = 3  # Duration of recording
conditions = ['Trustworthy', 'Untrustworthy', 'Deceptive', 'Random']
audio_labels = ['sweet candy',  'shiny star', 'big heart', 'fast car', 'sharp scissors']
state_labels = ['L 5',  'L 4', 'L 3', 'L 2', 'L 1', '0', ' R 1', 'R 2', 'R 3', 'R 4', 'R 5']









