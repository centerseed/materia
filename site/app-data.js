/*
 * 原鑑 Materia — 頁面資料與檢視邏輯
 * 直接沿用 Claude Design 專案「Materia 原鑑知識網站設計」的 renderVals() 內容。
 * ⚠️ 目前為設計稿的示意（DEMO）資料。之後接真實資料時，改成讀取
 *    materia/ingredients/{id}/{id}.json（見 materia/schema/materia.schema.json）即可，
 *    版面與 runtime 不需改動。
 */
class Component extends DCLogic {
  state = { view:'home', filter:'全部', mechOpen:false, openDomain:'amd' };

  go(v){ this.setState({ view:v }); if(typeof window!=='undefined') window.scrollTo(0,0); }

  badge(lvl){
    const map = {
      3:{ label:'證據充分', color:'oklch(0.5 0.075 155)', tint:'oklch(0.955 0.022 155)', border:'oklch(0.86 0.045 155)' },
      2:{ label:'證據發展中', color:'oklch(0.5 0.08 258)', tint:'oklch(0.955 0.022 258)', border:'oklch(0.86 0.045 258)' },
      1:{ label:'機轉／生標支持', color:'oklch(0.5 0.075 312)', tint:'oklch(0.955 0.022 312)', border:'oklch(0.86 0.045 312)' },
    };
    const m = map[lvl];
    const heights = [7,11,15];
    const bigH = [16,25,34];
    const bars = heights.map((h,i)=>({ h, hb:bigH[i], col: i<lvl ? m.color : 'rgba(34,32,27,0.13)' }));
    return { lvl, label:m.label, color:m.color, tint:m.tint, border:m.border, bars };
  }

  indexData(){
    return [
      { name:'葉黃素', brand:'Lutein · FloraGLO®', oneLine:'黃斑部色素的主要組成，吸收藍光、抗氧化，研究聚焦長期用眼與黃斑部退化。', chips:['眼睛','認知'], domains:['眼睛','認知'], lvl:3, go:'lutein' },
      { name:'蝦紅素', brand:'Astaxanthin · AstaReal®', oneLine:'強抗氧化類胡蘿蔔素，研究多探討睫狀肌調節、眼血流與運動恢復。', chips:['眼睛','抗氧化抗老'], domains:['眼睛','抗氧化抗老'], lvl:2 },
      { name:'NMN', brand:'β-Nicotinamide Mononucleotide', oneLine:'NAD⁺ 前驅物，抗老訴求以動物與機轉研究為主，人體證據仍屬初步。', chips:['抗氧化抗老','代謝'], domains:['抗氧化抗老','代謝'], lvl:1 },
      { name:'魚油 Omega-3', brand:'EPA / DHA', oneLine:'長鏈多元不飽和脂肪酸，人體證據集中於三酸甘油酯與心血管。', chips:['心血管','認知'], domains:['心血管','認知'], lvl:3 },
      { name:'薑黃素', brand:'Curcumin', oneLine:'薑黃活性成分，抗發炎機轉明確，人體證據受生體可用率限制。', chips:['關節'], domains:['關節'], lvl:2 },
      { name:'白藜蘆醇', brand:'Resveratrol', oneLine:'葡萄皮多酚，抗老訴求熱門，但人體有效劑量與生體可用率未解，證據以機轉為主。', chips:['抗氧化抗老','心血管'], domains:['抗氧化抗老','心血管'], lvl:1 },
      { name:'維生素 D3', brand:'Cholecalciferol', oneLine:'調節鈣磷代謝與免疫，缺乏者補充的骨骼與免疫證據較成熟。', chips:['骨骼免疫'], domains:['骨骼免疫'], lvl:3 },
      { name:'輔酶 Q10', brand:'Ubiquinol', oneLine:'粒線體能量代謝輔因子，研究多在心臟功能與他汀相關肌肉症狀，結果不一。', chips:['心血管'], domains:['心血管'], lvl:2 },
    ];
  }

  renderVals(){
    const v = this.state.view;
    const nav = {
      goHome: ()=>this.go('home'),
      goLutein: ()=>this.go('lutein'),
      goCombo: ()=>this.go('combo'),
      goBadges: ()=>this.go('badges'),
    };

    // 首頁篩選
    const filterNames = ['全部','眼睛','心血管','認知','骨骼免疫','關節','抗氧化抗老','代謝'];
    const active = this.state.filter;
    const filters = filterNames.map(n=>({
      name:n,
      onClick:()=>this.setState({ filter:n }),
      bg: n===active ? '#234139' : 'transparent',
      color: n===active ? '#F3EFE6' : '#55514A',
      border: n===active ? '#234139' : '#C9C1AE',
    }));
    const cards = this.indexData()
      .filter(c=> active==='全部' || c.domains.includes(active))
      .map(c=>({ ...c, badge:this.badge(c.lvl), onClick: c.go==='lutein' ? nav.goLutein : ()=>{} }));

    // 論文
    const amdStudies = [
      { title:'葉黃素/玉米黃素補充與 AMD 視覺功能的關聯（AREDS2）', stars:'★★★★★', year:'2013', journal:'JAMA · IF≈120', type:'大型 RCT', n:'4,203', subjects:'中晚期 AMD 高風險患者', key:'補充組進展至晚期 AMD 的風險較安慰劑降低約 10%（次族群，尤其飲食葉黃素攝取低者）。', caveat:'主要分析未達顯著，益處來自次族群與交互作用分析；以葉黃素替代 β-胡蘿蔔素後才觀察到。', coi:'NEI 主導；部分作者接受營養品廠商資助。' },
      { title:'健康成人補充葉黃素對黃斑部色素密度（MPOD）的影響', stars:'★★★★', year:'2017', journal:'Am J Clin Nutr · IF≈7', type:'隨機雙盲對照', n:'120', subjects:'健康成人', key:'10 mg/日 FloraGLO® 補充 6 個月，MPOD 顯著上升（約 +0.09 光密度單位），血清葉黃素上升 2–3 倍。', caveat:'終點為生物標記（MPOD），非直接視覺結果；受試者以年輕健康者為主。', coi:'原料供應商提供試驗品，獨立學術單位執行。' },
    ];
    const fatigueStudies = [
      { title:'葉黃素/玉米黃素與螢幕使用者視覺疲勞的隨機對照試驗', stars:'★★★', year:'2020', journal:'Nutrients · IF≈5.9', type:'小型 RCT', n:'48', subjects:'每日螢幕使用 > 6 小時的健康成人', key:'12 週補充後，對比敏感度與主觀視覺疲勞評分改善，光壓力恢復時間縮短。', caveat:'樣本小、以主觀指標為主、追蹤期短；效應量中等，仍需大型試驗確認。', coi:'廠商贊助試驗品；作者申報無其他利益衝突。' },
    ];

    const rawEvidence = [
      { id:'mpod', domain:'黃斑部色素密度（MPOD）', lvl:3, oneLine:'補充後黃斑部色素密度上升，是最一致、可測量的生理反應。', subjects:'健康成人 + AMD 高風險族群', papers:'約 40+ 篇', compliance:'多項人體研究顯示補充後 MPOD 上升；MPOD 為生理指標，不等同視力改善。', studies:fatigueStudies.slice(0,0).concat([amdStudies[1]]) },
      { id:'amd', domain:'年齡相關黃斑部退化（AMD）進程', lvl:2, oneLine:'對已患病高風險族群的疾病進展，有大型試驗支持。', subjects:'中晚期 AMD 患者', papers:'約 15 篇', compliance:'AREDS2 顯示對特定亞群有幫助，整體族群結果不一；屬患者研究。', studies:amdStudies },
      { id:'fatigue', domain:'視覺疲勞 / 藍光不適（3C 族）', lvl:2, oneLine:'長時間螢幕使用者的主觀疲勞與對比敏感度有初步改善。', subjects:'健康長時間螢幕使用者', papers:'約 10 篇', compliance:'小型人體研究顯示對比敏感度、光壓力恢復與主觀疲勞改善。', studies:fatigueStudies },
      { id:'cognition', domain:'認知功能', lvl:1, oneLine:'腦中亦有葉黃素堆積，與認知的關聯以機轉與觀察性研究為主。', subjects:'健康中老年', papers:'約 8 篇', compliance:'觀察性與初步 RCT 提示關聯；機轉為腦部葉黃素堆積，人體證據初步。', studies:[] },
      { id:'skin', domain:'皮膚光防護', lvl:1, oneLine:'抗氧化與抗藍光機轉支持，人體證據仍屬早期小樣本。', subjects:'健康成人小樣本', papers:'約 5 篇', compliance:'初步研究與機轉支持抗氧化與抗藍光防護，證據處早期階段。', studies:[] },
    ];
    const openId = this.state.openDomain;
    const evidence = rawEvidence.map(e=>{
      const hasStudies = e.studies.length>0;
      const open = hasStudies && openId===e.id;
      return {
        ...e,
        badge:this.badge(e.lvl),
        open,
        onClick: hasStudies ? ()=>this.setState({ openDomain: open?null:e.id }) : ()=>{},
        expandLabel: hasStudies ? (open?'收合文獻':'展開研究文獻') : '文獻整理中',
        arrow: open?'▲':'▼',
      };
    });

    const claims = [
      { claim:'「吃葉黃素改善視力、看東西更清楚。」', evidence:'主要證據是提升黃斑部色素密度與抗氧化保護；對「已受損視力的恢復」證據有限。對比敏感度等改善多來自健康或用眼疲勞者。', who:'多為健康人／用眼疲勞者研究，非視力矯正臨床。' },
      { claim:'「預防白內障、預防黃斑部病變。」', evidence:'AREDS2 顯示有幫助的是已患病的高風險族群之「疾病進展」；「讓健康人不發病」的預防證據不足。', who:'患者族群 RCT，不等於健康人的預防效果。' },
      { claim:'「一天一顆就夠，多吃更有效、更快有感。」', evidence:'MPOD 提升有劑量關係但會飽和；多數研究劑量 10–20 mg/日，需 3–6 個月才見變化，超量無額外益處證據。', who:'效果需數月累積，非即時；高劑量缺乏加成證據。' },
    ];

    const safety = [
      { tag:'劑量', title:'建議攝取量與上限', items:['常見研究劑量 10–20 mg／日，多與玉米黃素以 5:1~2:1 複方。','目前無正式安全上限（UL）；長期高劑量（>20 mg）缺乏額外益處證據。'] },
      { tag:'吸收與交互作用', title:'交互作用', items:['脂溶性，建議隨含油脂餐食用以利吸收。','高劑量 β-胡蘿蔔素等類胡蘿蔔素會競爭吸收。','與 orlistat、膽酸結合劑等影響脂肪吸收的藥物併用可能降低吸收。'] },
      { tag:'族群', title:'需謹慎的族群', items:['孕期、哺乳期高劑量補充證據不足，建議先諮詢。','吸菸者應避免同時補充高劑量 β-胡蘿蔔素（與肺癌風險相關，非葉黃素本身）。'] },
      { tag:'觀念', title:'常見誤解', items:['「吃越多越好」— MPOD 提升會飽和。','「立刻有感」— 需數月累積。','「能取代防曬與健康飲食」— 為輔助非替代。'] },
    ];

    const videos = [
      { name:'林彥文', title:'眼科專科醫師', summary:'拆解葉黃素在黃斑部的角色，以及「護眼」宣稱與實證之間的落差。' },
      { name:'陳思穎', title:'營養學博士', summary:'從 AREDS2 談葉黃素對誰有幫助、劑量與吸收的關鍵要點。' },
      { name:'王柏森', title:'家醫科醫師', summary:'保健食品該怎麼看證據等級，別被行銷話術帶著走。' },
    ];

    const combos = [
      { name:'葉黃素 + 玉米黃素', desc:'經典黃斑部色素複方，兩者比例與共同堆積是多數護眼配方的基礎。', cta:'查看搭配 →', onClick:nav.goCombo },
      { name:'葉黃素 + 蝦紅素', desc:'脂溶性抗氧化劑組合，作用位置與機轉互補的護眼搭配。', cta:'查看搭配 →', onClick:nav.goCombo },
      { name:'葉黃素 + Omega-3 DHA', desc:'DHA 為視網膜結構脂質，與色素抗氧化理論上互補。', cta:'查看搭配 →', onClick:nav.goCombo },
    ];

    // 搭配頁
    const members = [
      { name:'葉黃素', brand:'FloraGLO®', cta:'← 回原材料頁', onClick:nav.goLutein },
      { name:'蝦紅素', brand:'AstaReal®', cta:'頁面建置中', onClick:()=>{} },
    ];
    const synergy = [
      { h:'作用位置互補', p:'葉黃素堆積於黃斑部色素層，作為濾光與抗氧化；蝦紅素能通過血視網膜屏障，研究多探討睫狀肌調節與眼血流。' },
      { h:'機轉互補', p:'兩者皆為脂溶性抗氧化劑但結構不同，理論上可覆蓋不同的氧化壓力來源與眼部區位。' },
      { h:'證據現況', p:'各自單方的人體研究較多；直接比較「複方 vs 單方」的協同試驗仍在累積，現階段以機轉推論為主。' },
    ];
    const comboEvidence = [
      { domain:'眼睛疲勞 / 調節力', lvl:2, oneLine:'健康螢幕使用者的調節反應與主觀疲勞有初步人體研究。', subjects:'健康螢幕使用者', papers:'約 8 篇' },
      { domain:'抗氧化 / 氧化壓力標記', lvl:1, oneLine:'以生物標記與機轉證據為主，人體協同數據初步。', subjects:'健康成人', papers:'約 6 篇' },
    ].map(e=>({ ...e, badge:this.badge(e.lvl) }));
    const comboRisks = [
      '兩者皆為脂溶性類胡蘿蔔素，總類胡蘿蔔素高劑量時可能互相競爭吸收。',
      '蝦紅素可能有輕微降血壓作用，與降壓藥併用者宜留意。',
      '「複方協同」的長期人體證據有限，勿以單方研究直接推論複方效果。',
    ];

    // 徽章 showcase
    const levels = [
      { ...this.badge(3), en:'Well-established', note:'　多層級證據一致，含人體 RCT／meta-analysis。' },
      { ...this.badge(2), en:'Developing', note:'　已有人體研究，累積中或部分不一致。' },
      { ...this.badge(1), en:'Mechanistic', note:'　以機轉、細胞、生標證據為主，人體證據初步。' },
    ];

    return {
      ...nav,
      isHome: v==='home', isLutein: v==='lutein', isCombo: v==='combo', isBadges: v==='badges',
      filters, cards,
      heroDomains:['眼睛健康','黃斑部','認知（初步）','皮膚（初步）'],
      heroGroups:['3C 重度使用者','銀髮族','長時間戶外者','一般成人保養'],
      specs:[
        { k:'專利 / 商標', v:'FloraGLO® — Kemin Industries' },
        { k:'形式', v:'游離型葉黃素（free lutein）' },
        { k:'常見規格', v:'每份 10–20 mg，多與玉米黃素 5:1~2:1 複方' },
        { k:'主要臨床依據', v:'AREDS2 所採用之葉黃素／玉米黃素來源' },
      ],
      mechOpen:this.state.mechOpen,
      toggleMech:()=>this.setState({ mechOpen:!this.state.mechOpen }),
      mechBtnLabel:this.state.mechOpen?'收合完整機制敘述':'展開完整機制敘述',
      mechArrow:this.state.mechOpen?'▲':'▼',
      evidence, claims, safety, videos, combos,
      members, synergy, comboEvidence, comboRisks,
      levels,
    };
  }
}
