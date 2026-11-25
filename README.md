# rose-panel-bot · auto-deploy

这个分支（`deploy`，默认分支）只放部署脚本；`main` 分支保持和上游 [mango0114/rose-panel-bot](https://github.com/mango0114/rose-panel-bot) 一致。

- 每 15 分钟检查上游 latest release；tag 与 `DEPLOYED_TAG` 不同就依次执行：安装 → 测试 → 构建 → `wrangler deploy` → `/health` → `/setup`。测试不通过就不部署。
- 回滚：Actions → Run workflow，`tag` 填旧版本（如 `v1.2.2`）。强制重部署：勾选 `force`。
- `static/` 下的文件会覆盖进构建产物（例如 `avatar.png`）。

Secrets（全部在 Actions Secrets，不入库）：`CLOUDFLARE_API_TOKEN`、`CLOUDFLARE_ACCOUNT_ID`、`WEBHOOK_SECRET`、`KV_ID`、`ADMIN_IDS`。
`BOT_TOKEN` 只存在 Cloudflare Worker secret 里，不经过 GitHub。
