# 环境修复策略报告

## 一、最小修复方案（HYZ-mini）

目标：尽量少修改 requirements_broken.txt，使其能够成功安装

修改内容：

1. 删除 python==3.11  
原因：Python 不能通过 pip 安装，应由 conda 管理

2. 修改 sklearn==0.0 → scikit-learn  
原因：sklearn 不是实际包名

3. 修改 numpy==1.26.4 → 1.23.5  
原因：numba 0.56.4 仅支持 numpy <1.24

4. 修改 torchvision==0.10.0 → 0.17.0  
原因：需匹配 torch 2.2.0

5. 删除 tensorflow  
原因：依赖复杂，易冲突

---

## 二、工程修复方案（HYZ-project）

目标：构建稳定的深度学习环境（用于 YOLO / PyTorch）

设计原则：

- 使用 Python 3.9（兼容性最好）
- 使用 conda 安装核心库
- 使用 pip 安装补充库

---

## 三、conda 与 pip 分工

conda 安装：

- python
- torch
- torchvision
- numpy

pip 安装：

- opencv-python
- matplotlib
- scikit-learn
- jupyter

原因：

- conda 更适合管理底层依赖
- pip 适合安装纯 Python 包

---

## 四、关键问题解释

### 为什么不能用 sklearn==0.0

因为 sklearn 只是占位包，真正的库是 scikit-learn

---

### 为什么 torch / torchvision 不能乱配

它们是强依赖关系，版本必须匹配，否则会报错

---

### GPU / CPU 选择

- 有 GPU：安装 CUDA 对应版本
- 无 GPU：使用 CPU 版本（当前环境）

---

## 五、总结

- 避免 pip 安装底层依赖
- 保持版本兼容
- 使用 conda 管理环境