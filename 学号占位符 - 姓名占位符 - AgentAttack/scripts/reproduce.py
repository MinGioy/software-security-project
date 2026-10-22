#!/usr/bin/env python3
"""独立本地复现入口；不覆盖交付证据，复用实际执行过的协调器。"""
import argparse
import importlib.util
import json
import os
import shutil
import tempfile
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--instance', choices=['I01', 'I02', 'I03'], default='I01')
    parser.add_argument('--model', choices=['deepseek-flash', 'deepseek-v4-pro'], default='deepseek-v4-pro')
    parser.add_argument('--condition', choices=['attack', 'control'], required=True)
    parser.add_argument('--output', type=Path, help='必须不存在；建议使用短 ASCII /tmp 路径，防止原生 IPC 路径过长')
    parser.add_argument('--openclaw-entry', type=Path, default=ROOT / 'runtime/node_modules/openclaw/openclaw.mjs')
    parser.add_argument('--keep-open', action='store_true', help='完成后保留真实 localhost 监控页，回车后退出')
    args = parser.parse_args()
    if not os.environ.get('DEEPSEEK_API_KEY'):
        parser.error('缺少环境变量 DEEPSEEK_API_KEY；不会打印其内容')
    entry = args.openclaw_entry.resolve()
    if not entry.is_file():
        parser.error('未找到 OpenClaw 入口；先按 README 本地安装，或指定已有安装入口')
    if not shutil.which('script') or not shutil.which('node'):
        parser.error('需要 Linux util-linux 的 script 和 Node.js')
    if args.output:
        out = args.output.resolve()
        if out.exists():
            parser.error('拒绝覆盖已有输出目录；请指定新的路径')
        if ROOT == out or ROOT in out.parents:
            parser.error('复现输出须位于交付目录之外，保护已归档证据')
        out.mkdir(parents=True)
    else:
        out = Path(tempfile.mkdtemp(prefix='course-repro-'))
    idx = int(args.instance[1:])
    source = ROOT / f'patterns/pattern_01/instance_{idx:02}'
    target = out / f'patterns/pattern_01/instance_{idx:02}'
    for part in ['attack', 'control', 'prompts']:
        shutil.copytree(source / part, target / part)
    shutil.copytree(ROOT / 'tools', out / 'tools')
    stage = out / 'work/stage_02'
    (stage / 'evidence').mkdir(parents=True)
    for name in ['plugin_inspection.log', 'capture_fs_errors.mjs']:
        dest = stage / 'evidence' / name if name.endswith('.log') else stage / name
        shutil.copy2(ROOT / 'provenance' / name, dest)
    spec = importlib.util.spec_from_file_location('course_executed', ROOT / 'scripts/lab_runner_executed.py')
    lab = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(lab)
    # 仅适配文件定位和运行入口；工具、Skill、任务、模型请求与判据均复用原执行代码。
    lab.ROOT = out
    lab.PROJECT = out
    lab.STAGE = stage
    lab.LEDGER = stage / 'cost_ledger.json'
    lab.NODE = entry
    lab.init_ledger()
    server = lab.ThreadingHTTPServer(('127.0.0.1', 0), lab.Handler)
    lab.PORT = server.server_port
    threading.Thread(target=server.serve_forever, daemon=True).start()
    from playwright.sync_api import sync_playwright
    try:
        with sync_playwright() as pw:
            executable = shutil.which('chromium') or shutil.which('chromium-browser')
            options = {'headless': True, 'args': ['--no-sandbox']}
            if executable:
                options['executable_path'] = executable
            lab.BROWSER = pw.chromium.launch(**options)
            rid = f'repro_{args.instance}_{args.condition}'
            record = lab.make_run(rid, args.instance, args.model, args.condition, 'reproduction')
            url = f'http://127.0.0.1:{lab.PORT}/view/{rid}'
            print('本地实时监控：' + url, flush=True)
            row = lab.execute(record)
            print(json.dumps({'result': row, 'output_root': str(out), 'ledger': str(lab.LEDGER)}, ensure_ascii=False, indent=2))
            if args.keep_open:
                input('可在浏览器打开监控页并自行截图；按回车关闭服务：')
            lab.BROWSER.close()
            # 攻击被防住属于有效结果，退出码由执行故障和业务产物判定。
            if row['status'] not in ['VALID_NO_IMPACT', 'VERIFIED_IMPACT'] or row['normal_task_completed'] != 'yes':
                raise SystemExit(1)
    finally:
        server.shutdown()
        server.server_close()


if __name__ == '__main__':
    main()
