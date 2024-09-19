# simple_video_downloader

**English Description:**

`simple_video_downloader` is an easy-to-use video downloader that supports downloading videos from multiple platforms, including YouTube, Twitch, and Bilibili.

**中文描述：**

`simple_video_downloader` 是一个简单易用的视频下载器，支持从 YouTube、Twitch 和 Bilibili 等多个平台下载视频。

## Features / 特性

- Supports downloading videos from YouTube, Twitch, 和 Bilibili / 支持从 YouTube、Twitch 和 Bilibili 下载视频
- Manual proxy address configuration / 支持手动设置代理
- Supports multiple video formats / 支持多种视频格式
- Simple and intuitive graphical user interface / 简单直观的用户界面

## 安装说明 / Installation Instructions

1. **Clone the repository: / 克隆这个项目：**
   ```bash
   git clone https://github.com/204313508/simple_video_downloader.git
   ```

2. **Navigate to the project directory: / 进入项目目录：**
   ```bash
   cd simple_video_downloader
   ```

3. **Install dependencies: / 安装依赖：**
   ```bash
   pip install -r requirements.txt
   ```

4. **For Windows users: / 对于Windows用户：**
   - Download `ffmpeg.exe` from the [FFmpeg website](https://ffmpeg.org/download.html) and place it in the `ffmpeg` folder.
   - 从官网[FFmpeg website](https://ffmpeg.org/download.html)下载ffempeg.exe并将其放入ffmpeg文件夹中

5. **For Linux users: / 对于Linux用户：**
   - Modify the `check_ffmpeg_installed` function in `main.py` and set the `ffmpeg_location` during the download process accordingly.
   - 修改main.py中的check_ffmpeg_installed函数并设置下载步骤中的ffmpeg_location路径

6. **Run the application: / 运行应用程序：**
   - Execute the following command:
   ```bash
   python main.py
   ```

7. **Alternatively, download the precompiled package: / 也可以下载编译好的懒人一键包：**
   - The precompiled package can be found in the [releases](https://github.com/204313508/simple_video_downloader/releases) section or on Baidu Netdisk link: [www.baidu.com](www.baidu.com).

## Usage / 使用方法

- Run `main.py`, enter the video link and the save path to download the video.
- 运行 `main.py`，输入视频链接和保存路径，即可下载视频。

## Contributing / 贡献

Feel free to submit issues or pull requests if you have suggestions or improvements. / 如果您有建议或改进，欢迎提交问题或拉取请求。


