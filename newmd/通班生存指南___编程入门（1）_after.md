通班生存指南 | 编程入门（1）
================

原创 PKU通班 PKU通班 2025-08-07 18:05 北京

> 原文地址: [https://mp.weixin.qq.com/s/9HSa6lKU5u6h5amuhoJE9A](https://mp.weixin.qq.com/s/9HSa6lKU5u6h5amuhoJE9A)

  

![](https://cdn.jsdelivr.net/gh/gky0329/tong-image-repo@main/tongbanshengcunzhinan_bianchengrumen_1-1.png)

![](https://cdn.jsdelivr.net/gh/gky0329/tong-image-repo@main/tongbanshengcunzhinan_bianchengrumen_1-2.png)

![](https://cdn.jsdelivr.net/gh/gky0329/tong-image-repo@main/tongbanshengcunzhinan_bianchengrumen_1-3.png)

[

![](https://cdn.jsdelivr.net/gh/gky0329/tong-image-repo@main/tongbanshengcunzhinan_bianchengrumen_1-4.png)



](https://mp.weixin.qq.com/s?__biz=Mzk1Nzg0MzM0OQ==&mid=2247484387&idx=1&sn=948077f643e2d1c03b1d1acbacbe3255&scene=21#wechat_redirect "https://mp.weixin.qq.com/s?__biz=Mzk1Nzg0MzM0OQ==&mid=2247484387&idx=1&sn=948077f643e2d1c03b1d1acbacbe3255&scene=21#wechat_redirect")

  

  

![](https://cdn.jsdelivr.net/gh/gky0329/tong-image-repo@main/tongbanshengcunzhinan_bianchengrumen_1-5.png)

请滑动翻阅来自通班的信～

  

_**01**_

  

**Conda, VS Code, SSH**

  

😀

Python是我们实践人工智能的主要编程语言，与此同时很多工具可以帮助我们更高效地学习编程和进行人工智能项目的开发。下面这份指南包括Conda环境配置的基础，VS Code编辑器的安装与使用，以及通过SSH远程开发的详细步骤，帮助你在本地和服务器间无缝切换，高效完成AI项目。

📝 搞定环境：别让配置拖你后腿
================

环境隔离的意义：每个项目使用独立的虚拟环境，避免依赖冲突，保证复现性。

### 1\. 安装 Miniconda

1.  访问 **Miniconda 官网\[1\]**，下载对应系统的安装包。
    
      
    
    _（https://docs.conda.io/en/latest/miniconda.html_）
    
      
    
2.  按照官网指引执行安装（Windows 双击 .exe，macOS/Linux 终端运行 bash Miniconda3-latest-MacOSX-x86\_64.sh）。
    
3.  安装完成后打开终端，输入 conda --version 确认安装成功。
    
4.  注意：Miniconda是Anaconda的一个精简版，更容易控制包的版本和数量，可以避免臃肿、节省硬盘空间。如果需要快速拥有完整的数据科学工具栈（Jupyter, NumPy, pandas, matplotlib, scikit-learn 等），可以选装Anaconda。
    

### 2\. 创建与管理 Conda 环境

  

  

  

\# 创建环境，指定 Python 3.10  

conda create \-n tong python\=3.10  

\# 激活环境  

conda activate tong  

\# 安装常用库  

conda install pytorch torchvision torchaudio \-c pytorch 

conda install numpy matplotlib jupyterlab tqdm

*   保存环境： conda env export > environment.yml
    
*   恢复环境： conda env update -f environment.yml
    
*   删除环境： conda remove -n tong --all
    
*   加速安装：安装 **mamba\[2\]** 后使用 mamba install ...  
    
    （_https://github.com/mamba-org/mamba_）
    

📝 选对编辑器：VS Code + 插件生态
=======================

VS Code 轻量易用，插件丰富，尤其适合 AI 开发。

### 1\. 安装 VS Code

*   访问 **VS Code 官网\[3\]**，下载并安装。
    
      
    
    _（https://code.visualstudio.com/_）
    
      
    
*   启动后，按 Ctrl+Shift+X 打开插件市场。
    

### 2\. 必装插件推荐

插件名称

功能简介

Python

语法高亮、Lint、调试、环境切换

Jupyter

在编辑器中运行 Notebook

Pylance

智能提示、类型检查

GitLens

版本控制可视化

GitHub Copilot

AI 代码补全

Cursor 或 Codeium

另外的 AI 编程助手（可选）

安装方法：在插件搜索框输入名称，点击安装。

### 3\. 配置 VS Code 使用 Conda 环境

1.  在 VS Code 中打开一个 Python 文件或 Notebook，左下角会显示当前解释器。
    
2.  点击并选择 “Python: Select Interpreter”，选择 conda 环境下的 python.exe 或 python。
    
3.  配置 .vscode/settings.json（可选）：
    

  

  

  

{"python.defaultInterpreterPath":"/Users/yourname/miniconda3/envs/tong/bin/python","python.linting.enabled":true,"python.linting.pylintEnabled":true}

📝 SSH 远程开发：随时随地跑你的代码
=====================

当模型训练需要更强算力，或多人协作时，远程服务器/云主机是必备工具。VS Code 的 Remote - SSH 插件让你像在本地一样编辑远程代码。

### 1\. SSH 密钥管理

1.  在本地生成 SSH 密钥（若已有可跳过）：
    

  

  

  

ssh-keygen -t ed25519 -C "your\_email@example.com"  

\# 默认保存在 ~/.ssh/id\_ed25519

1.  将公钥添加到服务器（假设用户名 user，服务器地址 server.com）：
    

  

  

  

ssh-copy-id user@server.com  

# 或者手动将 ~/.ssh/id\_ed25519.pub 的内容追加到服务器

 ~/.ssh/authorized\_keys

1.  测试连接： ssh user@server.com，若直接登录则配置成功。
    

### 2\. 配置 SSH 客户端

编辑本地 ~/.ssh/config，添加：

  

  

  

Host myserver     HostName server.com     User user     IdentityFile ~/.ssh/id\_ed25519     ForwardAgent yes

这样以后可通过 ssh myserver 连接。

### 3\. 在 VS Code 中使用 Remote - SSH

1.  点击左下角绿色 >< 图标，选择 “Remote-SSH: Connect to Host...”
    
2.  选择 myserver，VS Code 将自动在远程端安装必要组件。
    
3.  连接成功后，你可以像在本地一样打开、浏览、编辑服务器上的文件。
    

### 4\. 远程终端与端口转发

*   在 VS Code 中打开远程终端：Ctrl+Shift+~，即可使用远程 Shell。
    
*   训练模型时常需启动 TensorBoard 或 JupyterLab，使用端口转发：
    

1.  在本地机器运行： ssh -NL 8888:localhost:8888 myserver
    
2.  在 VS Code 端口面板添加转发，也可通过 Remote-SSH 自动检测端口。
    
3.  浏览器访问 http://localhost:8888 查看远程服务。
    

📝 推荐工作流示例
==========

1.  本地开发：在 VS Code 本地打开项目，切换到 conda 环境，写小脚本、调试。
    
2.  同步代码：使用 Git 推送到远程仓库（GitHub/GitLab）。
    
3.  远程训练：通过 VS Code Remote-SSH 登录服务器，在服务器环境中执行训练脚本。
    
4.  监控与调试：结合端口转发实时查看 TensorBoard、Jupyter、或其他可视化页面。
    
5.  结果同步：训练完成后，将模型文件 scp 或者 Git LFS 同步回本地。
    

环境+编辑器+SSH 组合，让你的 AI 工程之路更加稳定、高效，不再被琐碎配置和远程连接问题绊倒。祝你编程愉快，早日跑出第一个AI项目！

  

### 参考资料

\[1\]

Miniconda 官网: _https://docs.conda.io/en/latest/miniconda.html_

\[2\]

mamba: _https://github.com/mamba-org/mamba_

\[3\]

VS Code 官网: _https://code.visualstudio.com/_

  

_**02**_

  

**Git与GitHub**

  

🎈

在刚开始接触编程的阶段，Git和Github常常让人感到陌生甚至困惑。但随着项目的积累和协作的需要，它们会逐渐成为你日常开发中不可或缺的工具。掌握版本控制不仅能帮助你更好地管理代码，更是进入更高效开发流程的第一步。本文将带你从基础出发，初步了解Git的使用方法，为之后的学习与项目实践打下扎实的基础。

📝 Git的基本操作
===========

Git是什么
------

Git是一个分布式版本控制系统，用于记录和管理代码的变化过程。它的核心目标是帮助开发者追踪项目中的每一次修改、便捷地回退历史版本，以及实现多人协作开发时的分支管理与合并。

在Git的工作机制中，有几个重要的区域：

1.  工作区：就是你当前编辑代码的目录，所有实际的修改都发生在这里。
    
2.  暂存区：也叫缓存区。你可以选择将部分改动加入暂存区，这样做的目的是将修改进行打包，准备好之后再一起提交（到与他人共享的远程仓库，例如后文我们会提到的GitHub）。
    
3.  本地仓库：当你执行 git commit 时，暂存区中的内容就会被正式保存到本地仓库，形成一次不可更改的提交记录（commit）。每个 commit 都有唯一的 ID，记录了修改的内容、时间、作者等信息。
    
4.  远程仓库：存放在网络服务器上的Git仓库，例如 GitHub、GitLab或Gitee（当然你也可以自己租用服务器搭建属于你的Git远程仓库），用于与他人共享代码。当你执行git push时，本地仓库中的提交会被上传到远程仓库，使团队成员可以获取、查看或协作开发相同的项目。远程仓库通常被命名为origin。
    

💡

对团队协作而言，Git提供了统一的代码历史，并在多人修改时提供清晰的冲突检测与合并机制。这对于多人合作是十分重要的。

在Git中，我们会涉及到一些专有名词：

*   add：将工作区中的改动添加到暂存区，为提交做准备。
    
*   commit：将暂存区的更改提交为一次快照，保存在本地仓库中。
    
*   push：将本地仓库中的提交上传到远程仓库。
    
*   pull：从远程仓库获取最新的提交，并合并到当前分支。
    
*   merge：将一个分支的更改整合到当前分支上。
    
*   clone：从远程仓库复制一个完整的 Git 仓库到本地。
    
*   branch：分支，用于并行开发（见后文）。
    
*   conflict：在合并过程中发生的修改冲突。
    
*   stash：暂时保存当前修改，以便切换到其他分支后再恢复。
    
*   remote：远程仓库的别名（如 origin），用于标识你与哪个远程仓库交互。
    

Git的基本命令
--------

接下来，我们简单介绍一下我们在使用Git时经常使用的一些基本命令。

### 初始化仓库

  

  

  

git init

这个命令会在当前目录下初始化一个Git仓库，生成.git隐藏文件夹，开始进行版本控制。

* * *

### 查看当前状态

  

  

  

git status

这个命令可以用于查看当前仓库下有哪些文件发生了变化、哪些已经被追踪、哪些准备提交。

* * *

### 添加变更到暂存区

  

  

  

git add <filename>  

\# 或添加全部变更 ↓  

git add .

将修改添加到暂存区，为提交做准备。

* * *

### 提交更改

  

  

  

git commit\-m "简要说明这次提交的内容"

将暂存区的内容提交到仓库中，形成一次新的版本记录。

* * *

### 查看提交历史

  

  

  

git log

查看当前仓库的提交历史，包括提交人、时间和提交信息。

* * *

### 关联远程仓库

  

  

  

git remote add origin <https://github.com/username/repo.git>

将本地仓库与远程仓库进行关联。其中，尖括号所包裹的内容是远程仓库的地址，我们会在后文讲述。

* * *

### 分支

在Git中，分支（branch）就像是你代码的一个“平行宇宙”。每个分支都是从某个commit出发形成的一条独立修改线。有了分支，你就可以在不影响主线（如main或master）的前提下，在自己的分支尝试新功能、DeBug，最后再决定是否合并到主分支。

最常见的分支操作流程：

  

  

  

git branch dev          \# 创建一个名为 dev 的分支  

git checkout dev        \# 切换到 dev 分支  

\# 在 dev 分支上做修改并提交  

git checkout master     \# 切换回主分支  

git merge dev           \# 把 dev 的改动合并回来

* * *

### 推送到远程仓库

  

  

  

git push -u origin master

将本地的提交推送到远程仓库，通常用于首次推送。

* * *

### 拉取远程更新

  

  

  

git pull

从远程仓库拉取最新的更新并合并到本地分支。

📝 Git的本地配置与ssh秘钥
=================

在将本地仓库上传至远程之前，我们需要先完成基本的用户身份配置，设置SSH密钥以便安全地连接远程仓库。

* * *

配置用户名和邮箱
--------

首先我们需要先配置本地的Git用户名和邮箱，Git使用这两个信息来标识每一次提交的作者。

  

  

  

git config --global user.name "你的名字"  

git config --global user.email "你的邮箱地址"

设置完后，你的每次 commit 都会带上这个身份信息。\--global表示这个设置对你当前用户的所有仓库生效。

你可以使用以下指令检查配置：

  

  

  

git config\--list

  

生成SSH密钥
-------

ssh是一种加密通信协议，最初用于远程登录服务器。在Git中，SSH被用作一种安全的身份认证方式，用于在你和远程仓库之间传输代码时确认你的身份。

SSH 使用一对密钥来验证身份：

*   私钥（private key）：保存在你自己的电脑上，严禁泄露。
    
*   公钥（public key）：上传到远程仓库网站（如 GitHub）。
    

验证方式如下：

当你执行git push时，GitHub会查看你发送请求的设备是否持有对应的私钥。如果和它存储的公钥匹配，验证通过。

  

一台设备理论上只需要一个ssh秘钥，后续其他需要ssh的场景可重复使用之前生成的秘钥。我们可以通过以下指令生成一对ssh秘钥：

  

  

  

ssh-keygen -t ed25519 -C "你的邮箱地址"

按提示一路回车即可。生成的密钥会保存在：

  

  

  

~/.ssh/id\_ed25519       （私钥，不能泄露） 

~/.ssh/id\_ed25519.pub   （公钥，可安全公开）

添加SSH公钥到GitHub
--------------

接下来，我们将SSH公钥上传至远程仓库，使得远程仓库平台能够识别我们的身份。

1.  打开 ~/.ssh/id\_ed25519.pub 文件，复制里面的全部内容。
    
2.  登录 GitHub → 点击头像 → Settings → SSH and GPG keys。
    
3.  点击 New SSH key，粘贴公钥，保存即可。
    

可以通过以下指令测试SSH是否配置成功

  

  

  

ssh -T git@github.com

如果配置成功，你会看到一段提示：

  

  

  

Hi Your-Username! You've successfully authenticated, but GitHub does not provide shell access.

完成这些配置后，你就可以通过 SSH 的方式与 GitHub 通信了，后续使用 git push、git pull 时无需每次输入账号密码，既安全又便捷。

📝 GitHub上的基本操作
===============

GitHub是一个国外的基于Git的远程代码托管平台，其URL为**github.com\[1\]**。（https://github.com/）国内裸连GitHub是一件很看运气的事情，最稳妥的方法还是使用一些科学上网手段。

在使用GitHub前，你需要先注册账号（并最好完成学生认证）。在注册好账号之后，你就可以点击右上角 + → New repository 创建新远程仓库了。在创建仓库过程中，你需要填写仓库名称、描述，选择是否公开（public）或私有（private，即非你授权的用户不可见），点击 Create repository创建。

创建与上传仓库（Repo）
-------------

创建仓库后，你可以通过SSH或HTTPS地址克隆到本地：

  

  

  

git clone git@github.com:username/repo.git   \# SSH  

\# 或  

git clone https://github.com/username/repo.git  \# HTTPS

上面的链接可以在仓库中”Code”按钮中找到。如图，在点开”Code“按钮后，GitHub会提供HTTPS/SSH的下载链接，以及直接Download Source(源代码)的入口。

  

如果你已经在本地创建好了仓库，也可以直接推送本地修改到GitHub：

  

  

  

git add . 

git commit\-m "Initial" 

git push \-u origin main

后续推送时，push -u可改用为push以简化操作：

  

  

  

git push

点击仓库中的 Commits 或单个文件中的 History，可以查看历史提交记录。每次提交都可以展开查看差异（diff）和修改内容。

创建合并请求 Pull Request（PR）
-----------------------

*   创建一个分支并在该分支中进行修改提交；
    
*   提交后在GitHub的仓库页面点击Compare & pull request创建PR，请求合并到主分支；
    
*   审核通过后可以点击Merge pull request自动在远程完成合并。
    

Star / Watch / Fork / Issues
----------------------------

*   Star：表示你喜欢该项目；
    
*   Watch：订阅项目更新；
    
*   Fork：复制项目到你自己的账户下，进行独立开发，适合参与开源项目或保留副本；你可以用git clone将其克隆到本地进行进一步开发；
    
*   Issues：问题追踪与任务管理系统（类似于发帖），用于记录bug、功能请求、想法讨论或待办事项。
    

* * *

最后，想将国内代码托管平台Gitee的Slogan分享给大家：

💡

让每一行代码，都有改变世界的力量！

Happy coding~ 🚀💻✨

### 参考资料

\[1\]

github.com: _https://github.com/_

  

关于通班：

[北京大学通用人工智能实验班：通识、通智、通用](https://mp.weixin.qq.com/s?__biz=Mzk1Nzg0MzM0OQ==&mid=2247484387&idx=1&sn=948077f643e2d1c03b1d1acbacbe3255&scene=21#wechat_redirect)

  

撰稿 | 李嘉豪 严绍恒

封面 | 严绍恒

排版 | 陈应涵 陈旭峥

PKU通班
