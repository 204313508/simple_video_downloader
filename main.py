import tkinter as tk
from tkinter import filedialog, messagebox
from pytube import YouTube
import subprocess
import os
import threading
import yt_dlp  # 导入yt-dlp库

# 检查本地ffmpeg是否存在
def check_ffmpeg_installed():
    """检查项目目录中的ffmpeg是否存在"""
    return os.path.exists('./ffmpeg/ffmpeg.exe')

# 主应用程序类
class VideoDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("视频下载器")

        # 代理设置
        self.proxy_var = tk.StringVar(value="none")

        # 下载链接输入
        self.url_label = tk.Label(root, text="视频链接:")
        self.url_label.grid(row=0, column=0, padx=10, pady=10)
        self.url_entry = tk.Entry(root, width=50)
        self.url_entry.grid(row=0, column=1, padx=10, pady=10)

        # 保存路径选择
        self.path_label = tk.Label(root, text="保存路径:")
        self.path_label.grid(row=1, column=0, padx=10, pady=10)
        self.path_entry = tk.Entry(root, width=50)
        self.path_entry.grid(row=1, column=1, padx=10, pady=10)
        self.path_button = tk.Button(root, text="选择", command=self.select_path)
        self.path_button.grid(row=1, column=2, padx=10, pady=10)

        # 代理选项
        self.proxy_none_radio = tk.Radiobutton(root, text="不使用代理", variable=self.proxy_var, value="none")
        self.proxy_none_radio.grid(row=2, column=0, padx=10, pady=10)
        self.proxy_manual_radio = tk.Radiobutton(root, text="手动设置代理", variable=self.proxy_var, value="manual")
        self.proxy_manual_radio.grid(row=2, column=1, padx=10, pady=10)

        # 手动输入代理地址
        self.proxy_entry = tk.Entry(root, width=50)
        self.proxy_entry.grid(row=3, column=1, padx=10, pady=10)
        self.proxy_label = tk.Label(root, text="代理地址 (如http://127.0.0.1:7890):")
        self.proxy_label.grid(row=3, column=0, padx=10, pady=10)

        # 下载按钮
        self.download_button = tk.Button(root, text="下载", command=self.download_video)
        self.download_button.grid(row=4, column=1, padx=10, pady=10)

    def select_path(self):
        """选择保存路径"""
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, folder_selected)

    def set_proxy(self):
        """手动设置代理"""
        proxy_setting = self.proxy_var.get()
        if proxy_setting == "none":
            os.environ.pop('http_proxy', None)
            os.environ.pop('https_proxy', None)
            messagebox.showinfo("代理设置", "不使用代理。")
        elif proxy_setting == "manual":
            proxy_address = self.proxy_entry.get()
            if proxy_address:
                os.environ['http_proxy'] = proxy_address
                os.environ['https_proxy'] = proxy_address
                messagebox.showinfo("代理设置", f"手动设置代理为: {proxy_address}")
            else:
                messagebox.showerror("错误", "请输入有效的代理地址！")

    def download_video(self):
        """下载视频"""
        video_url = self.url_entry.get()
        save_path = self.path_entry.get()

        if not video_url or not save_path:
            messagebox.showerror("错误", "请填写视频链接和保存路径！")
            return

        # 设置代理
        self.set_proxy()

        # 根据链接判断是YouTube、Twitch还是Bilibili
        if 'youtube.com' in video_url or 'youtu.be' in video_url:
            threading.Thread(target=self.download_youtube, args=(video_url, save_path)).start()
        elif 'twitch.tv' in video_url:
            threading.Thread(target=self.download_twitch, args=(video_url, save_path)).start()
        elif 'bilibili.com' in video_url:
            threading.Thread(target=self.download_bilibili, args=(video_url, save_path)).start()
        else:
            threading.Thread(target=self.download_other, args=(video_url, save_path)).start()

    def download_youtube(self, url, path):
        """下载YouTube视频"""
        try:
            # 在这里设置自定义的用户代理
            ydl_opts = {
                'outtmpl': os.path.join(path, '%(title)s.%(ext)s'),  # 设置输出文件路径
                'cookiefile': './cookies.txt',  # 指定cookie文件路径，确保该文件存在
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'no_check_certificate': True  # 可以尝试禁用证书检查
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                yt = ydl.extract_info(url, download=False)  # 获取视频信息
                print(f"视频标题: {yt['title']}")  # 输出视频标题用于调试
                ydl.download([url])  # 下载视频

            messagebox.showinfo("完成", "YouTube 视频下载完成！")
        except Exception as e:
            messagebox.showerror("错误", f"下载YouTube视频失败: {e}")
            print(f"详细错误信息: {e}")  # 输出详细错误信息用于调试

    def download_twitch(self, url, path):
        """下载Twitch视频"""
        try:
            command = f'streamlink --output "{os.path.join(path, "twitch_video.mp4")}" "{url}" best'
            subprocess.run(command, shell=True, check=True)
            messagebox.showinfo("完成", "Twitch 视频下载完成！")
        except Exception as e:
            messagebox.showerror("错误", f"下载Twitch视频失败: {e}")

    def download_bilibili(self, url, path):
        """使用yt-dlp下载Bilibili视频，指定本地ffmpeg路径"""
        if not check_ffmpeg_installed():
            messagebox.showerror("错误", "ffmpeg 未安装，无法合并Bilibili视频和音频！")
            return

        try:
            ydl_opts = {
                'outtmpl': os.path.join(path, '%(title)s.%(ext)s'),
                'ffmpeg_location': './ffmpeg/ffmpeg.exe',  # 指定ffmpeg的位置
                'proxy': os.environ.get('http_proxy')  # 使用设置的代理
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            messagebox.showinfo("完成", "Bilibili 视频下载完成！")
        except Exception as e:
            messagebox.showerror("错误", f"下载Bilibili视频失败: {e}")

    def download_other(self, url, path):
        """使用yt-dlp下载未知平台视频，指定本地ffmpeg路径"""
        if not check_ffmpeg_installed():
            messagebox.showerror("错误", "ffmpeg 未安装，无法合并视频和音频！")
            return

        try:
            ydl_opts = {
                'outtmpl': os.path.join(path, '%(title)s.%(ext)s'),
                'ffmpeg_location': './ffmpeg/ffmpeg.exe',  # 指定ffmpeg的位置
                'proxy': os.environ.get('http_proxy')  # 使用设置的代理
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            messagebox.showinfo("完成", "视频下载完成！")
        except yt_dlp.utils.DownloadError:
            messagebox.showerror("错误", "无法下载该平台的视频，解析失败！")
        except Exception as e:
            messagebox.showerror("错误", f"下载未知平台视频失败: {e}")

# 创建主窗口
root = tk.Tk()
app = VideoDownloaderApp(root)
root.mainloop()
