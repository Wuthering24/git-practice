Git 与代码版本管理 实践笔记


一、学习资料来源
Git 官方文档 (https://git-scm.com/doc)
菜鸟教程 Git 教程 (https://www.runoob.com/git/git-tutorial.html)
廖雪峰 Git 教程 (https://liaoxuefeng.com/books/git/introduction/)
部分命令行操作参考了课堂上老师推荐的博客文章
运用了Ai帮助我更好得了解代码的使用方式


二、实践流程

Git 环境配置
从 Git 官网下载 Windows 版本并安装。打开 Git Bash，配置用户名和邮箱：
git config --global user.name "Wuthering24"
git config --global user.email "3039358109@qq.com"

创建本地仓库
在用户目录下新建文件夹 git-practice：
mkdir ~/git-practice
cd ~/git-practice
git init

编写代码并进行多次提交

第一次提交：
创建 hello.c 文件，内容为一个简单的 C 语言程序。添加到暂存区并提交：
git add hello.c
git commit -m "第一次提交：添加hello.c"

第二次提交：
使用 Git Bash 自带的 vim 编辑器修改 hello.c，增加注释和输出语句。提交：
git add hello.c
git commit -m "第二次提交（使用vim编辑器）：更新了hello.c"

第三次提交：
将之前编写的一个“本地文旅推荐系统”项目的相关文件复制到仓库中。为了结构清晰，将这些文件统一放入一个名为“本地文旅推荐系统”的文件夹：
mkdir 本地文旅推荐系统
mv config.json main.py recommendation_visualization.png test_cases.md tourism_data.json 本地文旅推荐系统/
提交：
git add 本地文旅推荐系统/
git commit -m "第三次提交：添加本地文旅推荐系统完整代码及数据"

创建远程仓库并推送
登录 GitHub，新建一个公开仓库，命名为 git-practice。复制仓库地址：https://github.com/Wuthering24/git-practice.git
在本地关联远程仓库并推送：
git remote add origin https://github.com/Wuthering24/git-practice.git
git push -u origin master
推送成功，所有提交记录已同步到 GitHub。


三、每次提交的主要内容说明

提交序号 1：第一次提交：添加hello.c
主要内容：创建基础的 C 语言程序文件

提交序号 2：第二次提交：使用vim编辑器更新hello.c
主要内容：增加函数及注释，完善代码结构

提交序号 3：第三次提交：添加本地文旅推荐系统完整代码及数据
主要内容：包含配置、主程序、测试用例、数据文件及效果图，整理到单独文件夹


四、遇到的问题及解决方法

问题1：在 PowerShell 中输入 vim hello.c 报错“vim 不是可运行程序”
原因：Windows 默认的 PowerShell 不带 vim 编辑器。
解决方法：改用 Git Bash（Git 安装时自带）执行 vim 命令；或者直接用 Windows 记事本（notepad hello.c）编辑文件。后续所有 Git 操作都统一在 Git Bash 中完成，避免了此类问题。

问题2：在 PowerShell 中使用 rm -f hello.c 报错“参数名称具有二义性”
原因：PowerShell 的 Remove-Item 命令无法识别 -f 参数（它期望的是 -Force）。
解决方法：改用 del hello.c 删除文件，或者切换到 Git Bash 环境（它支持 Linux 风格的 rm -f）。之后我全程使用 Git Bash，命令行习惯更一致。

问题3：执行 git commit -m 时忘记写提交信息，报错“switch 'm' requires a value”
原因：-m 参数后面必须紧跟用双引号括起来的提交说明。
解决方法：每次提交前先写好简短的提交信息，例如 git commit -m "修改了xxx功能"。若需要写较长的说明，可以不带 -m 直接使用 git commit 进入 vim 编辑器。

问题4：git add 后提示“LF will be replaced by CRLF”
原因：我的文件在Git Bash上使用 LF 换行符，而 Git 在 Windows 上默认会将其转为 CRLF。
解决方法：这是正常提示，不影响实际使用。我执行了 git config --global core.autocrlf true 让 Git 自动处理换行符，之后不再出现警告。


五、Git 学习心得
通过这次读书实践周的练习，我从一个完全不会版本控制的新手，到现在能够尝试独立完成：
１.本地仓库的创建与管理
２.多次提交并查看历史记录
３.关联远程仓库并推送代码
４.解决常见命令行与环境问题
５.有所体会到 Git 相比传统复制文件夹备份的优势：可追溯：每次提交都有清晰的说明和唯一 ID，可以随时回到任意历史版本；可协作：远程仓库让多人同时开发成为可能，分支管理能避免代码冲突；安全备份：代码托管在 GitHub 上，即使本地文件丢失也能恢复；另外，我也意识到 README.md 是一个项目的关键，规范的文档不仅方便自己日后回顾，也能帮助他人快速了解项目内容。以后在写其他课程作业或项目时，我也会尝试使用 Git 进行版本管理，以养成良好的提交习惯。下一步我想继续学习分支管理（git branch、git merge）和解决冲突的方法，为接下来的团队合作做准，提供创新的方法。

