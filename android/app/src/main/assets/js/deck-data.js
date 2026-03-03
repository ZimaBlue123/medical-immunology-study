// 医学免疫学题库
// 自动生成，请勿手动修改

const DECK_DATA = {
  "meta": {
    "title": "医学免疫学核心自测题库（示例）",
    "source": "参考《医学免疫学》（人卫第9版）框架，自写题目与解析（不含教材原文）",
    "version": 1
  },
  "cards": [
    {
      "id": "core-0001",
      "type": "mcq",
      "stem": "下列哪一项最符合“固有免疫（innate immunity）”的特点？",
      "choices": [
        "反应速度较慢，但具有高度特异性与免疫记忆",
        "主要依赖 TCR/BCR 识别抗原决定簇",
        "对模式分子进行识别，反应快速，个体间差异相对较小",
        "需要抗原呈递细胞提供 MHC-肽复合物后才能启动"
      ],
      "answer_index": 2,
      "explain": "固有免疫以模式识别受体（PRR）识别 PAMP/DAMP 为核心，启动快、特异性低但稳定；适应性免疫才强调高度特异性与记忆。",
      "tags": [
        "module01",
        "innate"
      ]
    },
    {
      "id": "core-0002",
      "type": "short",
      "prompt": "用一句话解释：PAMP 和 DAMP 分别指什么？",
      "answer": "PAMP 是病原体相关分子模式；DAMP 是损伤相关分子模式。",
      "explain": "记忆抓手：P=pathogen（病原体），D=damage（损伤）。",
      "tags": [
        "module02",
        "innate"
      ]
    },
    {
      "id": "core-0003",
      "type": "mcq",
      "stem": "以下哪一种细胞更典型地参与“早期抗病毒”反应，并能产生大量 I 型干扰素？",
      "choices": [
        "中性粒细胞",
        "浆细胞样树突状细胞（pDC）",
        "肥大细胞",
        "嗜酸性粒细胞"
      ],
      "answer_index": 1,
      "explain": "pDC 是 I 型干扰素的重要来源之一，常被用来考“抗病毒早期先天反应”。",
      "tags": [
        "module02",
        "innate",
        "cytokine"
      ]
    },
    {
      "id": "core-0004",
      "type": "mcq",
      "stem": "补体经典途径最直接的“启动信号”通常是：",
      "choices": [
        "病原体表面甘露糖与凝集素结合",
        "抗体与抗原形成复合物并暴露 Fc",
        "自发水解形成 C3(H2O)",
        "细菌脂多糖直接裂解 C5"
      ],
      "answer_index": 1,
      "explain": "经典途径与“抗体介导”强绑定；凝集素途径靠 MBL/ficolin 等识别糖基；旁路途径靠 C3 自发水解与放大回路。",
      "tags": [
        "module03",
        "complement"
      ]
    },
    {
      "id": "core-0005",
      "type": "mcq",
      "stem": "下列哪一项最符合补体 C3b 的主要功能？",
      "choices": [
        "趋化中性粒细胞",
        "促进调理吞噬",
        "形成膜攻击复合体（MAC）",
        "直接诱导肥大细胞脱颗粒"
      ],
      "answer_index": 1,
      "explain": "记忆法：C3b = 'b' for binding（黏住）→调理；C5a 更强趋化；MAC 主要由 C5b-9 组成。",
      "tags": [
        "module03",
        "complement"
      ]
    },
    {
      "id": "core-0006",
      "type": "short",
      "prompt": "用一句话写出补体的“三大效应”（不要求严格顺序）。",
      "answer": "调理吞噬、炎症/趋化、溶解（MAC）。",
      "tags": [
        "module03",
        "complement"
      ]
    },
    {
      "id": "core-0007",
      "type": "mcq",
      "stem": "关于 MHC I 的“典型呈递对象”，下列哪项正确？",
      "choices": [
        "主要呈递外源性抗原肽给 CD4+ T 细胞",
        "主要呈递内源性抗原肽给 CD8+ T 细胞",
        "只在抗原提呈细胞上表达",
        "只在红细胞上表达"
      ],
      "answer_index": 1,
      "explain": "MHC I：几乎所有有核细胞表达，偏向内源性（细胞内）抗原→CD8+；MHC II：专业 APC 表达，偏向外源性抗原→CD4+。",
      "tags": [
        "module04",
        "mhc"
      ]
    },
    {
      "id": "core-0008",
      "type": "mcq",
      "stem": "“交叉呈递（cross-presentation）”这件事最常用于解释：",
      "choices": [
        "为何外源性抗原也能诱导 CD8+ T 细胞应答",
        "为何 IgE 介导速发型超敏反应",
        "为何补体旁路途径无需抗体",
        "为何中性粒细胞会吞噬细菌"
      ],
      "answer_index": 0,
      "explain": "交叉呈递的核心：外源性抗原被某些 APC（常见树突状细胞）“借道”进入 MHC I 呈递通路，从而激活 CD8+。",
      "tags": [
        "module04",
        "mhc",
        "tcell"
      ]
    },
    {
      "id": "core-0009",
      "type": "mcq",
      "stem": "下列哪个免疫球蛋白类别更典型地与“黏膜免疫”相关？",
      "choices": [
        "IgG",
        "IgA",
        "IgM",
        "IgE"
      ],
      "answer_index": 1,
      "explain": "IgA 在分泌型（sIgA）形态下常见于呼吸道/消化道等黏膜表面，强调“阻断黏附与入侵”。",
      "tags": [
        "module05",
        "antibody"
      ]
    },
    {
      "id": "core-0010",
      "type": "mcq",
      "stem": "初次体液免疫应答中，较早出现、常以五聚体形式存在的是：",
      "choices": [
        "IgG",
        "IgA",
        "IgM",
        "IgE"
      ],
      "answer_index": 2,
      "explain": "IgM 常作为“首发抗体”，亲和力未必最高但多价结合、凝集能力强；随后类别转换可出现 IgG/IgA/IgE 等。",
      "tags": [
        "module05",
        "antibody",
        "bcell"
      ]
    },
    {
      "id": "core-0011",
      "type": "short",
      "prompt": "用一句话区分“亲和力成熟（affinity maturation）”与“类别转换（class switch）”。",
      "answer": "亲和力成熟是同一类别内抗体与抗原结合力提升；类别转换是在不改变特异性的前提下更换重链类别以改变效应功能。",
      "tags": [
        "module07",
        "bcell"
      ]
    },
    {
      "id": "core-0012",
      "type": "mcq",
      "stem": "T 细胞活化的“第二信号”最经典的例子是：",
      "choices": [
        "TCR 识别 MHC-肽",
        "CD28 与 B7（CD80/86）结合",
        "IL-2 自分泌增殖",
        "抗体与 Fc 受体结合"
      ],
      "answer_index": 1,
      "explain": "第一信号决定“识别”，第二信号决定“允许激活”；没有第二信号更容易进入无反应（anergy）等耐受状态。",
      "tags": [
        "module06",
        "tcell"
      ]
    },
    {
      "id": "core-0013",
      "type": "mcq",
      "stem": "下列哪一项更符合“超敏反应 I 型（速发型）”的机制核心？",
      "choices": [
        "IgE + 肥大细胞/嗜碱性粒细胞",
        "IgG/IgM + 补体介导细胞溶解",
        "免疫复合物沉积引起炎症",
        "T 细胞介导的迟发反应"
      ],
      "answer_index": 0,
      "explain": "I 型：IgE 致敏后再次暴露引发脱颗粒与介质释放；II/III/IV 分别对应细胞毒、免疫复合物、T 细胞迟发。",
      "tags": [
        "module09",
        "hypersensitivity"
      ]
    },
    {
      "id": "core-0014",
      "type": "mcq",
      "stem": "“迟发型超敏反应（IV 型）”更典型的主导者是：",
      "choices": [
        "IgE",
        "补体 MAC",
        "免疫复合物",
        "T 细胞与巨噬细胞轴"
      ],
      "answer_index": 3,
      "explain": "IV 型强调细胞免疫：Th1/Th17 等与巨噬细胞/炎症反应相关，起效更慢（常以小时到天计）。",
      "tags": [
        "module09",
        "hypersensitivity",
        "tcell"
      ]
    },
    {
      "id": "core-0015",
      "type": "short",
      "prompt": "什么叫“免疫耐受（tolerance）”？用一句话说明。",
      "answer": "免疫耐受是免疫系统对自身抗原或特定抗原不发生有害应答的状态。",
      "tags": [
        "module10",
        "tolerance"
      ]
    },
    {
      "id": "core-0016",
      "type": "mcq",
      "stem": "下列哪项更符合“中枢耐受”而非“外周耐受”？",
      "choices": [
        "调节性 T 细胞抑制",
        "无共刺激导致无反应",
        "胸腺/骨髓内的负选择",
        "免疫检查点抑制信号"
      ],
      "answer_index": 2,
      "explain": "中枢耐受发生在淋巴细胞发育阶段（胸腺/骨髓），外周耐受发生在外周组织与二级淋巴器官环境中。",
      "tags": [
        "module10",
        "tolerance"
      ]
    },
    {
      "id": "core-0017",
      "type": "mcq",
      "stem": "关于“疫苗诱导保护”的最核心逻辑是：",
      "choices": [
        "只要诱导强烈炎症就一定有效",
        "通过先建立免疫记忆，使再次暴露时更快更强应答",
        "通过抑制固有免疫来避免组织损伤",
        "通过让补体持续激活来杀死所有病原体"
      ],
      "answer_index": 1,
      "explain": "疫苗的“价值点”在于记忆：再次遇到相同/相似抗原时，反应更快、更有效，临床上就体现为更轻或不发病。",
      "tags": [
        "module12",
        "vaccine"
      ]
    },
    {
      "id": "core-0018",
      "type": "mcq",
      "stem": "移植排斥反应中，“急性排斥”更典型地与哪类免疫机制相关？",
      "choices": [
        "预存抗体引起立即血管损伤",
        "T 细胞介导的应答为主",
        "完全与免疫无关",
        "仅与补体旁路途径相关"
      ],
      "answer_index": 1,
      "explain": "超急性多与预存抗体相关；急性常强调 T 细胞介导（也可伴体液成分）；慢性更像长期炎症与纤维化过程。",
      "tags": [
        "module12",
        "transplant",
        "tcell"
      ]
    },
    {
      "id": "core-0019",
      "type": "mcq",
      "stem": "肿瘤免疫“免疫逃逸”中，较典型的策略是：",
      "choices": [
        "增加肿瘤抗原呈递",
        "上调免疫抑制信号/微环境",
        "增强 NK 细胞活性",
        "促进树突状细胞成熟"
      ],
      "answer_index": 1,
      "explain": "肿瘤常通过抑制性通路与免疫抑制微环境降低免疫清除效率；免疫治疗常从“解除刹车”角度切入。",
      "tags": [
        "module12",
        "tumor"
      ]
    },
    {
      "id": "core-0020",
      "type": "short",
      "prompt": "用一句话解释：为什么“共刺激不足”会让 T 细胞更倾向于不应答？",
      "answer": "因为共刺激是“安全许可”，缺失时可诱导无反应/耐受以避免对无害或自身抗原误激活。",
      "tags": [
        "module06",
        "tcell",
        "tolerance"
      ]
    },
    {
      "id": "core-0021",
      "type": "mcq",
      "stem": "下列哪一项更符合“免疫缺陷 → 易感病原体类型”的典型映射？",
      "choices": [
        "补体缺陷 → 更易发生反复化脓性感染与免疫复合物相关问题",
        "B 细胞缺陷 → 更易感染所有细胞内病原体",
        "T 细胞缺陷 → 只会出现过敏，不会感染",
        "吞噬细胞缺陷 → 只会导致肿瘤，不影响感染"
      ],
      "answer_index": 0,
      "explain": "记忆抓手：缺哪一环，就缺那一类防线；体液、细胞免疫、吞噬、补体各自覆盖的病原体谱不同。",
      "tags": [
        "module11",
        "immunodeficiency"
      ]
    },
    {
      "id": "core-0022",
      "type": "mcq",
      "stem": "关于 NK 细胞识别靶细胞的典型线索，下列哪项更贴近核心？",
      "choices": [
        "识别靶细胞表面的特定抗原决定簇（像 BCR 一样）",
        "对 MHC I 表达下降等“缺失自身”信号更敏感",
        "必须先经抗原呈递细胞激活才能杀伤",
        "只在黏膜表面发挥作用"
      ],
      "answer_index": 1,
      "explain": "NK 细胞常用来理解“缺失自身（missing-self）”：当 MHC I 下降时抑制性信号减弱，杀伤倾向增强。",
      "tags": [
        "module02",
        "innate",
        "nk"
      ]
    },
    {
      "id": "core-0023",
      "type": "short",
      "prompt": "用一句话概括：抗原呈递细胞（APC）的意义是什么？",
      "answer": "APC 把抗原信息加工并呈递给 T 细胞，同时提供激活所需的共刺激与细胞因子环境来决定应答走向。",
      "tags": [
        "module04",
        "mhc",
        "tcell"
      ]
    },
    {
      "id": "core-0024",
      "type": "mcq",
      "stem": "下列哪项更像“免疫复合物（III 型超敏）”带来的病理特点？",
      "choices": [
        "IgE 交联引发即时脱颗粒",
        "自身抗体直接攻击细胞表面抗原导致溶解",
        "可溶性抗原-抗体复合物沉积在组织，引发补体与炎症",
        "T 细胞迟发反应导致局部硬结"
      ],
      "answer_index": 2,
      "explain": "III 型关键词：可溶性复合物 + 沉积 + 补体/炎症；常考“沉积部位”和“为何会沉积”。",
      "tags": [
        "module09",
        "hypersensitivity",
        "complement"
      ]
    },
    {
      "id": "core-0025",
      "type": "mcq",
      "stem": "以下哪项最符合“抗体的特异性（specificity）”含义？",
      "choices": [
        "能否激活补体",
        "能否结合某一特定抗原表位",
        "能否形成五聚体",
        "是否存在于黏膜分泌液"
      ],
      "answer_index": 1,
      "explain": "特异性回答的是“认得谁”；效应功能回答的是“结合后能做什么”（补体、调理、ADCC 等）。",
      "tags": [
        "module05",
        "antibody"
      ]
    }
  ]
};


function getDeckCards() {
    return DECK_DATA.cards || [];
}

function getCardById(cardId) {
    return DECK_DATA.cards.find(c => c.id === cardId) || null;
}

function filterCardsByTags(cards, tags) {
    if (!tags || tags.length === 0) return cards;
    return cards.filter(card => {
        const cardTags = card.tags || [];
        return tags.some(tag => cardTags.includes(tag));
    });
}
