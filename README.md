# CI/CD 工作流（可复用）

本仓库提供一个**集中式可复用的 GitHub Actions 工作流**，
通过自托管 Runner 将项目部署到 Raspberry Pi。

所有部署逻辑都在这里维护。
各应用仓库只需引用此工作流即可。

---

## 仓库职责

- 本仓库**拥有全部部署逻辑**
- 应用仓库**不得包含部署脚本**
- 此处的任何改动会**立即影响所有项目**

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
- 除 `with:` 参数外，不要编辑应用仓库的工作流
- 不要在应用仓库中加入部署逻辑
