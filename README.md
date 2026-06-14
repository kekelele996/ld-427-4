# 装修预算与支出管理 API 服务

## Docker 启动

```bash
cp .env .env.local 2>/dev/null || true
docker compose up --build
```

- API 地址：http://localhost:19306/api/
- Swagger 地址：http://localhost:19306/api/schema/swagger-ui/
- DRF Browsable API：http://localhost:19306/api/budgets/

## 技术栈

| 层级 | 技术 |
| --- | --- |
| 后端 | Django 5 + Django REST Framework |
| 认证 | djangorestframework-simplejwt |
| API 文档 | drf-spectacular |
| 数据库 | PostgreSQL 15 |
| 缓存 | Redis 7 |
| 部署 | Docker Compose |

## 目录结构

```text
backend/
├── budget_app/
│   ├── views/
│   ├── serializers/
│   ├── services/
│   ├── middleware/
│   ├── filters/
│   ├── models.py
│   ├── permissions.py
│   ├── urls.py
│   └── admin.py
├── config/
└── manage.py
```

## 枚举位置

业务枚举集中定义在 `backend/budget_app/models.py` 的 `TextChoices` 中；同时按提示词保留 `backend/src/types/enums.ts` 作为跨端/文档对照。

## 核心接口

- `GET/POST /api/budgets/`
- `GET/POST /api/items/`
- `GET/POST /api/expenses/`
- `POST /api/expenses/{id}/submit/`
- `POST /api/expenses/{id}/approve/`
- `POST /api/expenses/{id}/pay/`
- `GET/POST /api/suppliers/`
- `GET/POST /api/reconciliations/`

## License

MIT
