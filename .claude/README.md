# 经管博士论文 Skills 配置

这个目录配置了一组用于经管(经济/管理)博士论文写作的 Claude Code skills。

## 一键安装

```bash
bash .claude/scripts/setup-academic-skills.sh
```

执行后,以下 skills 会出现在你的 Claude Code 里(用户级 `~/.claude/skills/`):

| Skill | 用途 | 触发命令 |
|---|---|---|
| `deep-research` | 13-agent 文献综述与系统综述 | `/deep-research` |
| `academic-paper` | 12-agent 学术论文写作 pipeline | `/academic-paper` |
| `academic-paper-reviewer` | 多视角同行评议(EIC + 3 审稿人 + Devil's Advocate) | `/academic-paper-reviewer` |
| `academic-pipeline` | research→write→review→revise 全流程编排 | `/academic-pipeline` |
| `academic-paper-strategist` | 论文规划:选题、文献缺口、提纲 | `/academic-paper-strategist` |
| `academic-paper-composer` | 从提纲到完稿的系统化写作 | `/academic-paper-composer` |
| `econ-write` | 经济学论文写作专家(综合 Cochrane/McCloskey/Shapiro 等 50+ 经济学家方法论;IV/DiD/RDD/structural 等) | `/econ-write` |
| `zh-en-academic` | 中英混合学术风格适配器(本仓库自定义) | `/zh-en-academic` |

## 来源

- [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills) — CC-BY-NC 4.0,作者 Cheng-I Wu
- [lishix520/academic-paper-skills](https://github.com/lishix520/academic-paper-skills)
- [hanlulong/econ-writing-skill](https://github.com/hanlulong/econ-writing-skill)

`zh-en-academic` 是本仓库为经管中文论文场景自定义的风格 skill,详见 `.claude/skills/zh-en-academic/SKILL.md`。

## 更新

```bash
bash .claude/scripts/setup-academic-skills.sh --update
```

## 网页版会话

`.claude/skills/zh-en-academic/` 在仓库里,网页版会话 clone 仓库时自动可用。
其他三个仓库的 skills 需在网页会话启动后跑一次 `setup-academic-skills.sh`,或者在 [`.claude/settings.json`](https://code.claude.com/docs/en/claude-code-on-the-web) 里把它们配成 setup script 自动执行。

## License 提醒

`academic-research-skills` 为 CC-BY-NC 4.0,**非商业用途可用**;博士论文写作通常属于个人学术用途。若涉及商业咨询场景请联系原作者。
