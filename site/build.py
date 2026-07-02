#!/usr/bin/env python3
"""原鑑 Materia 建置：
1) 把 index.html 的原材料頁從「寫死葉黃素」改成通用綁定版（一次性、可重複執行）。
2) 從 site/data/*.json 產生 site/app-data.js（真實資料 baked-in）。
用法：cd materia/site && python3 build.py
"""
import json
import pathlib

SITE = pathlib.Path(__file__).resolve().parent
DATA_DIR = SITE / "data"

# ---------- 1) patch index.html ----------
idx = (SITE / "index.html").read_text(encoding="utf-8")

REPLACEMENTS = [
    # sc-if 切換 + screen label
    ('value="{{ isLutein }}"', 'value="{{ isIngredient }}"'),
    ('data-screen-label="Ingredient · 葉黃素"', 'data-screen-label="Ingredient"'),
    # 麵包屑 / 標題 / 商標 / 敘述
    ('<span style="color:#55514A;">葉黃素</span>',
     '<span style="color:#55514A;">{{ curName }}</span>'),
    ('line-height:1.1;">葉黃素</h1>',
     'line-height:1.1;">{{ curName }}</h1>'),
    ('letter-spacing:0.02em;">Lutein · FloraGLO®</span>',
     'letter-spacing:0.02em;">{{ curBrand }}</span>'),
    ('存在於視網膜黃斑部的類胡蘿蔔素，能吸收高能藍光、清除自由基。研究主要探討它對<strong style="color:#234139;">長時間用眼族群與年齡相關黃斑部退化</strong>的支持。',
     '{{ curDesc }}'),
    # 機制配圖：placeholder → 真圖
    ('''<div style="position:relative; aspect-ratio:4/3.4; border-radius:12px; background:repeating-linear-gradient(135deg,#ECE6D7,#ECE6D7 10px,#E7E1D0 10px,#E7E1D0 20px); border:1px solid #DDD6C4; display:flex; align-items:flex-end; padding:16px;">
            <span style="font-family:ui-monospace,monospace; font-size:11px; color:#8A857B; background:rgba(252,250,243,0.9); padding:5px 9px; border-radius:5px;">原廠機轉示意圖：黃斑部葉黃素堆積 / 藍光濾除</span>
          </div>''',
     '''<div style="position:relative; aspect-ratio:4/3.4; border-radius:12px; overflow:hidden; border:1px solid #DDD6C4; background:#ECE6D7;">
            <img src="{{ mechImage }}" alt="{{ mechCaption }}" style="width:100%; height:100%; object-fit:cover; display:block;">
            <span style="position:absolute; left:12px; bottom:12px; font-family:ui-monospace,monospace; font-size:11px; color:#8A857B; background:rgba(252,250,243,0.92); padding:5px 9px; border-radius:5px;">{{ mechCaption }}</span>
          </div>'''),
    # 機制摘要段
    ('<p style="font-size:16.5px; color:#33302B; margin:0 0 16px; line-height:1.8;">葉黃素與玉米黃素是<strong style="color:#234139;">黃斑部色素（MPOD）</strong>的主要組成，會選擇性堆積在視網膜中央。</p>',
     '<p style="font-size:16.5px; color:#33302B; margin:0 0 16px; line-height:1.8;">{{ mechSummary }}</p>'),
    # 機制要點清單 → sc-for
    ('''<li style="display:flex; gap:12px; font-size:15.5px; color:#44403A;"><span style="color:#234139; font-weight:700;">01</span><span>作為<strong>濾光層</strong>吸收高能藍光，降低光氧化壓力。</span></li>
            <li style="display:flex; gap:12px; font-size:15.5px; color:#44403A;"><span style="color:#234139; font-weight:700;">02</span><span>作為<strong>脂溶性抗氧化劑</strong>，清除光受器代謝產生的自由基。</span></li>
            <li style="display:flex; gap:12px; font-size:15.5px; color:#44403A;"><span style="color:#234139; font-weight:700;">03</span><span>人體<strong>無法自行合成</strong>，需由飲食或補充攝取。</span></li>''',
     '''<sc-for list="{{ mechPoints }}" as="mp" hint-placeholder-count="3"><li style="display:flex; gap:12px; font-size:15.5px; color:#44403A;"><span style="color:#234139; font-weight:700;">{{ mp.n }}</span><span>{{ mp.t }}</span></li></sc-for>'''),
    # 機制展開詳述
    ('FloraGLO® 為萬壽菊（marigold）萃取的<strong>游離型葉黃素（free lutein）</strong>，相較酯化型不需經腸道酯解即可吸收，原廠以此主張較穩定的生體可用率。補充後血清葉黃素通常於數週內上升，而黃斑部色素密度（MPOD）的變化則需 3–6 個月方能觀察。MPOD 提升被視為一項<strong>可測量的生物標記</strong>，但它與「主觀視覺改善」之間並非線性對應——這也是解讀相關研究時的關鍵。',
     '{{ mechDetail }}'),
]

patched = 0
for old, new in REPLACEMENTS:
    if old in idx:
        idx = idx.replace(old, new)
        patched += 1
(SITE / "index.html").write_text(idx, encoding="utf-8")
print(f"index.html: {patched}/{len(REPLACEMENTS)} 段替換完成")

# ---------- 2) build app-data.js ----------
DATA = {}
for f in sorted(DATA_DIR.glob("*.json")):
    if f.name.startswith("_"):
        continue
    DATA[f.stem] = json.loads(f.read_text(encoding="utf-8"))

data_js = json.dumps(DATA, ensure_ascii=False, indent=2)

# 搭配範例（依現有原料、有學理基礎的真實組合；語氣客觀正向）
COMBOS = [
    {
        "id": "lutein-omega3",
        "title": "葉黃素 ＋ 魚油 Omega-3",
        "lvl": 2,
        "oneLine": "護眼與大腦的經典組合：葉黃素沉積於黃斑部，DHA 是視網膜與神經細胞膜的結構脂質。",
        "desc": "兩者分屬「保護」與「結構」兩個面向——葉黃素在黃斑部形成濾光與抗氧化層，Omega-3 的 DHA 則是視網膜感光細胞與神經細胞膜的主要組成。各自的人體研究都相當豐富，是長期護眼保養常見的搭配。",
        "members": [
            {"id": "floraglo", "name": "葉黃素", "brand": "FloraGLO®"},
            {"id": "vivomega", "name": "魚油 Omega-3", "brand": "VivoMega®"},
        ],
        "synergy": [
            {"h": "作用位置互補", "p": "葉黃素選擇性堆積在黃斑部，作為濾光與抗氧化層；DHA 構成視網膜與神經細胞膜，兩者覆蓋不同層面。"},
            {"h": "吸收相輔", "p": "葉黃素為脂溶性，與含油脂的魚油同時攝取有助於吸收。"},
            {"h": "研究脈絡", "p": "兩者各自的人體研究豐富；直接比較「複方 vs 單方」的協同試驗仍在累積中。"},
        ],
        "evidence": [
            {"domain": "眼睛健康", "lvl": 2, "oneLine": "各自對黃斑色素密度與視覺機能均有人體研究支持，複方協同數據持續累積。"},
            {"domain": "認知 / 神經", "lvl": 1, "oneLine": "葉黃素與 DHA 皆存在於腦部，與認知的關聯以機轉與觀察性研究為主。"},
        ],
        "risks": [
            "兩者皆為脂溶性，建議隨餐食用；同時補充多種脂溶性營養素時留意整體攝取量。",
            "服用抗凝血藥物者，補充較高劑量魚油前宜先諮詢醫師或藥師。",
        ],
    },
    {
        "id": "collagen-vitc",
        "title": "膠原蛋白 ＋ 維生素C",
        "lvl": 2,
        "oneLine": "維生素C 是膠原蛋白合成的必需輔因子，與膠原蛋白胜肽是常見的美容與關節搭配。",
        "desc": "膠原蛋白胜肽提供合成所需的胺基酸原料，維生素C 則是膠原蛋白合成過程中關鍵酵素的必需輔因子——兩者一個是「原料」、一個是「必需的助手」，在生化上有明確的互補關係。",
        "members": [
            {"id": "nippi-collagen", "name": "膠原蛋白", "brand": "NIPPI®"},
            {"id": "pureway-c", "name": "維生素C", "brand": "PureWay-C®"},
        ],
        "synergy": [
            {"h": "生化上必需", "p": "維生素C 是脯胺酸、離胺酸羥化酶的輔因子，膠原蛋白的正常合成需要它參與。"},
            {"h": "原料與助手分工", "p": "膠原胜肽提供胺基酸原料，維生素C 支援其轉化並提供抗氧化保護。"},
            {"h": "研究脈絡", "p": "兩者各自的人體研究較多；直接針對複方的協同試驗相對較少。"},
        ],
        "evidence": [
            {"domain": "皮膚美容", "lvl": 2, "oneLine": "膠原胜肽對皮膚彈性與保濕有人體研究；維生素C 為合成必需輔因子，機理明確。"},
            {"domain": "關節 / 結締組織", "lvl": 1, "oneLine": "以機轉與初步研究為主，支持結締組織的原料與輔因子搭配思路。"},
        ],
        "risks": [
            "維生素C 於每日建議量下安全；一次攝取極高劑量可能造成腸胃不適。",
            "膠原蛋白為蛋白質，對特定來源（魚、海鮮）過敏者請留意原料來源。",
        ],
    },
    {
        "id": "spm-omega3",
        "title": "SPM ＋ 魚油 Omega-3",
        "lvl": 2,
        "oneLine": "上下游關係：魚油提供 EPA/DHA 原料，身體再轉化成主動「收尾」發炎的 SPM 訊號分子。",
        "desc": "專門促消炎介質（SPM）是 Omega-3 脂肪酸在體內轉化出的活性代謝產物，負責主動引導發炎反應「消退收尾」。魚油補足前驅物原料池，直接補充 SPM 則跳過轉化步驟——兩者是清楚的上下游互補。",
        "members": [
            {"id": "spms", "name": "SPM 促消炎介質", "brand": "SPM"},
            {"id": "vivomega", "name": "魚油 Omega-3", "brand": "VivoMega®"},
        ],
        "synergy": [
            {"h": "上下游關係", "p": "EPA/DHA 是 SPM 的前驅物，SPM 是其活性代謝產物，方向一致。"},
            {"h": "原料與訊號分工", "p": "魚油提供充足原料池，SPM 直接補足「發炎消退」的訊號分子。"},
            {"h": "研究脈絡", "p": "魚油的人體證據豐富；SPM 為新興領域，複方數據仍在累積。"},
        ],
        "evidence": [
            {"domain": "發炎調節", "lvl": 2, "oneLine": "魚油對發炎相關指標有較多人體研究；SPM 直接參與發炎消退，機轉明確、人體證據累積中。"},
            {"domain": "心血管 / 關節", "lvl": 1, "oneLine": "以機轉與初步研究為主，支持發炎相關的原料搭配思路。"},
        ],
        "risks": [
            "兩者皆為脂溶性，建議隨餐食用；服用抗凝血藥物者補充較高劑量魚油前宜諮詢醫師。",
            "SPM 為新興原料，長期高劑量的人體資料仍有限。",
        ],
    },
    {
        "id": "collagen-cuberup",
        "title": "膠原蛋白 ＋ 黃瓜萃取",
        "lvl": 2,
        "oneLine": "關節保養的「結構 ＋ 舒適」組合：膠原提供結締組織原料，黃瓜萃取支持關節舒適與活動。",
        "desc": "膠原蛋白胜肽是軟骨與結締組織的胺基酸原料；Euromed 專利黃瓜萃取（CuberUp®）則有人體研究支持關節舒適與活動表現。一個顧「結構原料」、一個顧「使用舒適」，是關節保養常見的互補搭配。",
        "members": [
            {"id": "nippi-collagen", "name": "膠原蛋白", "brand": "NIPPI®"},
            {"id": "cuberup", "name": "黃瓜萃取", "brand": "CuberUp®"},
        ],
        "synergy": [
            {"h": "結構與舒適互補", "p": "膠原提供結締組織原料，黃瓜萃取支持關節舒適與活動表現。"},
            {"h": "機轉不同", "p": "一為原料補充，一走抗氧化與一氧化氮相關路徑，覆蓋不同面向。"},
            {"h": "研究脈絡", "p": "兩者各自有人體研究；直接比較複方的協同試驗較少。"},
        ],
        "evidence": [
            {"domain": "關節骨骼", "lvl": 2, "oneLine": "兩者各自對關節舒適與結締組織有人體研究支持。"},
            {"domain": "運動 / 活動表現", "lvl": 1, "oneLine": "以初步研究與機轉為主。"},
        ],
        "risks": [
            "膠原蛋白為蛋白質，對特定來源（魚、海鮮）過敏者請留意來源。",
            "關節保養屬長期方向，效果需持續數週至數月累積。",
        ],
    },
    {
        "id": "blackseed-omega3",
        "title": "黑種草籽油 ＋ 魚油 Omega-3",
        "lvl": 2,
        "oneLine": "兩種機轉互補的脂溶性活性來源，常見於心血管代謝與發炎調節的搭配。",
        "desc": "黑種草籽油富含百里醌等活性成分，魚油則提供 EPA/DHA。兩者分屬不同的脂溶性活性來源，在代謝與發炎相關的研究方向上一致，適合作為互補搭配。",
        "members": [
            {"id": "thymoquin", "name": "黑種草籽油", "brand": "ThymoQuin®"},
            {"id": "vivomega", "name": "魚油 Omega-3", "brand": "VivoMega®"},
        ],
        "synergy": [
            {"h": "活性成分互補", "p": "百里醌與 EPA/DHA 屬不同活性來源，機轉互補。"},
            {"h": "吸收相輔", "p": "皆為脂溶性，隨含油脂餐食用有助吸收。"},
            {"h": "研究脈絡", "p": "兩者各自有人體研究；複方協同數據仍在累積。"},
        ],
        "evidence": [
            {"domain": "心血管代謝", "lvl": 2, "oneLine": "兩者各自對代謝相關指標有人體研究支持。"},
            {"domain": "發炎 / 過敏", "lvl": 1, "oneLine": "以機轉與初步研究為主。"},
        ],
        "risks": [
            "服用抗凝血或降血壓藥物者，併用前宜先諮詢醫師或藥師。",
            "皆為脂溶性，留意整體油脂與熱量攝取。",
        ],
    },
    {
        "id": "collagen-eggshell",
        "title": "膠原蛋白 ＋ 蛋殼膜",
        "lvl": 2,
        "oneLine": "皮膚與關節結締組織的原料互補：膠原胜肽 ＋ 蛋殼膜的彈性蛋白與醣胺聚醣。",
        "desc": "蛋殼膜天然含有膠原蛋白、彈性蛋白與醣胺聚醣（如玻尿酸、軟骨素等）；與膠原蛋白胜肽搭配，能為皮膚與關節的結締組織提供更多元的原料組成。",
        "members": [
            {"id": "nippi-collagen", "name": "膠原蛋白", "brand": "NIPPI®"},
            {"id": "ovoderm", "name": "蛋殼膜", "brand": "OVODERM®"},
        ],
        "synergy": [
            {"h": "原料互補", "p": "膠原胜肽提供胺基酸原料，蛋殼膜額外帶來彈性蛋白與醣胺聚醣。"},
            {"h": "皮膚與關節雙面向", "p": "兩者研究皆橫跨皮膚保養與關節結締組織。"},
            {"h": "研究脈絡", "p": "各自有初步至中等人體研究；複方直接數據有限。"},
        ],
        "evidence": [
            {"domain": "皮膚美容", "lvl": 2, "oneLine": "兩者各自對皮膚彈性與保濕有人體研究支持。"},
            {"domain": "關節骨骼", "lvl": 1, "oneLine": "以初步研究與機轉為主。"},
        ],
        "risks": [
            "對蛋、魚或海鮮過敏者，請留意各成分的原料來源。",
            "皮膚與關節保養屬長期方向，效果需持續累積。",
        ],
    },
]
combos_js = json.dumps(COMBOS, ensure_ascii=False, indent=2)

COMPONENT = r"""
class Component extends DCLogic {
  state = { view:'home', filter:'全部', currentId:null, currentComboId:null, mechOpen:false, openDomain:null };

  go(v){ this.setState({ view:v }); if(typeof window!=='undefined') window.scrollTo(0,0); }

  badge(lvl){
    const map = {
      3:{ label:'證據充分', color:'oklch(0.5 0.075 155)', tint:'oklch(0.955 0.022 155)', border:'oklch(0.86 0.045 155)' },
      2:{ label:'證據發展中', color:'oklch(0.5 0.08 258)', tint:'oklch(0.955 0.022 258)', border:'oklch(0.86 0.045 258)' },
      1:{ label:'機轉／生標支持', color:'oklch(0.5 0.075 312)', tint:'oklch(0.955 0.022 312)', border:'oklch(0.86 0.045 312)' },
    };
    const m = map[lvl] || map[1];
    const heights = [7,11,15], bigH = [16,25,34];
    const bars = heights.map((h,i)=>({ h, hb:bigH[i], col: i<lvl ? m.color : 'rgba(34,32,27,0.13)' }));
    return { lvl, label:m.label, color:m.color, tint:m.tint, border:m.border, bars };
  }

  catList(){ return ['眼睛健康','心血管代謝','認知神經','關節骨骼','皮膚美容','免疫防護','消化腸道','抗氧化體能','孕產育兒']; }
  catOf(domain){
    const R=[['眼睛','眼睛健康'],['孕','孕產育兒'],['胎兒','孕產育兒'],['葉酸','孕產育兒'],['腸道','消化腸道'],['消化','消化腸道'],['飽足','消化腸道'],['過敏','免疫防護'],['呼吸道','免疫防護'],['免疫','免疫防護'],['抗發炎','免疫防護'],['關節','關節骨骼'],['疼痛','關節骨骼'],['骨','關節骨骼'],['皮膚','皮膚美容'],['美容','皮膚美容'],['毛髮','皮膚美容'],['指甲','皮膚美容'],['修復','皮膚美容'],['認知','認知神經'],['神經','認知神經'],['情緒','認知神經'],['能量','抗氧化體能'],['運動','抗氧化體能'],['肌力','抗氧化體能'],['疲勞','抗氧化體能'],['抗老','抗氧化體能'],['抗氧化','抗氧化體能'],['利用率','抗氧化體能'],['吸收','抗氧化體能'],['心血管','心血管代謝'],['血糖','心血管代謝'],['血脂','心血管代謝'],['體重','心血管代謝'],['代謝','心血管代謝']];
    for(const pair of R){ if(domain.indexOf(pair[0])>=0) return pair[1]; }
    return null;
  }
  catsFor(c){ const s=[]; (c.domains||[]).forEach(d=>{ const k=this.catOf(d); if(k&&s.indexOf(k)<0) s.push(k); }); return s; }
  ytThumb(link){ if(!link) return ''; const m=String(link).match(/(?:v=|youtu\.be\/|embed\/)([A-Za-z0-9_-]{11})/); return m ? ('https://img.youtube.com/vi/'+m[1]+'/hqdefault.jpg') : ''; }

  renderVals(){
    const v = this.state.view;
    const open = (id)=>{
      const c = DATA[id]; if(!c) return;
      this.setState({ view:'ingredient', currentId:id, openDomain:null, mechOpen:false });
      if(typeof window!=='undefined') window.scrollTo(0,0);
    };
    const openCombo = (id)=>{
      this.setState({ view:'combo', currentComboId:id });
      if(typeof window!=='undefined') window.scrollTo(0,0);
    };
    const nav = { goHome:()=>this.go('home'), goBadges:()=>this.go('badges'), goCombo:()=>this.go('combos'), goLutein:()=>open('floraglo') };

    const list = Object.values(DATA);
    const active = this.state.filter;
    const present = this.catList().filter(cat => list.some(c=>this.catsFor(c).indexOf(cat)>=0));
    const filterNames = ['全部'].concat(present);
    const filters = filterNames.map(n=>({
      name:n, onClick:()=>this.setState({ filter:n }),
      bg: n===active?'#234139':'transparent',
      color: n===active?'#F3EFE6':'#55514A',
      border: n===active?'#234139':'#C9C1AE',
    }));
    const cards = list
      .filter(c=> active==='全部' || this.catsFor(c).indexOf(active)>=0)
      .sort((a,b)=> (b.lvl||0)-(a.lvl||0) || a.name.localeCompare(b.name))
      .map(c=>({ name:c.name, brand:c.brand, oneLine:c.oneLine, chips:this.catsFor(c).slice(0,3), badge:this.badge(c.lvl), onClick:()=>open(c.id) }));

    const base = {
      ...nav,
      isHome: v==='home', isIngredient: v==='ingredient', isCombos: v==='combos', isCombo: v==='combo', isBadges: v==='badges',
      filters, cards,
      curName:'', curBrand:'', curDesc:'',
      heroDomains:[], heroGroups:[],
      mechImage:'', mechCaption:'', mechSummary:'', mechDetail:'', mechPoints:[],
      specs:[], evidence:[], claims:[], safety:[], videos:[], combos:[],
      comboCards:[], comboTitle:'', comboDesc:'', comboMembers:[], comboSynergy:[], comboEvidence:[], comboRisks:[],
      mechOpen:this.state.mechOpen,
      toggleMech:()=>this.setState({ mechOpen:!this.state.mechOpen }),
      mechBtnLabel:this.state.mechOpen?'收合完整機制敘述':'展開完整機制敘述',
      mechArrow:this.state.mechOpen?'▲':'▼',
      levels:[
        { ...this.badge(3), en:'Well-established', note:'　多層級證據一致，含人體 RCT／meta-analysis。' },
        { ...this.badge(2), en:'Developing', note:'　已有人體研究，累積中或部分不一致。' },
        { ...this.badge(1), en:'Mechanistic', note:'　以機轉、細胞、生標證據為主，人體證據初步。' },
      ],
    };

    const cur = this.state.currentId ? DATA[this.state.currentId] : null;
    if(cur){
      const openId = this.state.openDomain;
      base.curName = cur.name; base.curBrand = cur.brand; base.curDesc = cur.desc;
      base.heroDomains = cur.domains||[]; base.heroGroups = cur.groups||[];
      const m = cur.mech||{};
      base.mechImage = m.image||''; base.mechCaption = m.caption||''; base.mechSummary = m.summary||''; base.mechDetail = m.detail||'';
      base.mechPoints = (m.points||[]).map((t,i)=>({ n:String(i+1).padStart(2,'0'), t }));
      base.specs = cur.specs||[];
      base.evidence = (cur.evidence||[]).map(e=>{
        const has = e.studies && e.studies.length>0;
        const isopen = has && openId===e.id;
        return { ...e, badge:this.badge(e.lvl), open:isopen,
          onClick: has ? ()=>this.setState({ openDomain: isopen?null:e.id }) : ()=>{},
          expandLabel: has ? (isopen?'收合文獻':'展開研究文獻') : '文獻整理中',
          arrow: isopen?'▲':'▼' };
      });
      base.claims = cur.claims||[]; base.safety = cur.safety||[];
      base.videos = (cur.videos||[]).map(v=>({ ...v, thumb:this.ytThumb(v.link) }));
      base.combos = COMBOS.filter(c=>c.members.some(m=>m.id===cur.id)).map(c=>({ name:c.title, desc:c.oneLine, cta:'查看搭配 →', onClick:()=>openCombo(c.id) }));
    }
    base.comboCards = COMBOS.map(c=>({ title:c.title, membersText:c.members.map(m=>m.name).join('、'), oneLine:c.oneLine, badge:this.badge(c.lvl), onClick:()=>openCombo(c.id) }));
    const cc = this.state.currentComboId ? COMBOS.find(x=>x.id===this.state.currentComboId) : null;
    if(cc){
      base.comboTitle = cc.title; base.comboDesc = cc.desc;
      base.comboMembers = cc.members.map(m=>({ name:m.name, brand:m.brand, onClick:()=>open(m.id) }));
      base.comboSynergy = cc.synergy;
      base.comboEvidence = cc.evidence.map(e=>({ ...e, badge:this.badge(e.lvl) }));
      base.comboRisks = cc.risks;
    }
    return base;
  }
}
"""

header = ("/* 原鑑 Materia — 真實資料（由 build.py 從 site/data/*.json 產生，勿手改）*/\n"
          "const DATA = ") + data_js + ";\n" + "const COMBOS = " + combos_js + ";\n"

(SITE / "app-data.js").write_text(header + COMPONENT, encoding="utf-8")
print(f"app-data.js: 已嵌入 {len(DATA)} 個原材料 -> {', '.join(DATA)}")
