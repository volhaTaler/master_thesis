#!/bin/sh

MODEL_PATH="gesture_model_30_11.pkl"

/home/volha/miniconda3/envs/env_py3/bin/python3.8 model_prediction.py $1 $MODEL_PATH

