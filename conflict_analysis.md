# 环境修复策略

## 一、最小修复方案（HYZ-mini）

目标：尽量少改 requirements_broken.txt，使其能安装成功

### 修改内容：

1. 删除 python==3.11  
原因：pip 无法安装 Python  

2. 修改 sklearn==0.0 → scikit-learn  
原因：sklearn 不是正式包  

3. 修改 numpy==1.26.4 → numpy==1.23.5  
原因：兼容 numba  

4. 修改 torchvision==0.10.0 → 0.17.0  
原因：匹配 torch 2.2  

5. 删除 tensorflow  
原因：依赖复杂，易冲突  

---

## 二、工程修复方案（HYZ-project）

目标：构建稳定的深度学习环境（用于 YOLO）

### 设计原则：

- 使用 Python 3.9（兼容性最好）
- 使用 conda 安装核心库（torch、numpy）
- 使用 pip 安装补充库

---

## 三、conda 与 pip 分工

### conda 安装：

- python
- numpy
- pytorch
- torchvision

### pip 安装：

- opencv-python
- scikit-learn
- jupyter

---

## 四、关键问题解释

### 为什么不能用 sklearn==0.0

因为 sklearn 不是实际包，真正包是 scikit-learn。

---

### 为什么 torch / torchvision 不能乱配

它们是强依赖关系，版本必须严格对应，否则运行报错。

---

### GPU / CPU 选择

- 有 GPU：安装 CUDA 对应版本  
- 无 GPU：使用 cpuonly  

---

## 五、总结

- 避免 pip 安装底层依赖
- 保持库版本兼容
- 尽量使用 conda 管理环境