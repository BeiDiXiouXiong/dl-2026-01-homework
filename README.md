# 依赖冲突分析报告（conflict_analysis.md）

---

## 问题 1：`numba` 与 `numpy` 版本硬冲突（依赖版本约束冲突）
- **原因分析**：
  `numba==0.56.4` 对 `numpy` 存在严格版本限制，要求 `numpy < 1.24`；但 `requirements_broken.txt` 中强制指定了 `numpy==1.26.4`，两者的版本区间无交集，导致 pip 无法找到同时满足两者的版本组合。
- **问题类型**：
  依赖版本硬冲突（Package Version Conflict）

---

## 问题 2：`sklearn==0.0` 无效包名（包命名错误）
- **现象**：
  `requirements_broken.txt` 中包含 `sklearn==0.0`
- **原因分析**：
  `sklearn` 是一个仅用于引导用户安装 `scikit-learn` 的占位元包（meta-package），本身不包含任何功能代码；`sklearn==0.0` 不是一个合法的功能包版本，会导致安装逻辑混乱。
- **问题类型**：
  错误包名（Package Naming Issue）

---

## 问题 3：`torch` 与 `torchvision` 版本不兼容（框架依赖不匹配）
- **现象**：
  `requirements_broken.txt` 中指定：
  ```text
  torch==2.2.0
  torchvision==0.10.0
原因分析：
---
torchvision 的版本必须与 torch 严格对应：torchvision==0.10.0 仅兼容 torch 1.9.x 系列版本，与 torch==2.2.0 完全不匹配。这会导致安装失败，或即使安装成功，运行时也会因 API 不兼容报错。

问题类型：
---
库版本兼容性问题（Library Compatibility Issue）

问题 4：tensorflow==2.10.0 与 Python 3.11 不兼容（Python 版本约束冲突）
---
现象：
---
requirements_broken.txt 中指定 tensorflow==2.10.0，但当前环境为 Python 3.11。

原因分析：
---
TensorFlow 2.10 的官方支持列表中，最高仅兼容 Python 3.10，未提供 Python 3.11 的预编译包，pip 无法找到适配版本。

问题类型：
---
Python 版本不兼容（Python Version Compatibility Issue）

问题 5：python==3.11 写入 requirements（工具使用错误）
---
现象：
requirements_broken.txt 中包含 python==3.11

原因分析：

pip 仅用于管理 Python 包，无法安装或修改 Python 解释器版本；Python 版本需由 Conda 或系统环境控制，将其写入 requirements.txt 是错误用法，会导致依赖解析逻辑混乱。

问题类型：

工具使用错误（Tool Misuse）

三、Conda 与 pip 依赖解析机制差异
---
表格
对比维度	pip	Conda

解析范围	仅基于当前 Python 环境解析包依赖	同时管理 Python 解释器 + 所有依赖包

Python 版本	无法自动调整 Python 版本	可自动选择兼容的 Python 与包组合

冲突处理	版本约束冲突时直接抛出 ResolutionImpossible	可在兼容区间内自动降级 / 升级包以解决冲突

适用场景	轻量纯 Python 包、无复杂编译依赖	深度学习框架（PyTorch/TensorFlow）、科学计算库、多依赖链环境

结论：Python 解释器、numpy、PyTorch/TensorFlow 等核心依赖建议优先使用 Conda 安装；轻量纯 Python 库可通过 pip 安装，以降低依赖冲突风险。

四、冲突根源总结
---
本次安装失败的核心原因可归纳为 5 类典型问题：
---
硬版本约束冲突：numba 与 numpy 的版本区间无交集；

包名错误：使用无效的占位包 sklearn 而非 scikit-learn；

深度学习框架依赖不匹配：torch 与 torchvision 版本未严格对齐；

Python 版本不兼容：tensorflow==2.10.0 不支持 Python 3.11；

工具使用逻辑错误：将 python 解释器版本写入 requirements.txt。

这些问题共同导致 pip 无法构建出兼容的依赖树，最终引发安装失败。
