# txht1h

《汤逊湖北路特1号回忆录》存档，使用 MkDocs + Material 主题生成静态网站，使用 uv 管理 Python 环境和依赖。

## 本地运行

先安装 [uv](https://docs.astral.sh/uv/getting-started/installation/)；macOS 可以使用：

```sh
brew install uv
```

在项目根目录执行：

```sh
uv sync --locked
uv run --locked mkdocs serve
```

浏览器打开 <http://127.0.0.1:8000>。修改 `docs/` 中的文档或 `mkdocs.yml` 后，页面会自动刷新；按 `Ctrl+C` 停止服务。

项目默认使用 Python 3.12（见 `.python-version`）。uv 会在需要时自动下载 Python，并在 `.venv/` 创建虚拟环境，无需手动激活。首次安装需要联网；无需配置环境变量或数据库。

如果端口被占用：

```sh
uv run --locked mkdocs serve --dev-addr 127.0.0.1:8001
```

## 构建与部署

```sh
uv run --locked mkdocs build
```

生成的静态文件位于 `site/`，不提交到 Git。向 `main` 或 `master` 推送后，GitHub Actions 会按 `uv.lock` 安装依赖，并通过 `mkdocs gh-deploy` 发布到 `gh-pages` 分支。仓库的 GitHub Pages 需要配置为从该分支发布。

`mkdocs.yml` 中的 `site_url` 目前是占位地址，正式部署时应改为实际访问地址。

## 项目结构

- `docs/`：网站正文，日常内容修改在这里进行。
- `mkdocs.yml`：站点配置、主题和导航；新增页面时同步更新导航。
- `index.html`：从金山文档下载的原始 HTML 存档，不是网站首页。
- `parse.py`：历史 HTML 拆分脚本，读取根目录的 `index.html`，按标题向 `docs/` 写入 `content.html`。它不生成当前站点使用的 Markdown，普通预览和构建不需要运行。需要重新导入时，在独立副本中执行 `uv run --locked python parse.py`，检查输出后再合并，以免覆盖已有同名文件。
- `pyproject.toml` / `uv.lock`：依赖声明与锁定版本，应一起提交。

## 更新依赖

```sh
uv lock --upgrade
uv sync --locked
uv run --locked mkdocs build
```

检查构建和页面后提交更新的 `uv.lock`。添加依赖使用 `uv add 包名`。

## TODO

- [ ] Download & Branch Creation Automation
- [ ] Image Compression & Replica Detection

## History

- 2024年10月22日金山文档下载
