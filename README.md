# CI/CD 工作流（可复用）

本仓库提供一个**集中式可复用的 GitHub Actions 工作流**，
通过自托管 Runner 将项目部署到 Raspberry Pi。

所有部署逻辑都在这里维护。
各应用仓库只需引用此工作流即可。

---

## 组织项目目录

组织内项目的“文件夹式”分类索引维护在：[`PROJECTS.md`](./PROJECTS.md)。

目前建议将 `zyxx-organization` 定位为：

```text
Home Lab / Raspberry Pi / 自部署生活服务 / 自动化基础设施
```

---

## 仓库职责

- 本仓库维护通用发布、健康检查及可选回滚；应用仓库维护自己的安装和验证命令。
- 支持 `revision` 传入已通过 CI 的完整 SHA；未传入的旧调用保留分支发布兼容。
- 发布中的任务不会被新推送中断。部署目录存在已跟踪文件改动时拒绝覆盖。
- `rollback_command` 启用失败恢复旧代码；不会回滚业务数据库。`smoke_command` 用于健康检查后的只读行为验证。
- `runner_label` 默认 `raspi`；独立仓库的现有 runner 没有该自定义标签时，可传已有的明确平台标签（例如 `ARM64`），不需要重新注册 runner。

该方案适合**个人或小团队**使用。

---

## 工作原理

每个应用仓库只需包含一个最小化的工作流，例如：

```yaml
name: Deploy

on:
  push:
    branches:
      - master   # or main

permissions:
  contents: read

jobs:
  deploy:
    uses: zyxx-organization/cicd-workflow/.github/workflows/deploy.yml@main
    with:
      project_name: my_project_name
      service_name: my_project_name
```

---

## 输入参数

| 参数名        | 必填 | 说明 |
|-------------|------|------|
| project_name | 是   | `/home/zyxx/projects/` 下的目录名 |
| service_name | 是   | systemd 服务名称 |
| project_path | 否   | 绝对路径（可选覆盖） |

---

## Runner

- 使用**自托管 Runner**（Raspberry Pi）
- Runner 标签：`self-hosted`、`raspi`

---

## 默认项目结构

```text
/home/zyxx/projects/
  my_project_name/
    .git/
    app/
    ...
```

---

## 重要说明

- 该工作流始终通过 `@main` 引用
- **没有** tags 或版本
- 这里的改动会立即生效
- 适用于可信环境

---

## 维护规则

- 修改 `.github/workflows/deploy.yml` 以调整部署行为
- 应用工作流应在 CI 成功后触发，并把同一次 CI 的 SHA 作为 `revision`。
- 回滚命令只恢复兼容运行环境、服务配置和服务，不把旧数据库覆盖新写入。
- 测试直接执行本工作流的 shell，在隔离 Git 仓库中验证分支前移、失败回滚与数据保留。
