# 金标准标注说明

2026年10月22日整理，合并了此前讨论中补充的全部规则。

## 一、基本要求

1. 标注时不看任何模型输出，也不用任何大模型（Claude、ChatGPT 等）辅助。
2. 意大利文可以用普通翻译软件、标注表中的“参照词表_Mazzi”和 Florio 1611 意英词典（LEME 在线本）对照阅读。用了哪个翻译软件，写在 notes 里。
3. 填写的是原文写法，不是译文。照抄原文，不翻译，不改错字，不改繁简。OCR 错字也照抄，正确拼法写在 notes 里。
4. 一个服饰词填一行。140条记录每条都要有记录，没有服饰词的条目填一行，surface 留空，notes 写“无”。

## 二、各栏填法

| 栏目 | 填什么 |
|---|---|
| record_id | 记录编号，从“记录”页抄 |
| surface | 原文中的写法 |
| category | 类别，见第三节 |
| wearer | 穿戴者，见第四节 |
| renamed | 文中说明此物另有名称、俗称，填1，否则填0 |
| negated | 允许、禁止或限额，见第五节 |
| combo | 组合编号，见第六节 |
| notes | 疑问、OCR 校正、适用对象、上限、所用翻译软件等 |

## 三、category 类别

| 值 | 含义 | 例子 |
|---|---|---|
| garment | 衣服，以及袖、领、裙片等衣服的组成部分 | 团衫、褙子、比甲、gamurra、cioppa、maniche、gherone |
| headwear_jewelry | 头饰与首饰，以及戴在头上的巾帕 | 珠翠冠、金钗、耳环、perle、ghirlanda、velo |
| material_technique | 面料、材料与工艺，以及缝在衣服上的装饰 | 紵丝、妆花、销金、银镀金、seta、broccato、ricamo、increspato |
| color | 颜色 | 大红、鸦青、chermisi、giallo |
| pattern | 纹样 | 蟒龙、飞鱼、翟文 |
| generic | 泛称 | 衣服、首饰、服饰、vestimento、panni、ornamenti |

**附属装饰按附着位置归类。**

- 缝在衣服上的流苏、饰边、镶带、刺绣、剪花、纽扣，归 material_technique。
- 挂在冠、发、耳、颈上的流苏、珠结、步摇，归 headwear_jewelry。
- 单独系在身上的带、绦、搭膊、cintola，归 garment。它的金银珠宝材料另记一行 material_technique，两行填同一个 combo。
- 霞帔是披在肩上、垂于胸前的帛带，按单独系在身上的带类归 garment。霞帔下端的坠子是挂在衣物上的饰件，归 material_technique，其材料与工艺另记，如钑花、金。

**珍珠、金银、宝石看是不是另一件东西的材料。**

- 文中有一件具名的东西，珍珠、金银、宝石是它的材料或装饰，归 material_technique，和那件东西填同一个 combo。例如 duo trecce di perle（两条珍珠发辫）、grillanda di penne con perle（缀珍珠的羽毛花冠）、perle in fruscholi、金丝鬏髻。
- 珍珠、金银、宝石单独作为佩戴物出现，前后没有别的具名物件，归 headwear_jewelry。例如 portare perle、珠翠满头。
- 材料词加物件词，拆到每一部分都能单独成为服饰词为止，同一个 combo。例如金钗拆为金、钗，翠龙拆为翠、龙，珠翟拆为珠、翟，珠翠云拆为珠、翠、云（珍珠与点翠装饰的云形饰件），翠口圈拆为翠、口圈，皂罗额子拆为皂、罗、额子，描金龙文拆为描金、龙文。
- 拆出来的某一部分单独不成服饰词的，或者内部结构有歧义、拆法不唯一的，整体不拆。例如珠结、珠滴、翠盖（结、滴、盖单独不成词），珠宝钿花、金宝钿花、抹金银宝钿花（可读作珠宝加钿花，也可读作珠加宝钿花，拆法不唯一），大珠花、小珠花（大小是品类的一部分）。
- 珠翠修饰一件物件时拆为珠、翠，翠指点翠，归 material_technique；珠翠单独作名词、泛指首饰时（如珠翠满头、先营珠翠）作一个词，归 headwear_jewelry。
- 前一部分是形状、式样或大小的说明、不是材料颜色工艺的，整体不拆。例如花钗、唐巾、东坡巾、小花、大珠花。量词和数字（九树、四十片）不记。
- 毛皮类：貂裘、狐裘、羔裘拆为貂、裘等两行，两个字在文言中都可指皮毛，都归 material_technique。
- 两个各有独立意义的物名并列成词的，拆开，例如钏镯拆为钏、镯，簪钗拆为簪、钗，金玉拆为金、玉，同一个 combo。
- 拆开后衣物部分只剩衣、服这类泛称的，整体作一个词，不拆。例如翟衣、鞠衣、团衫（不拆成翟、衣或团、衫）。这条只适用于前一部分不是材料、而是定出衣物种类的情况。前一部分是材料的，仍按材料加物件拆开，例如金饰件拆为金、饰件，玉饰件拆为玉、饰件，金事件拆为金、事件，饰件、事件、首饰归 generic。衣上另外记述的纹样照记，例如“翟衣……织翟文”中翟衣、翟文各记一行。
- 只有冠服的定名整体作一个词，不拆。例如珠翠冠、珠翠庆云冠、双凤翊龙冠、九翟冠、山松特髻。
- 工艺词中前一字是动作、单独不成服饰词的，整体作一个词，例如描金、销金、织金、泥金、圈金，不拆成描、金。
- “饰”和“文”一样是后缀，跟着最后一个成分，不单独成行。例如绣饰作一个词，归 material_technique；龙凤饰拆为龙、凤饰，归 headwear_jewelry。
- 几个母题组成的纹样按母题拆开，“文”字跟着最后一个母题，例如云龙文拆为云、龙文，云霞翟文拆为云霞、翟文，云霞孔雀文拆为云霞、孔雀文。明代霞帔按品级更换的是禽鸟，云霞不变，拆开才能看出这层等级。
- 冠上、头上装缀的龙、凤、翟、牡丹、云等形象归 headwear_jewelry；织绣在衣料上的龙凤文、翟文、云霞文归 pattern。数量（九、四、二十四片）不记，需要时写进 notes。

**判断顺序。** 先看它能否单独穿戴：能，归 garment 或 headwear_jewelry；不能，只是衣服上的装饰，归 material_technique。同一个词因位置不同可以归不同类别，以原文为准，例如戴在头上的 fazoletto 归 headwear_jewelry。

**泛称与回指。** 衣、服、冠、饰这类字只在泛指衣物或首饰时归 generic；指向文中一件具体物件时，按那件物件归类。

**动词与插戴的实物。** 簪、佩、戴、服、饰作动词时不记。鲜花、草、纸符等实际插戴在身上的东西，按插戴位置归类，notes 写明是实物，例如“簪以榴花”记榴花一行，归 headwear_jewelry，notes 写“鲜花，簪于发”。

**不标的词。** 人名、地名、官名不标，除非它是服饰名的一部分。只表示价值、数量、尺寸、位置的词不标，需要时写在 notes 里，例如“一指宽”“在头上”。

## 四、wearer 穿戴者

| 值 | 何时填 |
|---|---|
| female | 文中把此物与妇女、少女、妻、娼妓、婢女相连。意大利法令多数专门针对妇女，条文省略主语时也填 female |
| male | 只与男子相连 |
| both | 男女都提到 |
| unclear | 看不出 |

适用对象如果更具体，例如“满十岁的少女”“娼妓”，写在 notes 里。

**文中未直接标明性别的人群，按下列顺序判断，并在 notes 写明依据。**

1. 文中直接标明的，照文本。例如乐妓、女乐、妇人、妻为 female。
2. 同一条记录把女性人群另外单列、并用女性字样标出时，未标女性字样的人群按 male。例如教坊司条另列“乐妓”，俳长、色长、歌工、乐工就按 male，notes 写“同条另列乐妓”。
3. 职名本身有固定性别的，按职名。乐工、乐艺、伶人、俳长、色长、歌工、乐舞生、协律郎、生员、监生、举人、校尉、皂隶为 male；乐妓、女乐、歌章女乐、命妇、宫人、女官为 female。
4. 以上都不适用，填 unclear。

## 五、negated 允许、禁止或限额

| 值 | 含义 | 标志 |
|---|---|---|
| 0 | 允许或中性，包括强制穿戴（notes 写“强制”） | 许用、possino portare、sien tenute portare |
| 1 | 禁止。此物在这个语境中无论多少都不许 | 不许、不得、禁、non possa、sia vietato、poco o molto |
| 2 | 限额。在数量、尺寸、价值、件数的上限以内允许，超出才禁止 | 不过若干、止许一件、non più che、più d'otto |

填2时，把上限写进 notes，例如“上限8片”“不超过50弗罗林”。

## 六、combo 组合编号

几个词合起来才构成被规定的那件东西时，给它们填同一个编号。

**编号分两层。** 字母表示一件完整的东西，数字表示这件东西上的一个部件。

- 整件东西的名称，以及只属于整件东西、不属于某个部件的词，填字母，如 a。
- 某个部件的各个词（材料、形象、垂饰等）填字母加数字，如 a1、a2。同一个部件的材料和形象填同一个编号。
- 文中没有统摄全体的物件、只是几件东西并列时，每件东西各用一个字母，不加数字。
- 每条记录从 a 重新开始。

**negated 与 renamed 按组合判断**，组内每个词填同样的值。

**单独出现的词**，combo 留空。

**拆分规则不变**，衣服名与颜色、面料、工艺分开，各占一行；拆到每一部分都能单独成为服饰词为止。

例如 veste d'oro（金色礼服）：veste 和 oro 都填 c。被禁的是金色礼服，不是礼服本身，也不是金本身。

## 七、特殊情况

**重复出现。** 同一写法在同一条记录里只记一行。第二次出现时如果 wearer 或 negated 不同，或属于另一个组合，另记一行。

**写法变体。** 写法不同的变体各记一行，如 gamurra 与 ghamurra，归并留到后面统一做。

**回指已记的物件。** 文中用“中一”“馀皆”“其”“上有”“下垂”“饰以”或单字“冠”“衣”等回指前面已记的物件时，回指的词照记一行，并入被回指物件的 combo，notes 写“回指某某”，类别随被回指的物件，例如回指大袖衣的“衣”归 garment，不归 generic；如果写法与组内已记的词相同，按重复词规则只记一行。回指句中新出现的部件也并入该组。例如“其冠饰翠龙九，金凤四，中一龙衔大珠一，上有翠盖，下垂珠结，馀皆口衔珠滴”，整段都是对冠的描述，冠填 a；翠龙及其所衔大珠、翠盖、珠结、珠滴填 a1；金凤及其珠滴填 a2。“馀皆”指其余的龙和凤，珠滴在 a1、a2 各记一行。又如“龙凤珠翠冠……冠制如特髻”，后面的冠另记一行，与龙凤珠翠冠同组，notes 写“回指龙凤珠翠冠”。

**并列选项。** 用 o、overo、或、或者连接的选项，每个选项各记一行，同属一件被规定之物的选项填同一个 combo，notes 写“选项”。

**改名。** 看到“俗谓”“名曰”“谓之”“谬称”、detto、chiamato 一类说法，相关的词 renamed 填1。例如“大衣（俗谓长襖子）”，大衣和长襖子两行都填1。

**拿不准。** 不要硬判，按最接近的规则填，在 notes 里写明疑问，例如“饰件，归类存疑”“不确定是否服饰词”。冻结前统一过一遍。

## 八、示例

**文言。** “士庶妻，首饰用银镀金，耳环用金珠，钏镯用银，服浅色团衫，用紵丝、绫罗、紬绢。”

| surface | category | wearer | renamed | negated | combo | notes |
|---|---|---|---|---|---|---|
| 首饰 | generic | female | 0 | 0 | a | |
| 银镀金 | material_technique | female | 0 | 0 | a | 作一个词 |
| 耳环 | headwear_jewelry | female | 0 | 0 | b | |
| 金珠 | material_technique | female | 0 | 0 | b | |
| 钏 | headwear_jewelry | female | 0 | 0 | c | |
| 镯 | headwear_jewelry | female | 0 | 0 | c | |
| 银 | material_technique | female | 0 | 0 | c | |
| 浅色 | color | female | 0 | 0 | d | |
| 团衫 | garment | female | 0 | 0 | d | |
| 紵丝 | material_technique | female | 0 | 0 | d | 选项 |
| 绫罗 | material_technique | female | 0 | 0 | d | 选项 |
| 紬绢 | material_technique | female | 0 | 0 | d | 选项 |

**意大利文，全禁与限额并存。** “neuna fanciulla o garzonetta… possa portare… panni o vestimenti increspati o faldati o ripiegali… poco o molto, nè vestimento nel quale sieno più d'otto gheroni o gheroucini”

| surface | category | wearer | renamed | negated | combo | notes |
|---|---|---|---|---|---|---|
| panni | generic | female | 0 | 1 | a | 满十岁少女；选项 |
| vestimenti | generic | female | 0 | 1 | a | 选项 |
| increspati | material_technique | female | 0 | 1 | a | 起皱；选项 |
| faldati | material_technique | female | 0 | 1 | a | 打褶；选项 |
| ripiegali | material_technique | female | 0 | 1 | a | OCR 应为 ripiegati；选项 |
| vestimento | generic | female | 0 | 2 | b | |
| gheroni | garment | female | 0 | 2 | b | 上限8片；选项 |
| gheroucini | garment | female | 0 | 2 | b | OCR 应为 gheroncini；上限8片；选项 |

**意大利文，强制佩戴与选项。** “sien tenute portare un velo, overo sciugatoio o fazoletto o altra peza, in capo, che habbi una listra… d'oro o di seta o d'altra materia gialla”

| surface | category | wearer | renamed | negated | combo | notes |
|---|---|---|---|---|---|---|
| velo | headwear_jewelry | female | 0 | 0 | a | 强制；选项 |
| sciugatoio | headwear_jewelry | female | 0 | 0 | a | 选项 |
| fazoletto | headwear_jewelry | female | 0 | 0 | a | 此处戴在头上；选项 |
| peza | generic | female | 0 | 0 | a | 选项 |
| listra | material_technique | female | 0 | 0 | a | 缝在头巾上的条带 |
| oro | material_technique | female | 0 | 0 | a | 选项 |
| seta | material_technique | female | 0 | 0 | a | 选项 |
| gialla | color | female | 0 | 0 | a | |

**无服饰词的条目。**

| record_id | surface | category | wearer | renamed | negated | combo | notes |
|---|---|---|---|---|---|---|---|
| FI1356-045 | | | | | | | 无 |
