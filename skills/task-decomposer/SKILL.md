# Task Decomposer - 任务自动分解技能

## 功能说明

将复杂任务自动分解为可执行的子任务，支持并行执行和结果汇总。

## 核心能力

1. **任务分解**：基于 LLM 将复杂任务拆分为独立子任务
2. **依赖分析**：识别子任务之间的依赖关系
3. **并行执行**：无依赖的子任务并行执行
4. **结果汇总**：自动合成子任务结果为最终答案

## 任务分解算法

```python
def decompose_task(complex_task, max_subtasks=5):
    """
    将复杂任务分解为子任务
    
    Args:
        complex_task: 复杂任务描述
        max_subtasks: 最大子任务数
    
    Returns:
        subtasks: 子任务列表（含依赖关系）
    """
    prompt = f"""
将以下复杂任务分解为 {max_subtasks} 个以内的独立子任务：

任务：{complex_task}

要求：
1. 每个子任务应该是独立可执行的
2. 标注子任务之间的依赖关系
3. 识别可以并行执行的子任务
4. 输出 JSON 格式

示例输出：
{{
  "subtasks": [
    {{"id": 1, "name": "搜索 AI 开发工具", "dependencies": [], "parallel": true}},
    {{"id": 2, "name": "分析工具特点", "dependencies": [1], "parallel": false}},
    {{"id": 3, "name": "生成对比表格", "dependencies": [2], "parallel": false}}
  ]
}}
"""
    response = llm.generate(prompt)
    return parse_json(response)
```

## 执行引擎

```python
async def execute_decomposed_task(complex_task):
    # 1. 分解任务
    decomposition = decompose_task(complex_task)
    
    # 2. 构建执行图
    execution_graph = build_execution_graph(decomposition)
    
    # 3. 并行执行无依赖任务
    results = {}
    for level in execution_graph.levels:
        parallel_tasks = [t for t in level if t.can_execute(results)]
        parallel_results = await asyncio.gather(
            *[execute_subtask(task) for task in parallel_tasks]
        )
        results.update(parallel_results)
    
    # 4. 汇总结果
    final_result = synthesize_results(results)
    return final_result
```

## 使用场景

当用户说：
- "研究 2026 年 AI 开发工具趋势，生成报告"
- "帮我分析这个项目的优缺点，给出改进建议"
- "对比 Deer-Flow、Hermes-Agent、ECC 三个框架"

## 输出格式

```markdown
## 任务执行报告

### 任务分解
- 子任务 1：✅ 完成（耗时 10s）
- 子任务 2：✅ 完成（耗时 15s）
- 子任务 3：✅ 完成（耗时 8s）

### 执行方式
- 并行执行：子任务 1、3
- 串行执行：子任务 2（依赖子任务 1）

### 总耗时
25 秒（相比串行节省 8 秒）

### 结果汇总
[最终答案]
```

## 配置选项

| 选项 | 默认值 | 说明 |
|------|--------|------|
| max_subtasks | 5 | 最大子任务数 |
| enable_parallel | true | 是否启用并行执行 |
| timeout_per_task | 60s | 单个任务超时时间 |
| retry_count | 2 | 失败重试次数 |

---

**版本**: 1.0.0
**作者**: OpenClaw Partner
**最后更新**: 2026-03-26
