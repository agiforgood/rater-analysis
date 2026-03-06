# 评分者一致性分析

心理咨询对话质量评估数据集的评分者间一致性分析。

## 背景

本项目分析了一组咨询/教练评估数据：咨询师与家长的对话，由观察者使用标准化量表进行评分，测量共情、咨访同盟和无条件积极关注。

**数据规模：** 36名评分者 × 20段对话 × 3个评估维度

## 数据文件

| 文件 | 说明 |
|------|------|
| `问卷对话内容0305.csv/xlsx` | 咨询师-家长对话文本（14个场景） |
| `问卷内容.csv/xlsx` | 问卷定义（题目、评分规则、量表结构） |
| `问卷0305.csv/xlsx` | 评分者的评分数据 |

## 数据流

```
问卷对话内容0305（对话文本）
        ↓  使用
问卷内容（评分量表）
        ↓  产出
问卷0305（评分结果）
```

## 三个评估维度

| 维度 | 量表 | 题目数 | 分值范围 |
|------|------|--------|----------|
| 共情 | TES（治疗师共情量表） | 9题（q1–q9） | 1–7 |
| 无条件积极关注 | 积极关注等级 | 1题 | 1–5 |
| 咨访同盟 | WAI-Observer-Short | 12题（item1–item12） | 1–7 |

## 分析脚本

| 脚本 | 功能 |
|------|------|
| `rater_agreement.py` | 评分者间一致性（ICC、成对距离、离群检测） |
| `question_divergence.py` | 逐题分歧分析、反向题效应、一致性聚类 |
| `analysis_centered_avg.py` | 评分者中心化平均 vs 原始平均 |
| `analysis_mfrm.py` | 多面Rasch模型（公平分数、方差分解） |
| `analysis_bayesian.py` | 层次贝叶斯模型（含可信区间的质量估计） |

## 分析报告

| 报告 | 内容 |
|------|------|
| [`analysis_summary_2026-03-07.md`](analysis_summary_2026-03-07.md) | **总结报告**（所有发现汇总） |
| [`evaluation_and_solutions_cn_2026-03-07.md`](evaluation_and_solutions_cn_2026-03-07.md) | **数据质量评估与应对方案**（中文） |
| [`feedback_rating_study_2026-03-07.md`](feedback_rating_study_2026-03-07.md) | 对研究设计的反馈 |
| [`next_round_recommendations_cn_2026-03-07.md`](next_round_recommendations_cn_2026-03-07.md) | **下一轮改进建议与试点方案**（中文） |
| [`analysis_rater_agreement_2026-03-07.md`](analysis_rater_agreement_2026-03-07.md) | 初始ICC与评分者偏差 |
| [`analysis_question_divergence_2026-03-07.md`](analysis_question_divergence_2026-03-07.md) | 逐题分歧与聚类 |
| [`analysis_centered_averaging_2026-03-07.md`](analysis_centered_averaging_2026-03-07.md) | 中心化平均分析 |
| [`analysis_mfrm_2026-03-07.md`](analysis_mfrm_2026-03-07.md) | 多面Rasch模型 |
| [`analysis_bayesian_2026-03-07.md`](analysis_bayesian_2026-03-07.md) | 层次贝叶斯模型 |
| [`analysis_exploratory_2026-03-07.md`](analysis_exploratory_2026-03-07.md) | 探索性分析（item12深入分析、逐对话ICC、双峰检测） |

## 核心发现

1. **评分者偏差占总方差的54%**——分数高低主要取决于"谁在评"，而非对话本身的质量
2. **尽管如此，36人平均后的对话排名是稳定的**——三种统计方法（中心化平均、MFRM、贝叶斯）给出几乎一致的排名
3. **TES共情量表在文本评分场景下基本失效**（ICC ≈ 0），WAI咨访同盟量表相对较好（ICC(2,36) = 0.73–0.80）
4. **反向计分题（WAI item4、item10）是分歧最大的题目**，建议改为正向表述
5. **98%的评分分布是单峰的**，取平均值是合理的

## 运行

```bash
# 安装依赖
uv sync

# 运行各分析脚本
uv run python rater_agreement.py
uv run python question_divergence.py
uv run python analysis_centered_avg.py
uv run python analysis_mfrm.py
uv run python analysis_bayesian.py
```

## 下一步

详见 [`next_round_recommendations_cn_2026-03-07.md`](next_round_recommendations_cn_2026-03-07.md)：
- 评分者校准会议
- 修改反向计分题
- 添加锚定示例
- TES量表试点验证
- 扩展无条件积极关注量表
