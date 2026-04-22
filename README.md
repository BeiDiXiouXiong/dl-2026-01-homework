# 依赖冲突分析报告（conflict_analysis.md）

---

## 一、实验背景

在使用 Conda 创建 Python 3.11 环境后，尝试执行：

```bash
pip install -r requirements_broken.txt

过程中出现依赖解析失败（ResolutionImpossible），说明当前依赖列表存在多个冲突问题。

二、问题分析

本次共定位出 5 个关键依赖问题，分别属于不同类型。

问题1：numba 与 numpy 版本冲突（依赖版本冲突）
现象

报错信息：

numba 0.56.4 depends on numpy <1.24 and >=1.18
但 requirements 中指定 numpy==1.26.4
原因分析
numba==0.56.4 对 numpy 有严格版本要求：必须小于 1.24
但 requirements 文件中强制指定 numpy==1.26.4
导致 pip 无法找到同时满足两者的版本组合
问题类型

依赖版本冲突（package version conflict）

问题2：sklearn==0.0（错误包名问题）
现象

requirements 中包含：

sklearn==0.0
原因分析
sklearn 只是一个占位包（meta package）
实际应使用的是 scikit-learn
sklearn==0.0 并不包含真正功能代码
问题类型

错误包名（package naming issue）

问题3：torch 与 torchvision 版本不匹配（库兼容性问题）
现象

requirements 中：

torch==2.2.0
torchvision==0.10.0
原因分析
torchvision 版本必须与 torch 严格对应
torchvision==0.10.0 对应的是较早版本的 torch（约1.x）
与 torch==2.2.0 完全不兼容
影响

可能出现：

安装失败
或运行时报错（API 不匹配）
问题类型

库版本不兼容（library compatibility issue）

问题4：tensorflow 与 Python 版本冲突（Python版本问题）
现象

requirements 中：

tensorflow==2.10.0
python==3.11
原因分析
TensorFlow 2.10 官方仅支持 Python ≤ 3.10
当前环境使用 Python 3.11
pip 无法找到适配版本
问题类型

Python版本不兼容（Python compatibility issue）

问题5：pip 试图解析 python 版本（工具使用问题）
现象

requirements 中：

python==3.11
原因分析
pip 无法安装 Python 本身
Python 版本必须由 conda 或系统环境控制
将 python 写入 requirements 是错误用法
问题类型

工具使用错误（tool misuse）

三、conda 与 pip 解析差异
pip 特点
仅根据当前环境解析依赖
不会自动降级 Python
容易出现 ResolutionImpossible
conda 特点
同时管理 Python + 依赖包
能自动选择兼容组合
更适合构建完整环境
结论
Python、numpy、pytorch 等核心库建议使用 conda 安装
其余轻量库可使用 pip 安装
四、小结

本次依赖失败的根本原因是：

版本约束冲突（numba vs numpy）
包名错误（sklearn）
深度学习框架版本不匹配（torch vs torchvision）
Python版本不兼容（tensorflow）
工具使用错误（pip 管理 python）

这些问题共同导致 pip 无法解析依赖关系，从而安装失败。