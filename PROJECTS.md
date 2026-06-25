# zyxx-organization 项目目录

这个文件把组织内仓库按用途分组，作为“文件夹式”索引使用。GitHub organization 本身没有真正的仓库文件夹，所以这里用目录 + 命名规则 + 后续 custom properties 来管理。

## 01 · 基础设施 / Infra

| 仓库 | 状态 | 说明 |
|---|---|---|
| `cicd-workflow` | active | 集中式 GitHub Actions / Raspberry Pi self-hosted runner 部署工作流 |

## 02 · 健身与生活服务 / Life Apps

| 仓库 | 状态 | 说明 |
|---|---|---|
| `fitness_web` | active | 六周训练法、生活/训练记录相关 Web 服务 |
| `workout_nova` | active | 训练打卡、训练周期、1RM 设置与自部署 check-in 页面 |

## 03 · 待迁移：树莓派 / Home Lab

这些仓库建议之后从个人账号迁移到组织中，迁移后再归档到上面的分组。

| 当前仓库 | 建议分组 | 说明 |
|---|---|---|
| `zyxx66/raspi_server_ops` | Infra | 服务器运维、systemd、Cloudflare Tunnel、部署脚本等 |
| `zyxx66/raspi_software` | Infra | 树莓派通用软件/服务配置 |
| `zyxx66/raspberry_controller` | Automation | 树莓派控制器/API/设备控制相关 |
| `zyxx66/raspi_home_nav` | Automation | 家庭导航/入口页相关 |
| `zyxx66/raspberry_smart_home` | Automation | Home Assistant / AppDaemon / 智能家居自动化 |
| `zyxx66/journal_web` | Life Apps | 日记/习惯/个人记录 Web 服务 |
| `zyxx66/diet_web` | Life Apps | 体重、饮食、热量缺口相关 Web 服务 |
| `zyxx66/rsp_torrent_downloader` | Service | 树莓派下载服务，视使用情况 active 或 paused |

## 04 · 暂不迁移：实验 / 游戏 / 模板

这些项目更像个人实验、模板、游戏 demo 或 fork，建议继续留在个人账号，避免组织变成杂物堆。

- `zyxx66/henko`
- `zyxx66/standard-readme`
- `zyxx66/swatches`
- `zyxx66/MaaFramework`
- `zyxx66/dota2_auto`
- `zyxx66/auto_game_engine`
- `zyxx66/VR-wallpaper-keeper`
- `zyxx66/my_first_game`

## 推荐 custom properties

后续可以在 organization settings 里建立这些属性，用于 GitHub 仓库列表筛选：

| property | values |
|---|---|
| `area` | `infra`, `life-app`, `automation`, `service`, `archive` |
| `runtime` | `raspberry-pi`, `cloudflare-tunnel`, `github-actions`, `local-only`, `none` |
| `status` | `active`, `paused`, `legacy`, `archived` |

建议先给已有三个组织仓库设置：

| 仓库 | area | runtime | status |
|---|---|---|---|
| `cicd-workflow` | `infra` | `github-actions` | `active` |
| `fitness_web` | `life-app` | `raspberry-pi` | `active` |
| `workout_nova` | `life-app` | `raspberry-pi` | `active` |

## 命名建议

新仓库优先使用统一前缀：

```text
raspi-*       # 自己用，直观
homelab-*     # 对外展示更像作品集
```

短期不强制重命名现有仓库。先用 PROJECTS.md 和 custom properties 管理，等迁移稳定后再考虑统一命名。
