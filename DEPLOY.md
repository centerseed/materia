# 原鑑 Materia — Firebase Hosting 部署指南

靜態網站部署到 Firebase Hosting。設定檔自包含在 `materia/`，部署一律在 `materia/` 目錄下執行。

## 部署什麼

- 部署目錄：`materia/site/`（`public: "site"`）—— 只含前端（`index.html`、`runtime.js`、`app-data.js`，及日後的 `data/`、`assets/`）。
- **不會部署** `materia/ingredients/`（那是爬取來源素材，非網站內容），也不會部署 `schema/`、`tests/`、`validate.py`。

## 前置需求（一次性）

- Node.js（已具備 v20）與 firebase-tools（已安裝：`firebase --version`）。若未裝：`npm i -g firebase-tools`。
- 一個 Firebase 專案（在 https://console.firebase.google.com 建立，或用 CLI 建立）。

## 首次設定

1. 登入（互動式，需你本人操作）。在 Claude Code 輸入框執行：

   ```
   ! firebase login
   ```

2. 綁定 Firebase 專案 ID（把 `.firebaserc` 的 `REPLACE_WITH_YOUR_FIREBASE_PROJECT_ID` 換成你的專案 ID），或用 CLI：

   ```
   ! cd materia && firebase use --add
   ```

   （若還沒有專案，可先 `! firebase projects:create <your-project-id>`。）

## 部署

```
! cd materia && firebase deploy --only hosting
```

完成後 CLI 會印出線上網址（`https://<project-id>.web.app`）。

## 上線前先本機預覽（可選）

```
! cd materia && firebase emulators:start --only hosting
```

或用純靜態伺服器：`cd materia/site && python3 -m http.server 8137`，開 http://localhost:8137。

## 預覽頻道（staging，可選）

給利害關係人看未上線版本，不影響正式站：

```
! cd materia && firebase hosting:channel:deploy preview
```

## 設定說明（firebase.json）

- `cleanUrls: true`：`/foo` 對應 `foo.html`，網址更乾淨。
- `rewrites: ** → /index.html`：目前網站是單頁（畫面用前端狀態切換、網址不變），此改寫為日後加入網址路由時預留；既有實體檔案仍優先直接提供。
- 快取：`index.html` 不快取（每次拿最新）、JS 1 小時、JSON 10 分鐘、圖片 7 天。

## 已知限制與後續

- **單頁、無網址路由**：目前重新整理都會回到首頁，深層連結（分享某個原材料頁）尚不支援。要支援需加入前端路由（hash 或 History API）＋對應狀態還原——列為後續增強。
- **資料仍為 DEMO**：`site/app-data.js` 是設計示意資料。接真實資料時，把各原材料 JSON 放到 `site/data/`（fetch 相對路徑即可被 Hosting 提供），圖片放 `site/assets/`。
