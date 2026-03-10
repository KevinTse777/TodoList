# FastAPI Todo 学习进度

> 规则：每次我回复“完成”，教练在下一步先更新这里的勾选状态。

## A. 基础与工程骨架
- [x] `/api/v1` 路由前缀
- [x] 健康检查 `/api/v1/healthz`
- [x] 全局异常结构 `code/message/details`

## B. 用户与认证
- [x] 用户注册 `/api/v1/auth/register`
- [x] 密码哈希（bcrypt/passlib）
- [x] 登录接口（JSON 版）
- [x] JWT 签发函数 `create_access_token`
- [x] OAuth2 Password Flow 登录（官方推荐）
- [x] 获取当前用户 `/api/v1/auth/me`

## C. Todo 权限与业务
- [x] Todo 表含 `owner_id`
- [x] Todo 不再硬编码 `owner_id=1`，改为当前登录用户
- [x] 仅允许访问自己的 todos

## D. 数据库与迁移
- [x] MySQL 连接
- [x] Alembic 初始迁移（users/todos）
- [ ] 第二次迁移演练（字段变更）

## E. 容器与部署
- [ ] Dockerfile（backend）
- [ ] docker-compose（db/backend/frontend）
- [ ] 本地一键启动与迁移命令
- [ ] 部署说明（Nginx/ENV/卷/启动方式）

## F. 代码注释标准（从现在开始执行）
- [ ] 每个新增函数至少 1 条“做什么/为什么”的注释
- [ ] 涉及认证、权限、数据库提交处必须有注释
- [ ] 路由层注释“参数职责”，Service 层注释“业务职责”
