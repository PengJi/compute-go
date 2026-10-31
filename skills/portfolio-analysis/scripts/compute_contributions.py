#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""持仓主题贡献计算器（portfolio-analysis 技能配套脚本）。

用途：持仓标的较多（超过 5 个）时，把持仓表写入 CSV，用本脚本计算
各主题的权重占比、主题加权收益率与绝对贡献（权重 × 收益率），并做
加总校验，避免手工逐项计算出错或凑数。

CSV 格式（UTF-8，首行表头可写可不写）：
    名称,主题,数值,区间收益率
    沪深300ETF,宽基与底仓,20,8.5
    半导体ETF,科技与半导体,15,22.3
    某某纯债,现金与固收,25,2.1
    某主动基金,均衡配置,10,          <- 收益率留空视为"待估算"，单独列出

"数值"列填权重百分比（20 表示 20%）或金额（20000）均可，脚本按
数值量级自动识别；识别不可靠时用 --weight / --amount 显式指定。

用法示例：
    python3 scripts/compute_contributions.py /tmp/portfolio.csv
    python3 scripts/compute_contributions.py /tmp/portfolio.csv --amount
    python3 scripts/compute_contributions.py /tmp/portfolio.csv --portfolio-return 5.2

仅依赖 Python 标准库。
"""

import argparse
import csv
import sys


def parse_number(text):
    """解析数值字段，容忍 % 后缀与全角逗号；空值返回 None。"""
    s = (text or "").strip().replace("%", "").replace(",", "").replace("，", "")
    if not s:
        return None
    try:
        return float(s)
    except ValueError:
        return None


def load_items(csv_path):
    """读取 CSV，返回 [(名称, 主题, 数值, 收益率或None), ...]。"""
    rows = []
    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        for row in csv.reader(f):
            if row and any(cell.strip() for cell in row):
                rows.append(row)
    if not rows:
        sys.exit("错误：CSV 为空。")

    # 首行第三列不是数值则视为表头，跳过。但真正的表头行，第三/四列都不会是
    # 数值；若第四列（收益率）能解析出数字，更像是数值列残缺的数据行——静默
    # 丢弃等于丢数据，宁可报错让用户补表头或补全数值列。
    if len(rows[0]) >= 3 and parse_number(rows[0][2]) is None:
        if len(rows[0]) >= 4 and parse_number(rows[0][3]) is not None:
            sys.exit(
                "错误：无法确定首行是表头还是数据行（数值列为空或非数值，但收益率列是"
                f"数字 '{rows[0][3].strip()}'）。请为 CSV 补一行表头，或填全首行的数值列，"
                f"避免数据被静默丢弃。\n首行内容：{','.join(rows[0])}"
            )
        rows = rows[1:]
    if not rows:
        sys.exit("错误：CSV 除表头外没有数据行。")

    items = []
    for i, row in enumerate(rows, start=1):
        if len(row) < 3:
            sys.exit(f"错误：第 {i} 行列数不足，至少需要 名称,主题,数值 三列。")
        name, theme, value = row[0].strip(), row[1].strip(), parse_number(row[2])
        raw_ret = parse_number(row[3]) if len(row) >= 4 else None
        # CSV 中收益率按百分点填写（8.5 表示 8.5%），统一转为小数参与计算。
        ret = raw_ret / 100 if raw_ret is not None else None
        if not name or not theme:
            sys.exit(f"错误：第 {i} 行名称或主题为空。")
        if value is None or value < 0:
            sys.exit(f"错误：第 {i} 行数值列无法解析（'{row[2].strip()}'）。")
        items.append((name, theme, value, ret))
    return items


def main():
    parser = argparse.ArgumentParser(
        description="计算各持仓主题的权重占比、加权收益率与绝对贡献（权重×收益率），"
                    "并校验各主题贡献加总；收益率留空的标的视为待估算，单独列出。",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="示例：python3 compute_contributions.py /tmp/portfolio.csv --portfolio-return 5.2",
    )
    parser.add_argument("csv_path", help="持仓 CSV 文件路径（列：名称,主题,数值,区间收益率）")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--weight", action="store_true",
                       help="强制把数值列解释为权重百分比（默认自动识别）")
    group.add_argument("--amount", action="store_true",
                       help="强制把数值列解释为金额（默认自动识别）")
    parser.add_argument("--portfolio-return", type=float, default=None, metavar="X",
                        help="用户已知的组合真实总收益（单位 %%），用于交叉校验；"
                             "偏差超过 0.5 个百分点时打印口径警告")
    args = parser.parse_args()

    items = load_items(args.csv_path)

    total_value = sum(v for _, _, v, _ in items)
    if total_value <= 0:
        sys.exit("错误：数值列合计为 0，无法计算占比。")

    # 自动识别数值列含义：权重百分比通常 <=100，金额常见远大于 100。
    if args.weight:
        mode = "weight"
    elif args.amount:
        mode = "amount"
    elif max(v for _, _, v, _ in items) <= 100:
        mode = "weight"
    else:
        mode = "amount"
    mode_label = "权重百分比" if mode == "weight" else "金额"
    print(f"[识别] 数值列按{mode_label}处理（如不符请用 --weight / --amount 重跑）")

    # 权重口径下合计应约等于 100：偏离过多往往意味着漏了持仓或录错了权重，此时
    # 归一化会把各主题贡献按 100/合计 倍系统性放大，必须显式提醒而非静默处理。
    if mode == "weight" and abs(total_value - 100) > 0.5:
        print(f"[警告] 输入权重合计 {total_value:.2f}%，偏离 100% 超过 0.5 个百分点。"
              "本表按该合计归一化计算，贡献可能与全组合口径不符，"
              "请检查是否有持仓遗漏或权重录入错误。")
    print()

    # 逐主题聚合：贡献只累加有收益率数据的标的。
    themes = {}
    pending = []
    for name, theme, value, ret in items:
        w = value / total_value  # 归一化权重，用户权重不必恰好加总 100
        agg = themes.setdefault(theme, {"weight": 0.0, "known_weight": 0.0,
                                        "contribution": 0.0, "names": []})
        agg["weight"] += w
        agg["names"].append(name)
        if ret is None:
            pending.append((name, theme, w))
        else:
            agg["known_weight"] += w
            agg["contribution"] += w * ret  # 单位：小数（如 0.06 = +6%）

    print(f"{'主题':<12}{'权重占比':>10}{'主题收益率':>12}{'绝对贡献':>10}  覆盖")
    print("-" * 62)
    total_contrib = 0.0
    for theme, agg in sorted(themes.items(), key=lambda kv: -kv[1]["contribution"]):
        if agg["known_weight"] > 0:
            theme_ret = agg["contribution"] / agg["known_weight"]
            ret_str = f"{theme_ret * 100:+.2f}%"
        else:
            ret_str = "待估算"
        coverage = agg["known_weight"] / agg["weight"] if agg["weight"] > 0 else 0
        print(f"{theme:<12}{agg['weight'] * 100:>9.2f}%{ret_str:>12}"
              f"{agg['contribution'] * 100:>+9.2f}%  {coverage * 100:.0f}%")
        total_contrib += agg["contribution"]
    print("-" * 62)
    known_weight = sum(a["known_weight"] for a in themes.values())
    if known_weight == 0:
        # 一个收益率都没有时，+0.00% 仍会被误读成"组合收益为 0"，直接说没有数据。
        print("[校验] 无有效收益数据，无法估算组合收益，请先补充收益率或按 "
              "references/per-theme-analysis.md 的指引用跟踪指数/同类均值近似（并标注估算）。")
    else:
        print(f"[校验] 各主题绝对贡献加总 = {total_contrib * 100:+.2f}%（即组合估算收益，"
              f"基于已覆盖 {known_weight * 100:.1f}% 权重的数据）")

    if pending:
        print("\n[待估算] 以下标的收益率缺失，未纳入收益计算（禁止编造）：")
        for name, theme, w in pending:
            print(f"  - {name}（{theme}，权重 {w * 100:.2f}%）")

    if args.portfolio_return is not None:
        actual = args.portfolio_return
        if known_weight == 0:
            print(f"\n[交叉校验] 无有效收益数据，无法与已知组合总收益（{actual:+.2f}%）核对。")
            return
        deviation = abs(total_contrib * 100 - actual)
        print(f"\n[交叉校验] 组合已知总收益 {actual:+.2f}%，估算 {total_contrib * 100:+.2f}%，"
              f"偏差 {deviation:.2f} 个百分点。")
        if deviation > 0.5:
            print("[警告] 偏差超过 0.5 个百分点：可能存在区间内大额申赎、以当前权重近似"
                  "平均权重的误差、或个别标的收益为估算值。不要为凑数修改数据，"
                  "应在报告中注明口径局限并说明可能原因。")
        else:
            print("[通过] 偏差在 0.5 个百分点以内，口径一致。")


if __name__ == "__main__":
    main()
