# 智能体对话与评估 — 技术设计

## 1. 可自定义的家长提示词

**涉及模块**: 后端脚本 + API

目前 `create_session()` 从 `resources/parent_profiles/*.txt` 文件中加载家长配置文件。

**实现要点**:

- 脚本：添加 `--parent-prompt` / `--parent-prompt-file` 参数（与 `--parent-profile-id` 互斥）
- API：在运行请求体中接受可选的 `parent_prompt` 字段
- 当提供了自定义家长提示词时，完全跳过 `parent_profile_service`，将其直接传递给 `create_session(parent_profile=...)`
- 输出 JSON：当使用用户提供的提示词时，记录 `"parent_profile": "custom"`

## 2. 生成与评估不设置超时

**涉及模块**: 后端 API（+ 前端感知）

**实现要点**:

- API 层：**不要**在生成端点上设置请求超时
- ASGI 配置：确保 `uvicorn --timeout-keep-alive` 和任何反向代理（如 nginx 的 `proxy_read_timeout`）设置得足够高，或者针对该端点禁用
- 脚本：已经通过 `asyncio.run()` 运行且没有超时限制——无需更改
- 前端：绝不能使用短时间的 `fetch` 超时；参见功能点 3

## 3. 异步任务架构

**涉及模块**: 前端（主要）、后端 API

### 后端

- **任务创建端点**: `POST /api/v1/coach/runs` 立即返回 `run_id` 和状态 `"pending"`
- **后台执行**: 实际的对话 + 评估在后台 worker 中运行（例如 FastAPI 的 `BackgroundTasks`，或者如果需要扩展则使用 Celery/ARQ 等任务队列）
- **状态轮询端点**: `GET /api/v1/coach/runs/{run_id}` 返回当前状态（`pending` → `running` → `completed` | `failed`）、进度信息（当前轮次 / 总轮次、正在运行哪个评估维度）以及完成后的结果
- **结果存储在数据库**: 对话 + 评估的 JSON 保存到 `coach_run` 表中，使其在请求生命周期之外持久化

### 前端

- 用户点击 "Generate" → 获得带有 `run_id` 的确认，UI 显示状态为 "Running..." 的任务卡片
- 轮询或 SSE 更新卡片状态
- 完成后点击查看结果（对话 + 评估查看器）

### 序列图

```
用户                    前端                      后端
 |-- 点击 Generate -->  |                         |
 |                       |-- POST /runs ---------->|
 |                       |<-- 201 {run_id} --------|
 |<-- 显示任务卡片 ---    |                         |-- 启动后台任务
 |                       |                         |   (对话 + 评估)
 |   (用户进行           |                         |
 |    其他操作)          |-- GET /runs/{id} ------>|
 |                       |<-- {status: running} ---|
 |                       |-- GET /runs/{id} ------>|
 |                       |<-- {status: completed,  |
 |                       |     result: {...}} -----|
 |<-- 显示结果 -------   |                         |
```
