import json
import os
from datetime import datetime

DATA_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_tasks(tasks):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

def add_task():
    name = input("请输入任务名称：").strip()
    if not name:
        print("任务名不能为空！")
        return
    priority = input("优先级（高/中/低，默认：中）：").strip() or "中"
    due_str = input("截止日期（格式 YYYY-MM-DD，留空不填）：").strip()
    due_date = None
    if due_str:
        try:
            due_str = due_str.strip()
            datetime.strptime(due_str, "%Y-%m-%d")
            due_date = due_str
        except ValueError:
            print("⚠️ 日期格式错误，忽略该截止日期")
    task = {
        "id": len(load_tasks()) + 1,
        "name": name,
        "priority": priority,
        "due_date": due_date,
        "finished": False,
        "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    tasks = load_tasks()
    tasks.append(task)
    save_tasks(tasks)
    print("✅ 任务添加成功！")

def mark_finished():
    tasks = load_tasks()
    if not tasks:
        print("暂无任务")
        return
    show_tasks()
    try:
        tid = int(input("输入要标记完成的任务 ID："))
    except ValueError:
        print("ID 必须是数字")
        return
    found = False
    for t in tasks:
        if t["id"] == tid:
            t["finished"] = True
            found = True
            break
    if found:
        save_tasks(tasks)
        print("✅ 已标记为完成")
    else:
        print("未找到该任务")

def show_tasks():
    tasks = load_tasks()
    if not tasks:
        print("暂无任务")
        return
    weight = {"高": 0, "中": 1, "低": 2}
    # bugfix 分支：这里写一套和 feature 不一样的排序注释 + key
    tasks_sorted = sorted(
        tasks,
        key=lambda x: (
            weight.get(x["priority"], 99),
            x["due_date"] if x["due_date"] else "9999-12-31"
        )
    )
    print("\n" + "=" * 70)
    print(f"{'ID':<4}{'状态':<6}{'任务名称':<22}{'优先级':<6}{'截止日期':<12}{'创建时间'}")
    print("-" * 70)
    for t in tasks_sorted:
        status = "✓完成" if t["finished"] else "○待办"
        due = t["due_date"] if t["due_date"] else "无"
        print(f"{t['id']:<4}{status:<6}{t['name']:<22}{t['priority']:<6}{due:<12}{t['create_time']}")
    print("=" * 70 + "\n")

def export_markdown():
    tasks = load_tasks()
    if not tasks:
        print("没有任务可以导出")
        return
    today = datetime.now().strftime("%Y-%m-%d")
    md_lines = [f"# 任务日报 {today}\n"]
    md_lines.append("## ✅ 已完成任务\n")
    for t in tasks:
        if t["finished"]:
            md_lines.append(f"- [x] {t['name']}（优先级：{t['priority']}，截止：{t['due_date'] or '无'}）")
    md_lines.append("\n## ○ 待办任务\n")
    for t in tasks:
        if not t["finished"]:
            md_lines.append(f"- [ ] {t['name']}（优先级：{t['priority']}，截止：{t['due_date'] or '无'}）")
    filename = f"daily_report_{today}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
    print(f"✅ Markdown 日报已导出至：{filename}")

def menu():
    while True:
        print("===== taskboard_44 命令行任务看板 =====")
        print("1. 添加任务")
        print("2. 查看任务（按优先级、截止日期排序）")
        print("3. 标记任务完成")
        print("4. 导出 Markdown 日报")
        print("0. 退出")
        choice = input("\n请输入选项：").strip()
        if choice == "1":
            add_task()
        elif choice == "2":
            show_tasks()
        elif choice == "3":
            mark_finished()
        elif choice == "4":
            export_markdown()
        elif choice == "0":
            print("程序退出。")
            break
        else:
            print("输入无效，请重新选择！")

if __name__ == "__main__":
    menu()
