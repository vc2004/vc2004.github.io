---
layout: homepage
title: 每日卦象
---

<div class="hexagram-container">
  <div id="hexagram-content" class="hexagram-content">
    <h2 id="hexagram-title" class="hexagram-title"></h2>
    <div id="hexagram-symbol" class="hexagram-symbol"></div>
    <div id="hexagram-meaning" class="hexagram-meaning"></div>
    <div id="hexagram-description" class="hexagram-description"></div>
  </div>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
  const hexagrams = [
    {
      title: '乾卦',
      symbol: '☰',
      meaning: '乾为天',
      description: '大哉乾元，万物资始。乃统天。云行雨施，品物流形。大明终始，六位时成，时乘六龙以御天。乾道变化，各正性命。'
    },
    {
      title: '坤卦',
      symbol: '☷',
      meaning: '坤为地',
      description: '至哉坤元，万物资生。乃顺承天。坤厚载物，德合无疆。含弘光大，品物咸亨。牝马地类，行地无疆，柔顺利贞。'
    },
    {
      title: '屯卦',
      symbol: '☳☵',
      meaning: '云雷屯',
      description: '屯，元亨，利贞。勿用有攸往，利建侯。屯刚柔始交而难生，动乎险中，大亨贞。雷雨之动满盈，天造草昧。'
    },
    {
      title: '蒙卦',
      symbol: '☵☶',
      meaning: '山水蒙',
      description: '蒙，亨。匪我求童蒙，童蒙求我。初筮告，再三渎，渎则不告。利贞。蒙以养正，圣功也。'
    },
    {
      title: '需卦',
      symbol: '☰☵',
      meaning: '水天需',
      description: '需，有孚，光亨，贞吉。利涉大川。需须待也，饮食之道，有孚光亨，位乎天位，以正中也。'
    },
    {
      title: '讼卦',
      symbol: '☵☰',
      meaning: '天水讼',
      description: '讼，有孚，窒惕，中吉，终凶。利见大人，不利涉大川。讼，上刚下险，险而健讼。'
    },
    {
      title: '师卦',
      symbol: '☵☷',
      meaning: '地水师',
      description: '师，贞丈人吉，无咎。师众也，贞正也。能以众正，可以王矣。刚中而应，行险而顺，以此毒天下，而民从之。'
    },
    {
      title: '比卦',
      symbol: '☷☵',
      meaning: '水地比',
      description: '比，吉。原筮，元永贞，无咎。不宁方来，后夫凶。比，辅也，下顺从也。原筮元永贞，以应初也。'
    },
    {
      title: '小畜卦',
      symbol: '☰☴',
      meaning: '风天小畜',
      description: '小畜，亨。密云不雨，自我西郊。柔得位而上行，是以小畜。健而巽，刚中而志行，乃亨。'
    },
    {
      title: '履卦',
      symbol: '☱☰',
      meaning: '天泽履',
      description: '履，履虎尾，不咥人，亨。柔履刚也。说而应乎乾，是以履虎尾，不咥人，亨。刚中正，履帝位而不疚，光明也。'
    },
    {
      title: '泰卦',
      symbol: '☷☰',
      meaning: '地天泰',
      description: '泰，小往大来，吉亨。天地交泰，上下交泰，天地之道，大明终始。泰，通也。物不可穷，故受之以泰。'
    },
    {
      title: '否卦',
      symbol: '☰☷',
      meaning: '天地否',
      description: '否之匪人，不利君子贞，大往小来。天地不交，否。君子以俭德辟难，不可荣以禄。'
    },
    {
      title: '同人卦',
      symbol: '☰☲',
      meaning: '天火同人',
      description: '同人于野，亨。利涉大川，利君子贞。同人，同也。外比于贤，以从上也。柔得中位，故亨。'
    },
    {
      title: '大有卦',
      symbol: '☲☰',
      meaning: '火天大有',
      description: '大有，元亨。大有，柔得尊位，大中而上正，天下信之，顺而应之，大有之象也。'
    },
    {
      title: '谦卦',
      symbol: '☶☷',
      meaning: '地山谦',
      description: '谦，亨，君子有终。谦，德之柄也。内卑而外节，义以行之，以正君臣之体。'
    },
    {
      title: '豫卦',
      symbol: '☳☷',
      meaning: '地雷豫',
      description: '豫，利建侯行师。豫，刚应而志行，顺以动，豫。豫顺以动，故天地如之，而况建侯行师乎？'
    },
    {
      title: '随卦',
      symbol: '☳☱',
      meaning: '泽雷随',
      description: '随，元亨，利贞，无咎。随，刚来而下柔，动而说，随。大亨贞，无咎，而天下随时，随时之义大矣哉。'
    },
    {
      title: '蛊卦',
      symbol: '☶☴',
      meaning: '山风蛊',
      description: '蛊，元亨，利涉大川。先甲三日，后甲三日。蛊，刚上而柔下，巽而止，蛊。蛊，匪其时，有与也。'
    },
    {
      title: '临卦',
      symbol: '☷☱',
      meaning: '地泽临',
      description: '临，元亨，利贞。至于八月有凶。临，刚浸而长，说而顺，刚中而应，大亨以正，天之道也。'
    },
    {
      title: '观卦',
      symbol: '☴☷',
      meaning: '风地观',
      description: '观，盥而不荐，有孚颙若。观，盥而不荐，有孚颙若，下观而化也。观天之神道，而四时不忒，圣人以神道设教，而天下服矣。'
    },
    {
      title: '噬嗑卦',
      symbol: '☳☲',
      meaning: '火雷噬嗑',
      description: '噬嗑，亨。利用狱。噬嗑，上下颊动也。刚柔相错，上下相咬也。利用狱，以明邦也。'
    },
    {
      title: '贲卦',
      symbol: '☶☲',
      meaning: '山火贲',
      description: '贲，亨。小利有攸往。贲，亨，柔来而文刚，故亨。分，刚上而文柔，故小利有攸往。天文也，文明以止，人文也。'
    },
    {
      title: '剥卦',
      symbol: '☶☷',
      meaning: '山地剥',
      description: '剥，不利有攸往。剥，剥也，柔变刚也。不利有攸往，小人长也。顺而止之，观象也。'
    },
    {
      title: '复卦',
      symbol: '☷☳',
      meaning: '地雷复',
      description: '复，亨。出入无疾，朋来无咎。反复其道，七日来复，利有攸往。复，其见天地之心乎。'
    },
    {
      title: '无妄卦',
      symbol: '☰☳',
      meaning: '天雷无妄',
      description: '无妄，元亨，利贞。其匪正有眚，不利有攸往。无妄，刚自外来，而为主于内。动而健，刚中而应，大亨以正，天之命也。'
    },
    {
      title: '大畜卦',
      symbol: '☶☰',
      meaning: '山天大畜',
      description: '大畜，利贞，不家食吉，利涉大川。大畜，刚健笃实辉光，日新其德。刚上而尚贤。能止健，大正也。'
    },
    {
      title: '颐卦',
      symbol: '☶☳',
      meaning: '山雷颐',
      description: '颐，贞吉。观颐，自求口实。颐，养正则吉。观颐，观其所养也。自求口实，观其自养也。天地养万物，圣人养贤以及万民。'
    },
    {
      title: '大过卦',
      symbol: '☱☴',
      meaning: '泽风大过',
      description: '大过，栋桡。利有攸往，亨。大过，大者过也。栋桡，本末弱也。刚过而中，巽而说行，利有攸往，乃亨。'
    },
    {
      title: '坎卦',
      symbol: '☵☵',
      meaning: '坎为水',
      description: '坎，习坎，有孚，维心亨，行有尚。习坎，重险也。水流而不盈，行险而不失其信。维心亨，乃以刚中也。'
    },
    {
      title: '离卦',
      symbol: '☲☲',
      meaning: '离为火',
      description: '离，利贞，亨。畜牝牛，吉。离，丽也。日月丽乎天，百谷草木丽乎土，重明以丽乎正，乃化成天下。'
    },
    {
      title: '咸卦',
      symbol: '☱☶',
      meaning: '泽山咸',
      description: '咸，亨，利贞，取女吉。咸，感也。柔上而刚下，二气感应以相与，止而说，男下女，是以亨利贞，取女吉也。'
    },
    {
      title: '恒卦',
      symbol: '☳☴',
      meaning: '雷风恒',
      description: '恒，亨，无咎，利贞，利有攸往。恒，久也。刚上而柔下，雷风相与，巽而动，刚柔皆应，恒。'
    },
    {
      title: '遁卦',
      symbol: '☰☶',
      meaning: '天山遁',
      description: '遁，亨。小利贞。遁，退也。刚当位而应，与时行也。小利贞，浸而长也。遁之时义大矣哉。'
    },
    {
      title: '大壮卦',
      symbol: '☳☰',
      meaning: '雷天大壮',
      description: '大壮，利贞。大壮，大者壮也。刚以动，故壮。大壮利贞，大者正也。正大而天地之情可见矣。'
    },
    {
      title: '晋卦',
      symbol: '☲☷',
      meaning: '火地晋',
      description: '晋，康侯用锡马蕃庶，昼日三接。晋，进也。明出地上，顺而丽乎大明，柔进而上行。是以康侯用锡马蕃庶，昼日三接也。'
    },
    {
      title: '明夷卦',
      symbol: '☷☲',
      meaning: '地火明夷',
      description: '明夷，利艰贞。明入地中，明夷。内文明而外柔顺，以蒙大难，文王以之。利艰贞，晦其明也，内难而能正其志也。'
    },
    {
      title: '家人卦',
      symbol: '☴☲',
      meaning: '风火家人',
      description: '家人，利女贞。家人，女正位乎内，男正位乎外，男女正，天地之大义也。家人有严君焉，父母之谓也。'
    },
    {
      title: '睽卦',
      symbol: '☲☱',
      meaning: '火泽睽',
      description: '睽，小事吉。睽，火动而上，泽动而下；二女同居，其志不同行；说而丽乎明，柔进而上行。是以小事吉也。'
    },
    {
      title: '蹇卦',
      symbol: '☶☵',
      meaning: '山水蹇',
      description: '蹇，利西南，不利东北；利见大人，贞吉。蹇，难也，险在前也。见险而能止，知矣哉。'
    },
    {
      title: '解卦',
      symbol: '☳☵',
      meaning: '雷水解',
      description: '解，利西南，无所往，其来复吉。有攸往，夙吉。解，险以动，动而免乎险，解。解利西南，往得众也。其来复吉，乃得中也。'
    },
    {
      title: '损卦',
      symbol: '☶☱',
      meaning: '山泽损',
      description: '损，有孚，元吉，无咎，可贞，利有攸往。曷之用？二簋可用享。损，损下益上，其道上行。损而有孚，元吉，无咎，可贞，利有攸往。'
    },
    {
      title: '益卦',
      symbol: '☴☳',
      meaning: '风雷益',
      description: '益，利有攸往，利涉大川。益，损上益下，民说无疆。自上下下，其道大光。利有攸往，中正有庆。利涉大川，木道乃行。'
    },
    {
      title: '夬卦',
      symbol: '☱☰',
      meaning: '泽天夬',
      description: '夬，扬于王庭，孚号，有厉，告自邑，不利即戎，利有攸往。夬，决也，刚决柔也。健而说，决而和，扬于王庭，柔乘五刚也。'
    },
    {
      title: '姤卦',
      symbol: '☰☴',
      meaning: '天风姤',
      description: '姤，女壮，勿用取女。姤，遇也，柔遇刚也。勿用取女，不可与长也。天地相遇，品物咸章也。刚遇中正，天下大行也。'
    },
    {
      title: '萃卦',
      symbol: '☱☷',
      meaning: '泽地萃',
      description: '萃，亨。王假有庙，利见大人，亨，利贞。用大牲吉，利有攸往。萃，聚也。顺以说，刚中而应，故聚也。王假有庙，致孝享也。'
    },
    {
      title: '升卦',
      symbol: '☷☴',
      meaning: '地风升',
      description: '升，元亨，用见大人，勿恤，南征吉。升，柔以顺，刚中而应，是以大亨。用见大人，勿恤，有庆也。南征吉，志行也。'
    },
    {
      title: '困卦',
      symbol: '☱☵',
      meaning: '泽水困',
      description: '困，亨，贞，大人吉，无咎，有言不信。困，刚掩也。险以说，困而不失其所，亨，其唯君子乎。贞，大人吉，以刚中也。'
    },
    {
      title: '井卦',
      symbol: '☵☴',
      meaning: '水风井',
      description: '井，改邑不改井，无丧无得，往来井井。汔至，亦未繘井，羸其瓶，凶。井，养而不穷也。改邑不改井，乃以刚中也。'
    },
    {
      title: '革卦',
      symbol: '☱☲',
      meaning: '泽火革',
      description: '革，己日乃孚，元亨，利贞，悔亡。革，水火相息，二女同居，其志不相得，曰革。己日乃孚，革而信之。'
    },
    {
      title: '鼎卦',
      symbol: '☲☴',
      meaning: '火风鼎',
      description: '鼎，元吉，亨。鼎，象也。以木巽火，亨饪也。圣人亨以享上帝，而大亨以养圣贤。巽而耳目聪明，柔进而上行，得中而应乎刚，是以元亨。'
    },
    {
      title: '震卦',
      symbol: '☳☳',
      meaning: '震为雷',
      description: '震，亨。震来虩虩，笑言哑哑。震惊百里，不丧匕鬯。震，亨。震来虩虩，恐致福也。笑言哑哑，后有则也。'
    },
    {
      title: '艮卦',
      symbol: '☶☶',
      meaning: '艮为山',
      description: '艮，艮其背，不获其身，行其庭，不见其人，无咎。艮，止也。时止则止，时行则行，动静不失其时，其道光明。'
    },
    {
      title: '渐卦',
      symbol: '☴☶',
      meaning: '风山渐',
      description: '渐，女归吉，利贞。渐之进也，女归吉也。进得位，往有功也。进以正，可以正邦也。其位刚，得中也。止而巽，动不穷也。'
    },
    {
      title: '归妹卦',
      symbol: '☳☱',
      meaning: '雷泽归妹',
      description: '归妹，征凶，无攸利。归妹，天地之大义也。天地不交，而万物不兴，归妹，人之终始也。说以动，所归妹也。'
    },
    {
      title: '丰卦',
      symbol: '☳☲',
      meaning: '雷火丰',
      description: '丰，亨。王假之，勿忧，宜日中。丰，大也。明以动，故丰。王假之，尚大也。勿忧宜日中，宜照天下也。日中则昃，月盈则食，天地盈虚，与时消息。'
    },
    {
      title: '旅卦',
      symbol: '☶☲',
      meaning: '火山旅',
      description: '旅，小亨，旅贞吉。旅，柔进而下行，得中乎外，而顺乎刚，止而丽乎明，是以小亨，旅贞吉也。旅之时义大矣哉。'
    },
    {
      title: '巽卦',
      symbol: '☴☴',
      meaning: '巽为风',
      description: '巽，小亨，利有攸往，利见大人。巽，入也。巽，巽，以从风也。君子以申命行事。巽而顺，志行得也。'
    },
    {
      title: '兑卦',
      symbol: '☱☱',
      meaning: '兑为泽',
      description: '兑，亨，利贞。兑，说也。刚中而柔外，说以利贞，是以顺乎天，而应乎人。说以先民，民忘其劳；说以犯难，民忘其死。'
    },
    {
      title: '涣卦',
      symbol: '☴☵',
      meaning: '风水涣',
      description: '涣，亨。王假有庙，利涉大川，利贞。涣，亨。刚来而不穷，柔得位乎外而上同。王假有庙，王乃在中也。利涉大川，乘木有功也。'
    },
    {
      title: '节卦',
      symbol: '☵☱',
      meaning: '水泽节',
      description: '节，亨。苦节不可贞。节，节也。刚柔分，而刚得中。节以制度，不伤财，不害民。苦节不可贞，其道穷也。'
    },
    {
      title: '中孚卦',
      symbol: '☴☱',
      meaning: '风泽中孚',
      description: '中孚，豚鱼吉，利涉大川，利贞。中孚，柔在内而刚得中。说而巽，孚乃化邦也。豚鱼吉，信及豚鱼也。利涉大川，乘木舟虚也。'
    },
    {
      title: '小过卦',
      symbol: '☳☶',
      meaning: '雷山小过',
      description: '小过，亨，利贞，可小事，不可大事。飞鸟遗之音，不宜上，宜下，大吉。小过，小者过而亨也。过以利贞，与时行也。'
    },
    {
      title: '既济卦',
      symbol: '☵☲',
      meaning: '水火既济',
      description: '既济，亨，小利贞，初吉终乱。既济，亨，小者亨也。利贞，刚柔正而位当也。初吉，柔得中也。终乱，其道穷也。'
    },
    {
      title: '未济卦',
      symbol: '☲☵',
      meaning: '火水未济',
      description: '未济，亨，小狐汔济，濡其尾，无攸利。未济，亨，柔得中也。小狐汔济，未出中也。濡其尾，无攸利，不续终也。虽不当位，刚柔应也。'
    }
  ];

  function getDateString() {
    const now = new Date();
    return `${now.getFullYear()}-${now.getMonth() + 1}-${now.getDate()}`;
  }

  function hashCode(str) {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      const char = str.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash;
    }
    return Math.abs(hash);
  }

  function displayDailyHexagram() {
    const dateStr = getDateString();
    const hash = hashCode(dateStr);
    const index = hash % hexagrams.length;
    const hexagram = hexagrams[index];
    
    document.getElementById('hexagram-title').textContent = hexagram.title;
    document.getElementById('hexagram-symbol').textContent = hexagram.symbol;
    document.getElementById('hexagram-meaning').textContent = hexagram.meaning;
    document.getElementById('hexagram-description').textContent = hexagram.description;
  }

  displayDailyHexagram();
});
</script> 