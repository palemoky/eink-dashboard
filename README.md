# eink-dashboard

一个运行在树莓派上的电子墨水屏仪表盘，显示天气、日期、时间、GitHub 提交、VPS 数据使用、比特币价格和待办事项列表。

## 功能特性

- 📅 **日期和时间显示**
- 🌤️ **实时天气信息**（支持多种天气图标）
- 💻 **GitHub 提交统计**
- 📊 **VPS 数据使用监控**
- ₿ **比特币价格追踪**
- ✅ **待办事项列表**（Goals / Must / Optional）
- 🌙 **静默时间段**（可配置不刷新的时间段，节省电量）
- 📸 **截图模式**（用于开发和调试）

## 硬件要求

- 树莓派（任意型号）
- Waveshare 7.5 inch E-Paper Display (V2)

## 安装

### 1. 克隆仓库

```bash
git clone https://github.com/yourusername/eink-dashboard.git
cd eink-dashboard
```

### 2. 安装依赖

```bash
pip3 install -r requirements.txt
```

### 3. 配置环境变量

复制 `.env.example` 文件为 `.env` 并填入你的配置：

```bash
cp .env.example .env
vim .env
```

在 `.env` 文件中配置你的 API 密钥：

```env
# 基础配置
REFRESH_INTERVAL=600
SCREENSHOT_MODE=False

# 静默时间段配置（24小时制）
QUIET_START_HOUR=1
QUIET_END_HOUR=6

# API Keys
OPENWEATHER_API_KEY=your_openweather_api_key_here
CITY_NAME=Beijing
VPS_API_KEY=your_vps_api_key_here
GITHUB_USERNAME=your_github_username
GITHUB_TOKEN=your_github_token_here
```

### 4. 配置待办事项

编辑 `src/config.py` 中的列表内容：

```python
LIST_GOALS = [
    "1. English Practice (Daily)",
    "2. Daily Gym Workout Routine",
]
LIST_MUST = ["Finish Python Code", "Email the Manager", "Buy Milk and Bread"]
LIST_OPTIONAL = ["Read 'The Great Gatsby'", "Clean the Living Room", "Sleep Early"]
```

## 使用方法

### 在树莓派上运行

```bash
python3 -m src.main
```

### 开发模式（生成截图）

在 Mac/PC 上开发时，可以使用截图模式：

```bash
SCREENSHOT_MODE=true python3 -m src.main
```

这会生成 `screenshot.bmp` 文件，你可以查看布局效果。

### 设置开机自启动

创建 systemd 服务文件：

```bash
sudo nano /etc/systemd/system/eink-dashboard.service
```

添加以下内容：

```ini
[Unit]
Description=E-Ink Dashboard
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/eink-dashboard
ExecStart=/usr/bin/python3 -m src.main
Restart=always

[Install]
WantedBy=multi-user.target
```

启用服务：

```bash
sudo systemctl enable eink-dashboard.service
sudo systemctl start eink-dashboard.service
```

## 配置说明

### 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `REFRESH_INTERVAL` | 刷新间隔（秒） | 600 |
| `SCREENSHOT_MODE` | 截图模式 | False |
| `QUIET_START_HOUR` | 静默时间段开始（小时） | 1 |
| `QUIET_END_HOUR` | 静默时间段结束（小时） | 6 |
| `OPENWEATHER_API_KEY` | OpenWeather API 密钥 | - |
| `CITY_NAME` | 城市名称 | Beijing |
| `VPS_API_KEY` | VPS API 密钥 | - |
| `GITHUB_USERNAME` | GitHub 用户名 | - |
| `GITHUB_TOKEN` | GitHub Token | - |

### 获取 API 密钥

- **OpenWeather API**: https://openweathermap.org/api
- **GitHub Token**: https://github.com/settings/tokens

## 项目结构

```
eink-dashboard/
├── src/
│   ├── main.py          # 主程序入口
│   ├── config.py        # 配置文件
│   ├── layout.py        # 布局管理
│   ├── renderer.py      # 渲染工具
│   ├── providers.py     # 数据提供者
│   └── lib/             # 硬件驱动
├── resources/
│   └── Font.ttc         # 字体文件
├── .env.example         # 环境变量模板
├── requirements.txt     # Python 依赖
└── README.md
```

## Docker 部署

### 使用 GitHub Actions 自动构建

本项目包含 GitHub Actions 配置，可以自动构建多架构镜像（支持 PC 和树莓派）。

1. Fork 本仓库。
2. 在 GitHub 仓库设置中 (Settings -> Secrets and variables -> Actions)，添加以下 Secrets：
   - `DOCKERHUB_USERNAME`: 你的 Docker Hub 用户名
   - `DOCKERHUB_TOKEN`: 你的 Docker Hub Access Token (在 Docker Hub -> Account Settings -> Security 中生成)

配置完成后，每次推送到 `main` 分支或打 tag (如 `v1.0.0`) 时，都会自动构建并推送到你的 Docker Hub。

### 使用 Docker Compose 运行

```bash
# 拉取镜像 (替换为你的用户名)
docker pull yourusername/eink-dashboard:latest

# 启动
docker-compose up -d
```

## 许可证

MIT License

## 致谢

- Waveshare 提供的 E-Paper 驱动库
- OpenWeatherMap API
- GitHub API