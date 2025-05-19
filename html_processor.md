# HTML文件处理应用使用指南

我已经在桌面上创建了一个名为`html_processor.py`的Python脚本，下面是将其设置为右键菜单可用的应用程序的步骤：

## 步骤一：确保Python脚本可执行

1. 打开终端
2. 执行以下命令：
```bash
chmod +x ~/Desktop/html_processor.py
```

## 步骤二：创建macOS应用程序

### 方法一：使用Automator（推荐）

1. 打开Automator（在应用程序文件夹中）
2. 选择"新建文稿"
3. 选择"应用程序"
4. 在左侧搜索"运行Shell脚本"并将其拖到右侧工作区
5. 在Shell脚本框中输入：
```bash
for f in "$@"
do
  /usr/bin/env python3 /Users/bruce/Desktop/html_processor.py "$f"
done
```
6. 选择"文件" > "存储"，将应用程序保存为"HTML处理器.app"到应用程序文件夹
7. 关闭Automator

### 方法二：使用PyInstaller（需要额外安装）

如果你更喜欢这种方法，请在终端执行：
```bash
pip install pyinstaller
cd ~/Desktop
pyinstaller --onefile --windowed html_processor.py
```
生成的应用将在`~/Desktop/dist`目录中

## 步骤三：将应用设置为HTML文件的打开方式

1. 在Finder中，找到任意HTML文件
2. 右键点击，选择"显示简介"或"获取信息"
3. 在"打开方式"部分，选择你刚创建的"HTML处理器"应用
4. 点击"全部更改..."按钮，将所有HTML文件默认用此应用打开

## 使用说明

1. 当你右键点击任何HTML文件并选择打开方式，或直接用HTML处理器打开时，会弹出一个对话框
2. 输入你想要的新文件名（无需输入.html后缀）
3. 点击确定后，应用会：
   - 将文件复制到`/Users/bruce/git/xiaobu/ai`目录下
   - 使用新文件名重命名
   - 在`/Users/bruce/git/xiaobu`目录下执行`push.sh`脚本提交更改
4. 操作成功或失败都会显示相应提示

## 注意事项

- 确保`/Users/bruce/git/xiaobu/push.sh`脚本存在且有执行权限
- 确保目标目录`/Users/bruce/git/xiaobu/ai`已存在或有权限创建
- 应用需要访问文件系统的权限，首次运行时可能需要授权