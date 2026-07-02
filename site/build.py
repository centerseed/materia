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
    const domainSet = ['全部'];
    list.forEach(c=>(c.domains||[]).forEach(d=>{ if(!domainSet.includes(d)) domainSet.push(d); }));
    const filters = domainSet.map(n=>({
      name:n, onClick:()=>this.setState({ filter:n }),
      bg: n===active?'#234139':'transparent',
      color: n===active?'#F3EFE6':'#55514A',
      border: n===active?'#234139':'#C9C1AE',
    }));
    const cards = list
      .filter(c=> active==='全部' || (c.domains||[]).includes(active))
      .sort((a,b)=> (b.lvl||0)-(a.lvl||0) || a.name.localeCompare(b.name))
      .map(c=>({ name:c.name, brand:c.brand, oneLine:c.oneLine, chips:c.chips||[], badge:this.badge(c.lvl), onClick:()=>open(c.id) }));

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
      base.claims = cur.claims||[]; base.safety = cur.safety||[]; base.videos = cur.videos||[];
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
