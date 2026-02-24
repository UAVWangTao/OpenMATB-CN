# OpenMATB：多属性任务电池（MATB）开源版

**[English](README.md)**

多属性任务电池（MATB）最早见于 NASA 技术备忘录（Comstock & Arnegard, 1992），包含一组与飞机驾驶任务类似的交互任务。MATB 要求被试在电脑屏幕上同时完成四项任务：(1) 监控任务，(2) 跟踪任务，(3) 听觉通讯任务，(4) 资源管理任务。界面还包含 (5) 调度视图，用于显示即将到来的任务事件图表。

<img src=".img/capture.png" alt="OpenMATB 界面截图" width="600" />

自 MATB 首次实现（Comstock & Arnegard, 1992）以来已近三十年，现有研究对工具提出了新的需求。

OpenMATB 旨在提供多属性任务电池的开源重实现，并侧重三点：
1. **任务可定制**：完整适配实验需求；
2. **软件可扩展**：便于添加新功能；
3. **实验可复现**：支撑可靠结果。

上述内容详见：

Cegarra, J., Valéry, B., Avril, E., Calmettes, C., & Navarro, J. (2020) OpenMATB: A Multi-Attribute Task Battery promoting task customization, software extensibility and experiment replicability. *Behavior Research Methods*, 52, 1980–1990. https://doi.org/10.3758/s13428-020-01364-w

联系：<a href="mailto:julien.cegarra@univ-jfc.fr">julien.cegarra AT univ-jfc.fr</a>；<a href="mailto:benoit.valery@univ-jfc.fr">benoit.valery AT univ-jfc.fr</a>

## 运行环境

当前版本需要 Python 3.9，并依赖以下第三方库：

- [pyglet](https://github.com/pyglet/pyglet)
- [pyparallel](https://github.com/pyserial/pyparallel)
- [rstr](https://github.com/leapfrogonline/rstr)
- [pylsl](https://github.com/chkothe/pylsl)

程序可在 Windows、Mac 和 Linux 上运行。为完整使用跟踪任务，需要电脑和操纵杆。

## 跨平台安装

首先在电脑上 [安装 Python 3.9](https://www.python.org/downloads/)（或更高版本）。

在多数平台上，将本仓库克隆到本地目录后，用 pip 安装依赖。所需库及版本见 `requirements.txt`，可使用 pip 的 `-r` 参数一次性安装。

（Windows 下可将下面命令中的 `python` 改为 `py`。）

```bash
python -m pip install -r requirements.txt
```

然后使用 Python 3.9 运行 `main.py` 即可启动 OpenMATB。

```bash
python main.py
```

### 虚拟环境

若希望为项目使用独立的 Python 环境，可在本地仓库中创建虚拟环境，步骤见 [Python 官方文档](https://docs.python.org/3.9/tutorial/venv.html)。

**注意：** 虚拟环境目录需命名为 `.venv`。若使用其他名称，请同步修改 `main.py` 首行的 [shebang](https://docs.python.org/3.9/tutorial/appendix.html#tut-scripts)（`#! .venv/bin/python3.9`），以便直接执行时使用该环境。

创建并激活虚拟环境后，在其中安装依赖：

- **Linux**：`source .venv/bin/activate`
- **Windows**：`.venv\Scripts\activate.bat`（详见 [官方文档](https://docs.python.org/3.9/tutorial/venv.html)）。

激活虚拟环境后，按与“全局”安装相同的方式安装依赖：

```bash
python -m pip install -r requirements.txt
```

之后有两种运行方式：

1. 先激活 OpenMATB 的虚拟环境，在终端执行 `python main.py`；
2. 或直接执行 `main.py`，由 shebang 指定解释器（此时无需激活虚拟环境，且需将 `main.py` 设为可执行）。

### 使用编译版本（即将推出）

若不需要查看源码，可使用软件的编译版本，无需单独安装 Python 及依赖。

- **Linux**：[即将推出]()
- **Windows**：[即将推出]()

## OpenMATB 基本用法示例

*更详细的说明见下方“教程”中的 Wiki。*

运行主程序时，会读取 `config.ini` 中的变量：`language`、`screen_index`、`fullscreen`、`scenario_path` 等。其中最重要的是 `scenario_path`，它指定用于协议编排与设置的场景文本文件。

（当前提供法语 fr_FR、英语 en_EN 和简体中文 zh_Hans_CN 等语言包，也可自行 [参与翻译](https://github.com/juliencegarra/OpenMATB/wiki/Internationalization)。）

场景是一个文本文件，为每个模块（如系统监控任务）规定要执行的事件及其发生时间。例如下面这个简单场景会在开始时启动 MATB 的四个主任务，并在 2 分 30 秒后停止。（注意每条命令——本例中的 `start` 和 `stop`——都对应一个别名，如 `sysmon` 表示系统监控任务。）

*`includes/scenarios/basic.txt` 内容示例*：
```
0:00:00;sysmon;start
0:00:00;track;start
0:00:00;scheduling;start
0:00:00;resman;start
0:00:00;communications;start
0:02:30;sysmon;stop
0:02:30;track;stop
0:02:30;communications;stop
0:02:30;resman;stop
0:02:30;scheduling;stop
```

通过场景文件可以控制各任务/模块、修改参数并触发事件。掌握场景语法与模块选项后，即可更灵活地定制 OpenMATB 场景。详见 [场景编写教程](https://github.com/juliencegarra/OpenMATB/wiki/How-to-build-a-scenario-file)。

场景结束后，运行过程会以逗号分隔的 .csv 形式保存在 `sessions` 目录下。该日志包含分析场景与计算绩效所需的信息，格式如下：

```
logtime,totaltime,scenario_time,type,module,address,value
13869.194646,0,0,input,keyboard,ENTER,release
...
```

各模块的日志说明见 [日志文件说明](the log file)。

## 教程

更多使用说明请参阅 [项目 Wiki](https://github.com/juliencegarra/OpenMATB/wiki)。

## 主要更新

### 1.3+ 版本

**回放模式（新）**
- 完整会话回放：从日志文件回放已录制会话
- 回放模式下的文件选择界面与静音按钮
- 支持播放、暂停与拖动的回放进度条
- 快进
- 回放中支持说明与量表插件

**新功能**
- 场景命令 `system;pause`：在场景中直接触发暂停
- 新增通用触发插件
- 操纵杆按键映射：可将任意操纵杆按键设为插件响应键（如系统监控中的 scales-1-key）
- 可自定义插件区域的垂直边界
- `generic scales` 的 showvalue 参数：隐藏刻度滑块上的数值（默认隐藏）
- `generic scales` 中当标题与问题不同时显示问题标题
- 动态量表布局与滑块子容器分布
- `genericscales` 幻灯片支持键盘操作
- config.ini 未设置场景时，启动时显示场景选择器
- 通讯任务中改进的英语语音

**问题修复**
- 修复 `performance` 量表忽略 start 之后设置的参数 (#34)
- 修复场景将油泵按键设为默认值时小键盘键被移除 (#52)
- 修复 `communications` 语音语言切换 (#32)
- 修复 `track` 中的 automode (#57)
- 修复 Windows 下退出卡死
- 修复滑块控件在问卷页间残留
- 修复 pylsl 导入阻塞编译版
- 修复场景生成器的若干问题
- 防止音频加载导致崩溃

### 1.2 版本

**新插件/功能：**
- 各任务（系统监控、跟踪、通讯、资源管理）可通过 `automaticsolver` 参数由自动化接管；
- 调度模块可显示最多四条时间线（每任务一条）；
- 调度模块中计时器可隐藏或改为显示剩余时间；
- 任务插件可显示反馈（如 resman 油罐越界时将容差指示变红；communications 以绿/红框显示应答等）；
- 各任务可显示逾期未响应的告警（新参数）；
- 新增 labstreaminglayer 插件，通过 LSL 协议输出日志以便与生理信号同步；
- 新增 `performance` 插件，向被试显示整体绩效水平；
- 新增 `instructions` 模块，可在指定时间以 HTML 形式呈现说明与图片；
- `track` 支持反转操纵杆轴向；
- 跟踪准星路径与 Comstock & Arnegard (1992) 原始 MATB 算法一致；
- 移除 `equalproportions`，跟踪任务中宽高比例固定为相等；
- `pumpstatus` 已并入资源管理模块（`resman`）的 `displaystatus` 选项；
- 资源管理油泵状态改为 `on`/`off`/`failure`（替代 1/0/-1）；
- 系统监控量表箭头在正确检测后冻结 1.5 秒（与原始 MATB 一致）。

**其他变更：**
- 场景参数经类型校验（如 taskplacement 须在指定位置列表中）；
- 场景错误写入 `last_scenario_errors.log`；
- 不再强制场景末尾结束行，无待执行事件且所有模块停止后程序退出；
- 新增 `config.ini` 配置主参数（场景、语言、全屏等）；
- 由 PySide/PyQt 迁移至 pyglet；
- 支持 Escape 键 + 确认退出、P 键暂停；
- 可在 config.ini 中指定全局字体；
- 各任务 AOI 在启动时自动记录，可用 `highlight_aoi` 调试显示；
- 以会话 ID 替代 participantinfo，用于会话日志文件名；
- 新增场景生成器，便于设计难度递进场景；
- 各任务模块在数据可用时即记录绩效指标。
