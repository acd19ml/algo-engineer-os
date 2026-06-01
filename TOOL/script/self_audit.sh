#!/usr/bin/env bash
# self_audit.sh — algo-engineer-os 仓库一致性自审
#
# WHAT  把"规则层一致性"做成可复跑检查：单一真值源、节点自含、
#       meta.yaml 卫生、WORK↔PROJECT 边界、ownership 单源、README 无硬编计数。
# WHEN  任何"建/改了文件"的 session 收尾前必跑（INBOX triage 与
#       直接设计 / 项目 session 都算）；平时想确认仓库一致也可跑。
#       有 FAIL 必须修掉再收尾。可入 CI（出现 FAIL 时 exit 1）。
# HOW   bash TOOL/script/self_audit.sh        # 从任意目录，脚本自己定位仓库根
# OWN   本脚本在 TOOL/（LLM 可写）。"何时跑"的规则在 META/llm/triage.md
#       （用户拥有）的「两条入口，都受同一套纪律」段。
#
# 退出码：0 = 无 FAIL（可有 WARN）；1 = 有 FAIL；2 = 找不到仓库根。

set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." 2>/dev/null && pwd)"
[ -f "$ROOT/META/REGISTRY.md" ] || { echo "找不到仓库根（缺 META/REGISTRY.md）"; exit 2; }
cd "$ROOT"

FAIL=0; WARN=0
fail(){ printf '  \342\235\214 %s\n' "$*"; FAIL=$((FAIL+1)); }
warn(){ printf '  \342\232\240\357\270\217  %s\n' "$*"; WARN=$((WARN+1)); }
ok(){   printf '  \342\234\205 %s\n' "$*"; }

tmp=$(mktemp -d); trap 'rm -rf "$tmp"' EXIT
echo "# self-audit @ $(date +%F)"
echo "# root: $ROOT"

# ── A. 节点计数 / REGISTRY 单一真值源 ──────────────────────────────
echo; echo "## A 节点计数一致性（REGISTRY 是唯一真值源）"
find KNOWLEDGE -mindepth 2 -name meta.yaml -not -path '*_self_check*' -exec dirname {} \; \
  | xargs -n1 basename | sort -u > "$tmp/disk"
awk '/^## KNOWLEDGE nodes/{f=1}/^### /{f=0}f' META/REGISTRY.md \
  | grep -E '^\| [a-z]' | sed -E 's/^\| *([a-z0-9-]+).*/\1/' | grep -vx id | sort -u > "$tmp/reg"
dn=$(grep -c . "$tmp/disk"); rn=$(grep -c . "$tmp/reg")
mr=$(comm -23 "$tmp/disk" "$tmp/reg"); md=$(comm -13 "$tmp/disk" "$tmp/reg")
[ -n "$mr" ] && fail "节点在磁盘但 REGISTRY 缺登记: $(echo $mr)"
[ -n "$md" ] && fail "REGISTRY 有但磁盘无此节点: $(echo $md)"
[ -z "$mr$md" ] && ok "磁盘 $dn 节点 == REGISTRY $rn 行，一一对应"
fn=$(grep -m1 '新形态' META/REGISTRY.md | grep -oE '[0-9]+' | head -1)
[ "$fn" = "$dn" ] && ok "形态状态计数 $fn == $dn" || warn "形态状态写 $fn 但实际 $dn（硬编数字漂了）"

# ── B. 节点自含（节点 artifact 不引用 INBOX；层/域 README 是 process 文档，豁免）──
echo; echo "## B 节点自含（节点 artifact 不引用 INBOX）"
h=""
while IFS= read -r d; do
  x=$(grep -rl 'INBOX/' "$d" --include='*.md' --include='*.yaml' 2>/dev/null || true)
  [ -n "$x" ] && h="$h$x"$'\n'
done < <(find KNOWLEDGE -mindepth 2 -name meta.yaml -not -path '*_self_check*' -exec dirname {} \;)
[ -n "$h" ] && { fail "节点 artifact 引用了 INBOX 路径（违反自含不变量）："; printf '%s' "$h" | sed 's/^/      /'; } \
            || ok "节点 artifact 无 INBOX 引用（层/域 README 的 process 说明豁免）"

# ── C. meta.yaml 卫生 ─────────────────────────────────────────────
echo; echo "## C meta.yaml 卫生"
b=$(grep -rlE '^(status|last_reviewed_at):' KNOWLEDGE --include=meta.yaml 2>/dev/null | grep -v _self_check || true)
[ -n "$b" ] && { fail "节点 meta.yaml 又出现已废弃的 status / last_reviewed_at："; echo "$b" | sed 's/^/      /'; } \
            || ok "无已废弃字段"
miss=""
while IFS= read -r m; do
  for k in id title type created_at; do grep -qE "^$k:" "$m" || miss="$miss $m:$k"; done
done < <(find KNOWLEDGE -mindepth 2 -name meta.yaml -not -path '*_self_check*')
[ -n "$miss" ] && fail "meta.yaml 缺必填字段：$miss" || ok "id / title / type / created_at 齐全"

# ── D. WORK↔PROJECT 边界（通用层零项目事实）───────────────────────
echo; echo "## D WORK↔PROJECT 边界（WORK/ 整层不得把项目事实当内容）"
# 项目专有名：新增项目时在此补其"会泄漏到 WORK 的"短词（公司/产品/代号）
PROJECT_TERMS='neo|qiniu|七牛|zeroops'
# 扫整个 WORK/；豁免 provenance 引用行（含 [[…]] 或 PROJECTS/，WORK→PROJECTS 引用是允许的）
leak=$(grep -rinE "$PROJECT_TERMS" WORK 2>/dev/null | grep -vE '\[\[|PROJECTS/' || true)
[ -n "$leak" ] && { fail "WORK/ 疑似把项目事实当内容（应只在 PROJECTS/<project>/）："; echo "$leak" | sed 's/^/      /'; } \
              || ok "WORK/ 整层无项目事实（provenance 引用豁免）"

# ── E. ownership 单一权威（其余两处只能是镜像 banner）──────────────
echo; echo "## E ownership 单源"
e=1
grep -q 'CONTEXT.md` §1' README.md       || { warn "根 README ownership 段缺『权威在 CONTEXT §1』banner"; e=0; }
grep -q 'CONTEXT.md` §1' META/REGISTRY.md || { warn "REGISTRY 速查缺『权威在 CONTEXT §1』banner"; e=0; }
[ "$e" -eq 1 ] && ok "两处镜像 banner 在位"

# ── F. 根 README 不再硬编节点计数 ─────────────────────────────────
echo; echo "## F README 无硬编计数"
grep -qE '[0-9]+ *个节点' README.md && warn "根 README 仍硬编『N 个节点』，应指向 REGISTRY" || ok "未硬编计数"

echo; echo "## 结果: FAIL=$FAIL  WARN=$WARN"
[ "$FAIL" -gt 0 ] && exit 1 || exit 0
