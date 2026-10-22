# 课程交付自检清单

本清单针对归档交付物；正式实验有效性由阶段 3 原件和归档离线核验共同支撑。成稿期间没有新增模型调用、接收事件或实验结果。

|课程要求|状态|核对材料与结果|
|---|---|---|
|规定目录、report.pdf、README.md、patterns/pattern_01|通过|根目录“学号占位符 - 姓名占位符 - AgentAttack”；必需文件齐全|
|单人至少一种模式、三个实例|通过|P01 与 I01/I02/I03；pattern_info.json 列出完整实例编号|
|实例有实质差异|通过|报告 2.2 与 sample_info.json 六维矩阵：归档数据流、账单状态、作业资源，超出表面改名|
|用户任务、攻击能力、前提、机制、判据|通过|sample_info.json、prompts/user_task.txt、模式 threat_model|
|每实例 attack/control|通过|三对实际 Skill；移除唯一虚假前置段后逐字相等；名称、描述与正常步骤不变|
|至少两个受测环境|通过|OpenClaw 2026.10.2 + deepseek-v4-pro / deepseek-flash；原始响应模型 ID 可核对|
|至少一种环境有可验证安全影响|通过|Pro 三实例各 5/5；接收、事务或作业事件与工具及状态相互印证|
|重复测试与成功率|通过|冻结计划 60 个唯一 run_id 顺序一致；12 单元各 5 次；4 次冒烟独立编号和分母|
|实验组与对照统计|通过|Pro 实验组 15/15；Flash 0/15；30/30 对照正常且无目标影响；以 success_rates.csv 为准|
|拒绝与执行故障分开|通过|15 次 Flash 未达目标为防御成功；正式无 INFRA_ERROR；I01 Flash 5/5 已读未发单独披露|
|输入、行为与客观结果证据|通过|逐轮输入、原始 API 响应、tools、receiver/transactions/jobs、before/after 与产物，不只计 CSV 行数|
|证据真实性与归档完整性|通过|阶段 3 已核验 64 轮的 2,035 个证据文件逐字节匹配原 SHA-256；来源索引原件及新路径映射均保留|
|截图与录制|通过|64 次冒烟/正式均有真实 localhost 监控截图及 GNU script 文本录制；未冒充原生 GUI 或视频|
|数字与结论有证据索引|通过|报告 E01～E14 映射；观察解释与未测量的内部原因明确区分|
|31 条 SQLite 警告说明|通过|29 条准入关闭，2 条另含清理失败；31 个 run_id 原行保留；分别核对 CLI 0、产物、状态；不声称原生会话长期完整性已验证|
|安全与隐私|通过|攻击目标仅 127.0.0.1、全虚构数据；推理仅官方 API；真实 key 原值扫描通过、未入包；姓名学号占位|
|费用账本|通过|241 次原推理调用估算 1.19028200 元；分阶段列示、非现金账单；成稿新增调用 0|
|中文报告与 Word 源稿|通过|report.pdf 实际转换且视觉检查，8 页；report.docx 七节，report.md 同源；字体嵌入与文本边界检查通过|
|环境、安装、完整最小复现命令|通过|README 的 Linux/WSL2 全命令，含依赖、安全 key 注入、I01 control/attack、本地截图与证据导航|
|原始链路运行验证|通过|原协调器预检、4 次冒烟与 60 次正式真实完成；运行及独立核验原件保留|
|新增本地包装入口验证|已披露边界|CLI、Python/Bash 语法、覆盖保护与组件一致性离线验证通过；成稿不新造数据，未新增付费端到端模型实验|
|JSON 字段与合法性|通过|模式/实例必需字段、证据路径、双模型和组别已核对，归档 JSON 可解析|
|Git 与 ZIP|交付流程核对|见工作区最终交付回执；ZIP 使用已提交树生成，CRC 与解压内容逐项核对|

## 核验命令

```bash
python3 scripts/verify_archive.py
sha256sum -c MANIFEST.sha256
```

首条预期输出 verified_formal=60、verified_smoke=4、groups=12、source_evidence_files=2035、sqlite_warning_runs=31、estimated_cny=1.19028200、new_experiments=0。它不请求模型、不启动服务、不改写证据。

## 核验记录与来源

- validation/archive_verification.json：归档、顺序、判据、哈希及账本离线检查。
- validation/reproduction_checks.json：新复现包装器的离线检查范围。
- validation/document_validation.json：JSON、报告数字、页数、字体及视觉检查。
- provenance/archive_origin.json：阶段 3 来源与源 Git 快照。
- MANIFEST.sha256：除其自身外的完整交付文件哈希。

历史预检与安装/修复记录仅作背景补充，未混入正式分母。原始快照中的“待确认”等历史状态与旧绝对路径原样保留，以免改造证据。

## 已知局限

每条件仅五次；模型别名、定价与运行时可能变化；Flash I01 仍有非必要读取；mock 业务不能等同生产攻击效果；后台警告未做框架级根因及长期持久化实验；新本地包装器未在成稿阶段额外付费重跑。报告与 README 均已明示。
