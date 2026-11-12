# taskboard_44
> Python 命令行任务看板

## 项目简介
本项目是一个基于 Python 的命令行任务看板，数据持久化保存在本地 tasks.json。
支持新增任务、标记完成、按优先级与截止日期自动排序，一键导出 Markdown 格式日报。

## 功能清单
- 添加任务：任务名称、优先级（高 / 中 / 低）、截止日期
- 查看任务：自动按优先级、截止日期排序展示
- 将指定任务标记为已完成
- 导出 Markdown 日报，区分待办 / 已完成
- JSON 文件本地持久化

## 运行方式
```bash
git clone https://github.com/你的github用户名/taskboard_44.git
cd taskboard_44
python taskboard.py

