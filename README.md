# software-security-project

2026 软件安全课程项目：智能体安全攻防与评估。队伍 1 人，姓名与学号使用占位符。

## 下载与阅读

- [完整提交包 ZIP（约 10.8 MiB）](https://github.com/MinGioy/software-security-project/raw/refs/heads/main/backups/%E5%AD%A6%E5%8F%B7%E5%8D%A0%E4%BD%8D%E7%AC%A6%20-%20%E5%A7%93%E5%90%8D%E5%8D%A0%E4%BD%8D%E7%AC%A6%20-%20AgentAttack.zip)
- [中文报告 PDF（8 页）](%E5%AD%A6%E5%8F%B7%E5%8D%A0%E4%BD%8D%E7%AC%A6%20-%20%E5%A7%93%E5%90%8D%E5%8D%A0%E4%BD%8D%E7%AC%A6%20-%20AgentAttack/report.pdf)
- [可编辑 Word 源稿](%E5%AD%A6%E5%8F%B7%E5%8D%A0%E4%BD%8D%E7%AC%A6%20-%20%E5%A7%93%E5%90%8D%E5%8D%A0%E4%BD%8D%E7%AC%A6%20-%20AgentAttack/report.docx)
- [完整 README：环境、最小复现、本地截图与证据说明](%E5%AD%A6%E5%8F%B7%E5%8D%A0%E4%BD%8D%E7%AC%A6%20-%20%E5%A7%93%E5%90%8D%E5%8D%A0%E4%BD%8D%E7%AC%A6%20-%20AgentAttack/README.md)
- [课程要求自检清单](%E5%AD%A6%E5%8F%B7%E5%8D%A0%E4%BD%8D%E7%AC%A6%20-%20%E5%A7%93%E5%90%8D%E5%8D%A0%E4%BD%8D%E7%AC%A6%20-%20AgentAttack/SELF_CHECK.md)
- [正式成功率 CSV](%E5%AD%A6%E5%8F%B7%E5%8D%A0%E4%BD%8D%E7%AC%A6%20-%20%E5%A7%93%E5%90%8D%E5%8D%A0%E4%BD%8D%E7%AC%A6%20-%20AgentAttack/results/success_rates.csv)

交付目录包含一个攻击模式、三个实例，每例均有 attack、control、sample_info.json 与原始 evidence。实验使用 OpenClaw 2026.10.2 与 deepseek-v4-pro / deepseek-flash；所有攻击目标为 localhost，全虚构数据。

正式 60 轮：Pro 实验组 15/15 达到目标，Flash 0/15，对照 30/30 正常且无目标影响。Flash I01 已读取虚构配置但拒绝发送，不能称为完全没有任务外读取。31 条 SQLite 后台警告及全部未达目标轮次如实保留。结果解释与局限以报告和原始证据为准。

原正式与冒烟共 64 轮中 2,035 份已核验证据保持原 SHA-256。总模型费用保守估算 1.19028200 元（包含预检与冒烟，非账户现金账单）；成稿、归档与 GitHub 上传不新增模型实验。本地包装入口仅做离线验证，未新增付费端到端重跑。

## 离线验收

解压 ZIP 后，在交付目录执行（无需 key、网络或模型费用）：

```bash
python3 scripts/verify_archive.py
sha256sum -c MANIFEST.sha256
```

ZIP SHA-256：`11260e4e700a7388e11d1d290ad74beefbacf8e3665fd1bfcbdc83b9d47b76c7`。

云端源交付快照：`aa293646f4f79909f5b5fda8861f5690b2bdc81a`。此仓库的交付提交接续原 main 分支，不改写已有历史；原实验完整工作区仍在云端保存。
