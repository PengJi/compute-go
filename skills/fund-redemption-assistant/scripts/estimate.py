#!/usr/bin/env python3
"""基金赎回助手：确认日/到账日推算与赎回费用估算。

用法示例：

    # 推算 T 日与 T+N 日期：15:00 前提交当日为 T 日，之后顺延到下一工作日
    python3 scripts/estimate.py settlement --date 2026-11-13 --time 14:30 --t-plus 1

    # 估算赎回金额、赎回费与到账金额；--rate 为小数（0.005 即 0.5%），多批次成对重复传参
    python3 scripts/estimate.py fee --nav 1.234 --shares 10000 --rate 0.005 --shares 5000 --rate 0

限制（重要）：
    - 仅用 Python 标准库，无需安装第三方包。
    - 工作日推算只跳过周六、周日。法定节假日未内置（每年发布且调休安排会变），
      节假日期间的结果会把休息日当作工作日，输出给用户前必须人工核对节假日。
"""

import argparse
import json
import sys
from datetime import datetime, timedelta

CUTOFF_HOUR = 15  # 交易日 15:00 截止，之后算下一交易日

WEEKDAY_NAMES = ("周一", "周二", "周三", "周四", "周五", "周六", "周日")

HOLIDAY_WARNING = (
    "法定节假日未内置（每年不同，调休可能改变工作日），本结果仅跳过周六日，"
    "输出给用户前需人工核对节假日。"
)


def fail(message):
    print(f"错误：{message}", file=sys.stderr)
    sys.exit(2)


def is_weekend(d):
    return d.weekday() >= 5  # 周六=5，周日=6


def roll_to_business_day(d):
    """d 若为周末，顺延到下一个工作日；工作日原样返回。"""
    while is_weekend(d):
        d = d + timedelta(days=1)
    return d


def next_business_day(d):
    """d 之后（不含 d）的下一个工作日，跳过周六日。"""
    return roll_to_business_day(d + timedelta(days=1))


def add_business_days(d, n):
    """从 d 起加 n 个工作日（跳过周六日）。"""
    for _ in range(n):
        d = next_business_day(d)
    return d


def weekday_cn(d):
    return WEEKDAY_NAMES[d.weekday()]


def parse_time(value):
    """接受 HH:MM 或 HH:MM:SS，返回当日分钟数。"""
    for fmt in ("%H:%M", "%H:%M:%S"):
        try:
            t = datetime.strptime(value, fmt)
            return t.hour * 60 + t.minute
        except ValueError:
            continue
    return None


def cmd_settlement(args):
    try:
        submitted = datetime.strptime(args.date, "%Y-%m-%d").date()
    except ValueError:
        fail("--date 格式应为 YYYY-MM-DD，如 2026-11-13")
    if args.t_plus < 0:
        fail("--t-plus 不能为负数")

    submit_minutes = None
    if args.time is not None:
        submit_minutes = parse_time(args.time)
        if submit_minutes is None:
            fail("--time 格式应为 HH:MM，如 14:30")

    cutoff = CUTOFF_HOUR * 60
    if is_weekend(submitted):
        # 周末不是交易日，无论几点提交，T 日都是下一工作日
        date_t = roll_to_business_day(submitted)
        note = "提交日为周末（非交易日），T 日为下一工作日。"
    elif submit_minutes is not None and submit_minutes >= cutoff:
        date_t = next_business_day(submitted)
        note = "交易日 15:00 及以后提交，T 日为下一工作日。"
    elif submit_minutes is not None:
        date_t = submitted
        note = "交易日 15:00 前提交，当日为 T 日。"
    else:
        date_t = submitted
        note = "未提供 --time，按 15:00 前提交处理，当日为 T 日；若实际在 15:00 后提交，T 日顺延一个工作日。"

    result = add_business_days(date_t, args.t_plus)
    return {
        "submitted_date": submitted.isoformat(),
        "t_plus": args.t_plus,
        "date_t": date_t.isoformat(),
        "date_t_weekday": weekday_cn(date_t),
        "result_date": result.isoformat(),
        "result_weekday": weekday_cn(result),
        "result_note": f"自 T 日起加 {args.t_plus} 个工作日（仅跳过周六日）。",
        "deadline_note": note,
        "warnings": [HOLIDAY_WARNING],
    }


def cmd_fee(args):
    if args.nav <= 0:
        fail("--nav 必须大于 0")
    if len(args.shares) != len(args.rate):
        fail(f"--shares 与 --rate 必须成对出现（当前 {len(args.shares)} 个份额 vs {len(args.rate)} 个费率）")

    batches = []
    for i, (shares, rate) in enumerate(zip(args.shares, args.rate), start=1):
        if shares <= 0:
            fail(f"第 {i} 批 --shares 必须大于 0")
        if rate < 0 or rate > 1:
            fail(f"第 {i} 批 --rate 应为 0~1 的小数（0.005 即 0.5%）")
        amount = round(args.nav * shares, 2)
        fee = round(amount * rate, 2)
        batches.append({
            "batch": i,
            "shares": shares,
            "rate": rate,
            "redemption_amount": amount,
            "redemption_fee": fee,
            "net_amount": round(amount - fee, 2),
        })

    total_amount = round(sum(b["redemption_amount"] for b in batches), 2)
    total_fee = round(sum(b["redemption_fee"] for b in batches), 2)
    return {
        "nav": args.nav,
        "batch_count": len(batches),
        "batches": batches,
        "totals": {
            "shares": round(sum(b["shares"] for b in batches), 2),
            "redemption_amount": total_amount,
            "redemption_fee": total_fee,
            "net_amount": round(total_amount - total_fee, 2),
        },
        "warnings": [
            "赎回适用未知价法，实际金额按 T 日确认净值计算；本估算使用的净值为传入的假设值。",
            "赎回费率与持有期分档以基金合同和销售平台显示为准。",
        ],
    }


def build_parser():
    parser = argparse.ArgumentParser(
        prog="estimate.py",
        description="基金赎回确认日/到账日推算与费用估算（仅标准库；法定节假日未内置）",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_settle = sub.add_parser("settlement", help="推算 T 日与 T+N 日期（跳过周六日，不含节假日）")
    p_settle.add_argument("--date", required=True, help="提交日期，格式 YYYY-MM-DD")
    p_settle.add_argument("--time", help="提交时间，格式 HH:MM；缺省按 15:00 前提交处理")
    p_settle.add_argument("--t-plus", type=int, default=1, help="T+N 的 N，按工作日计（默认 1）")
    p_settle.set_defaults(func=cmd_settlement)

    p_fee = sub.add_parser("fee", help="估算赎回金额、赎回费与到账金额（支持多批次）")
    p_fee.add_argument("--nav", type=float, required=True, help="单位净值，如 1.234")
    p_fee.add_argument("--shares", type=float, required=True, action="append",
                       help="赎回份额；多批次时重复传入，如 --shares 10000 --shares 5000")
    p_fee.add_argument("--rate", type=float, required=True, action="append",
                       help="该批次赎回费率（小数，0.005 即 0.5%）；与 --shares 成对出现")
    p_fee.set_defaults(func=cmd_fee)
    return parser


def main():
    args = build_parser().parse_args()
    result = args.func(args)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
