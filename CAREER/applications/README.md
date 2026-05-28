# Applications

真实投递工作区。这里记录已经投、准备投、正在沟通和已经结束的岗位。

## 和其它目录的边界

| 目录 | 作用 | 是否记录真实投递动作 |
|---|---|---|
| `RAW_SOURCES/jd-and-interviews/` | JD / 面经 / HR 信息原始素材 | 否 |
| `CAREER/target-roles/` | 目标岗位画像和投递方向判断 | 否 |
| `CAREER/applications/` | 每一次投递、沟通、面试和跟进 | 是 |

原则：不要把这里变成第二个 JD 素材库。JD 原文长期放在 `RAW_SOURCES`；这里保留岗位快照、匹配判断、投递材料和下一步动作。

## 目录结构

```text
applications/
├── README.md
├── pipeline.md                 # 总投递看板
├── prep-backlog.md             # active JD / 面经反推的短期学习清单
├── templates/
│   └── application.template.md  # 单岗位记录模板
├── active/                      # 待投 / 已投 / 沟通中 / 面试中
├── archived/
│   ├── rejected/                # 明确拒绝
│   ├── no-response/             # 长期无回复
│   └── closed/                  # 岗位关闭 / 自己放弃 / offer 后归档
└── snippets/
    ├── boss-greetings.md
    ├── referral-messages.md
    └── follow-up-messages.md
```

## 状态枚举

| 状态 | 含义 |
|---|---|
| `待投` | 已判断匹配，但还没发出 |
| `已投递` | 简历 / Boss / 官网 / 内推已发出 |
| `沟通中` | HR / 内推人 / 用人团队正在回复 |
| `面试中` | 已进入面试流程 |
| `待跟进` | 到了应该补发消息或确认进度的时间 |
| `拒绝` | 明确拒绝 |
| `无回复归档` | 超过预设周期无回复 |
| `关闭` | 岗位关闭、自己放弃或流程结束 |
| `offer` | 拿到 offer |

## 使用流程

1. 看到新岗位时，如果只是素材，先放 `RAW_SOURCES/jd-and-interviews/`。
2. 决定要投时，从 `templates/application.template.md` 复制到 `active/YYYY-MM-DD_company_role.md`。
3. 在 `pipeline.md` 增加一行，保持状态、下一步和详情链接同步。
4. 面试后把问题和复盘沉淀到该岗位文件；能复用的题再进 `CAREER/interview-bank/`。
5. 流程结束后，把文件移到 `archived/` 对应目录，并更新 `pipeline.md`。

## 命名规则

单岗位文件：

```text
YYYY-MM-DD_company_role.md
```

示例：

```text
2026-05-17_huawei_group-it_ai-intern.md
```

日期使用首次投递或准备投递日期。公司名和岗位名用小写英文或拼音，尽量短。
