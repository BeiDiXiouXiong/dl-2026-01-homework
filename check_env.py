import sys
import torch
import torchvision
import os

print("===== Environment Check =====")

# Python版本
print("Python version:", sys.version)

# Conda环境名
print("Conda env:", os.environ.get("CONDA_DEFAULT_ENV"))

# PyTorch
print("Torch version:", torch.__version__)
print("Torchvision version:", torchvision.__version__)

# CUDA
print("CUDA available:", torch.cuda.is_available())

if torch.cuda.is_available():
    print("GPU:", torch.cuda.get_device_name(0))
else:
    print("Device: CPU")