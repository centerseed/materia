# 原材料頁資料萃取規格（給 subagent）

把某個原材料爬回的素材，整理成一份「頁面 JSON」給原鑑 Materia 前端用，並挑好配圖。

## 核心合規原則（必守）
保健食品不用藥品標準評斷。機轉／細胞／生物標記／健康人研究都是正當證據；缺病患試驗 ≠ 無證據。
證據成熟度只決定「措辭合規」，不判定有效性。**禁止**「治療」「治癒」「降低數值」等療效字眼。
⚠️ 陰性結果與研究對象據實呈現（為透明，非看衰）。

## 讀哪些檔（都用 Read/ls/grep，勿臆造數字）
- `materia/ingredients/{id}/supplier/*.html`：機制、規格、專利（原廠說明）
- `materia/ingredients/{id}/supplier/images/**`：原廠頁面圖（挑配圖用）
- `materia/ingredients/{id}/research/*.md` 或 `*.html`、`research_index.md`：論文（evidence）
- `materia/ingredients/{id}/youtube/*.html`：影片（videos，若無則 videos:[]）
- 若 `ingredients/{id}/`（專案根，非 materia）存在，其 `research/`、`youtube/`、`research/images/` 也要一起讀（floraglo/pureway-c/spms 的論文與影片在這裡）。

## 產出
寫檔到 `materia/site/data/{id}.json`，UTF-8，結構如下（欄位齊全，無資料的陣列給 []）：

```json
{
  "id": "",
  "name": "中文名",
  "brand": "英文/商標，如 ThymoQuin®",
  "oneLine": "索引卡用的一句話（≤40字）",
  "desc": "Hero 段落，2-3句：這是什麼、研究主要探討什麼族群/狀況",
  "domains": ["健康領域1","健康領域2"],
  "groups": ["適合族群1","適合族群2"],
  "chips": ["索引卡標籤1","標籤2"],
  "lvl": 3,
  "mech": {
    "image": "assets/{id}/檔名.jpg",
    "caption": "圖說",
    "summary": "3-4句白話學理：為什麼會作用、身體裡發生什麼",
    "points": ["機制要點1","要點2","要點3"],
    "detail": "展開的完整機制敘述（1段）"
  },
  "specs": [{"k":"專利/商標","v":""},{"k":"形式","v":""},{"k":"常見規格","v":""},{"k":"主要依據","v":""}],
  "evidence": [
    {
      "id": "amd",
      "domain": "健康領域",
      "lvl": 2,
      "oneLine": "一句話結論",
      "subjects": "研究對象（健康人/患者/高風險）",
      "papers": "約 N 篇",
      "compliance": "合規措辭一句",
      "studies": [
        {"title":"","stars":"★★★★","year":"2013","journal":"JAMA · IF≈120","type":"RCT","n":"4203","subjects":"","key":"關鍵數字","caveat":"⚠️但書/陰性結果","coi":"利益衝突","link":"PMID或URL"}
      ]
    }
  ],
  "claims": [{"claim":"廠商常這樣說…","evidence":"研究實際支持到…","who":"研究對象備註"}],
  "safety": [{"tag":"劑量","title":"","items":["",""]}],
  "videos": [{"name":"講者","title":"頭銜","summary":"重點","link":"URL"}]
}
```

### lvl 判定（證據成熟度）
- 3 證據充分：有 meta-analysis 或多篇一致陽性人體 RCT
- 2 證據發展中：有人體研究但累積中/部分不一致
- 1 機轉／生標支持：以機轉/細胞/生標為主，人體證據初步

`evidence` 每個領域也各自給 lvl。至少 3 個領域、每領域 1-2 篇 studies。claims 3 條、safety 3-4 張卡。

## 配圖（重要：純文字很痛苦，一定要配圖）
1. `ls materia/ingredients/{id}/supplier/images/`（及根 research/images）找有內容的圖。
2. 挑 1 張最能當「機制/主視覺」的圖 → `mkdir -p materia/site/assets/{id}` → `cp` 過去 → 填 `mech.image`（路徑寫成 `assets/{id}/檔名`）。
3. 可另挑 1-2 張論文圖表，但總數 ≤3 張，避免肥大。跳過純 logo/空白圖。

## 完成後
- 確認 `materia/site/data/{id}.json` 是合法 JSON（`python3 -m json.tool` 檢查）。
- 回報：抓到幾個領域/幾篇論文/幾支影片、複製了幾張圖、有無缺漏。
