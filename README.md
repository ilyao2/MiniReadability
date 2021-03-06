# MiniReadability
## How to use

Console application
main.exe (URL (config_path))

* main.exe  
Application will ask you URL
* main.exe (URL)  
Application will save file with default config
Default config works for lenta.ru and gazeta.ru
* main.exe (URL) (config_path)  
Will use json config from path

## Config
### Parameters
- words_wrap (bool)
- rows_size (int)
- except_class_list (list[str])
- except_id_list (list[str])
- except_tag_list (list[str])
- need_attr_list (list[str])
### Default config
These parameters remove ads and unnecessary elements for lenta.ru or gazeta.ru  
```json
{
  "words_wrap": true,
  "rows_size": 80,
  "except_class_list": [
    "b-topic-sidebar",
    "b-socials",
    "b-topic-addition",
    "b-tabloid",
    "b_audio_wrapper",
    "b-header",
    "b_social_sharing",
    "adcenter-wrapper",
    "closebtn",
    "voice-over__label"
  ],
  "except_id_list": [
    "header",
    "footer",
    "recommender",
    "article_main_video",
    "article_pants",
    "right",
    "news-left"
  ],
  "except_tag_list": [
    "script",
    "noscript",
    "link",
    "nav",
    "footer",
    "header", 
    "news-right",
    "news-pants", 
    "rcm_home", 
    "add_rcm_point"
  ],
  "need_attr_list": [
    "href",
    "src"
  ]
}
```
## How it works
### libs
- Pyhton 3.9
- lxml
- beautifulsoup4
- requests

### Usage
```python
from mini_readability import MiniReadabilityManager as Manager

manager = Manager()
manager.read_url(URL)
print(manager.URL)
print(manager.HTML)
print(manager.text)
manager.save_in_file()
```

### Classes
- MiniReadabilityManager
    - HTMLFormatter
        - HTMLRequiredGetter
        - TextStyler
        
#### HTMLRequiredGetter
Contains:
- except_class_list (list[str])
- except_id_list (list[str])
- except_tag_list (list[str])
- need_attr_list (list[str])

Recursively descends the HTML tree, excluding unnecessary branches.
Gathers text from leaves and removes them. Thus, the text of branches,
where there is both normal text and other tags, will not be lost.  
For example:
```html
<div>
  <div> some text 1 </div>
  some text 2
  <div> some text 3 </div>
</div>
```
It returns:  
some text 1  
some text 3  
some text 2

Yes, it have bug)))  
The wrong order is formed under such conditions

Code:  
```python
def __get_dom_child_text(self, node) -> str:
    """ Recursive func for deep-check html dom-tree """
    text = ''
    child_list = [e for e in node.children if e.name is not None]
    if child_list:
        # Excepting elements
        for child in child_list:
            if child.name in self.except_tag_list:
                child.decompose()
                continue
            elif 'class' in child.attrs and set(child.attrs['class']) & set(self.except_class_list):
                child.decompose()
                continue
            elif 'id' in child.attrs and child.attrs['id'] in self.except_id_list:
                child.decompose()
                continue
            # Recursive appending elements
            text += self.__get_dom_child_text(child)

    blank_line_flag = False

    # Saving required text
    if node.text.strip() != '':
        text += ' '.join(node.text.split()) + '\n'
        blank_line_flag = True

    for attr in self.need_attr_list:
        if attr in node.attrs:
            text += '[' + node.attrs[attr] + ']\n'
            blank_line_flag = True

    if blank_line_flag:
        text += '\n'

    node.decompose()

    return text
```

#### TextStyler
Contains:
- words_wrap (bool)
- rows_size (int)

if wrap on:  
Split paragraphs by number of characters  
```python
'\n'.join([page[i:i + self.rows_size] for i in range(0, len(page), self.rows_size)])
```  
if wrap off:  
Split words in paragraph and look at words lenght  
```python
def __wrap_words(self, words: list[str]) -> str:
    row = ''
    page = ''
    for word in words:
        if len(row) + len(word) > self.rows_size:
            if not row:
                row = '\n'.join([word[i:i + self.rows_size] for i in range(0, len(word), self.rows_size)])
                page += row + '\n'
                row = ''
                continue
            page += row + '\n'
            row = ''
        row += word + ' '
    if row:
        page += row + '\n'
    return page
```  

## Examples of work
### URL: https://lenta.ru/articles/2020/12/23/kozlov/
```
Коронавирус с нами надолго. Как научиться жить в новой реальности — отвечает 
психолог: Общество: Россия: Lenta.ru 

00:01, 23 декабря 2020

«Перемещаемся в сторону нормального, здорового страха»

Коронавирус с нами надолго. Как научиться жить в новой реальности — отвечает 
психолог 

[https://icdn.lenta.ru/images/2020/12/19/19/20201219194658357/detail_f58ba46f5c4
efabb6435364a5c291bf1.jpg]

Фото: Максим Шеметов / Reuters

«Ленте.ру»
[/tags/organizations/lenta-ru/]

Вячеслав Козлов
[/tags/persons/kozlov-vyacheslav/]

Практически год назад пандемия коронавируса пришла в Россию и стала одним из 
самых сильных испытаний для страны за последние десятки лет. Страх перед 
неизвестной болезнью во время первой волны сменился страхом перед статистикой 
заболеваемости и смертности во второй, а впереди, по разным оценкам, еще год или 
два года эпидемии, пока COVID-19 не станет обычной болезнью, такой как грипп. 
Как перестать бояться, где искать ресурсы, чтобы не сойти с ума в изоляции, и 
чему пандемии еще только предстоит нас научить — рассказал психолог , который 
сам совсем недавно был пациентом «красной зоны» ковидного госпиталя. 

«Лента.ру»: Как бы вы охарактеризовали настроения россиян к концу года и их 
психическое состояние? 

Козлов:

Если наш разговор о том, каким образом на эти настроения повлиял ковид, то я бы 
вот как откликнулся. Если весной был достаточно большой уровень тревоги, 
связанный с тем, что мы встретились с чем-то непривычным, пугающим, то за лето 
произошло определенное прояснение многих важных вопросов. Не только медицинских, 
но и социально-экономических. 

[https://icdn.lenta.ru/images/2020/12/19/18/20201219180235867/preview_72c2b6a7bf
6798cfc6f1ef3def8bafa0.jpg]

Вячеслав Козлов

Сейчас уже появилось ощущение, что мы начали адаптироваться к тому, что 
происходит, воспринимать многие вещи спокойнее. Тревоги, связанной с 
неопределенностью ситуации, становится меньше. Нельзя сказать, что она совсем 
исчезла, — она не исчезнет, потому что болезнь присутствует, люди болеют, цифры 
показывают под 30 тысяч ежедневно выявленных, и болезнь протекает сложно. При 
этом мы стали воспринимать ковид и то, что с ним связано, как часть реальности, 
с которой надо научиться как-то быть и как-то справляться. 

Большущую роль тут играет объективное информирование: какие исследования по 
этому поводу есть, как продвигается понимание причин болезни, способов ее 
лечения, процессов восстановления, и так далее. Есть те, кто переболел, и они 
рассказывают свои истории, делятся своим реальным опытом. Это тоже важно. 

Самый страшный страх — неназванный. [Здесь] страх как будто получил свое 
название, и, может, до конца не ясно, как именно победить вирус, но формируется 
хотя бы представление — это не что-то большое и глобальное, что нас всех 
обязательно убьет. Это просто сложная, тяжелая задача, которую надо решить. 

У людей есть именно страх, а не тревога? В чем разница этих состояний?

Тревога, как правило, сопровождает жизнь человека фоном, а страх — предметен. 
Когда я чего-то боюсь, то отдаю себе отчет, чего именно боюсь. А если я начинаю 
отдавать себе отчет в том, чего я боюсь, могу это упорядочить: собрать 
информацию о том, что это такое, понять, что я могу или не могу с этим сделать, 
каким образом организовать жизнь, чтобы я был в безопасности, и так далее. А в 
итоге найти выход и разрешить пугающую меня ситуацию. В этом отношении 
постоянная тревога — более опасный стресс. Она есть, и непонятно, что с ней 
делать, каковы ее конкретные причины, как с ней бороться. И это выматывает. 

Весной мы оказались в ситуации тревожной неопределенности, а сейчас перемещаемся 
в сторону нормального, здорового страха. Если я уже заболел, я боюсь конкретных 
вещей: не приедет скорая, не совладаю со скачками температуры, не смогу найти 
необходимые лекарства. Я начинаю говорить об этом с теми, кто готов меня 
поддержать, получаю поддержку, взаимодействую с теми, кто прошел через похожие 
ситуации, — я начинаю что-то делать с этим и в итоге могу справиться 

Весной мы относились с тревогой к будущему и не видели ничего хорошего впереди? 
Или это началось позже, когда цифры начали расти? 

Я думаю, здесь многое зависит от того, какими стратегиями совладания со стрессом 
пользуется каждый конкретный человек. У людей очень широкий набор стратегий: 
кто-то игнорирует, кто-то пытается разобраться, кто-то убегает, кто-то рвется в 
бой. 

На бытовом уровне первыми стали переживать тревогу те, у кого психологические 
защиты самые слабые. Далее ситуация развивалась по нарастающей, и стали 
испытывать тревогу люди, которые в большей степени отдавали себе отчет о 
происходящем, меньше верили тревожной информации из СМИ, но оказались подвержены 
психологическому заражению тревогой, которую транслировали близкие и родные. 

Но параллельно этому возник еще один процесс — после первой волны появилось 
большое количество людей, которые переболели коронавирусом и стали говорить о 
том, что это для них такое было, делиться тем, что им помогало справляться. Их 
тоже стали слушать, и это помогло многим снова обрести возможность трезво 
мыслить и чувствовать себя увереннее. Я думаю, всегда есть те, кто разгоняет 
тревогу, и те, кто работает на ее утилизацию и переработку, чтобы она не 
зашкаливала. 

Люди разгоняют и утилизируют тревогу неосознанно?

Если говорить об осознанности и неосознанности, есть профессии, направленные на 
утилизацию тревоги: психологи, врачи, соцработники. Те люди, которые работают на 
сохранение определенного положительного социального уровня. А вот некоторые СМИ 
грешат тем, что ловят информационный хайп на недоказанных и необоснованных 
сведениях, их задача — привлекать внимание к себе, масштабируя «3С» (три С: 
секс, скандал, страх). Так что есть институты, которые работают и на разгон 
тревоги, и на ее замедление. 

Но обычные люди часто не осознают, на что они работают. Под работой я имею в 
виду то, на что именно они откликаются и источником чего они являются. Это во 
многом зависит от жизненной позиции, которую занимает человек в принципе. 

А отношение к ситуации меняется?

Я точно могу сказать, что смена отношения к происходящему может поменяться как в 
одну, так и в другую сторону. Например, человек сначала занимал позицию «это все 
фигня, кто-то хочет нажиться на продаже масок и антисептиков, ковида нет, 
переболеем, и будет незаметно», а потом сам заболевал, оказывался в «красной 
зоне» и оттуда писал: «Блин, ребят, это на самом деле страшно, это не грипп, мне 
тяжелее» — это в одну сторону. 

[https://icdn.lenta.ru/images/2020/12/19/19/20201219193624870/pic_c439ca7f2a27e5
1864b4d7dbaa46d7c0.jpg]

Фото: Софья Сандурская / АГН «Москва»

В другую — человек паниковал, прям боялся, но при этом заболел кто-то из 
родственников. Тут происходят две вещи. Первое — если я отвечаю за этого 
человека, то у меня нет времени паниковать, я начинаю заботиться о другом. После 
того как я понимаю, что я о нем позаботился, и тот прошел через все у меня на 
глазах, дальше нет оснований паниковать. Я понимаю, что с этим можно жить. Это 
непросто, но я понимаю, что это меня не убьет и не разрушит. Тогда человек 
успокаивается и говорит: «Да, это объективная реальность нашей жизни, тяжелая, 
непростая, при этом я с этим справлюсь». 

Отношение в итоге зависит от того опыта, который мы получаем.

К концу года многие из нас выгорели — мы заперты на удаленке, у некоторых 
заболели и умерли близкие. Это опасность того, что мы начнем впадать в апатию? 

Так может случиться, это имеет психологическое основание. Когда человек долго 
находится в стрессе и все никак не может с ним справиться, то тратится огромное 
количество энергии, и нормальная психика «срывает стоп-кран». Кончаются ресурсы 
на то, чтобы злиться, бояться, бороться. Если я с паникой не смог совладать, то 
психика начинает обо мне заботиться, и я начинаю погружаться в состояние апатии, 
отключаюсь от способности бурно реагировать на внешние раздражители. 

Апатия — одна из граней переживания стресса, когда страх, гнев или какое-то иное 
сильное чувство уже родиться не может, потому что человек истощился. И тогда 
основная задача — помочь человеку справиться с длительным стрессом, это можно и 
нужно сделать 

А если у человека заканчивается ресурс, кроме апатии может ли у него развиться 
какое-то психическое расстройство или проявиться что-то хроническое? 

На бытовом уровне, если у человека нет внутренних ресурсов, он «перегорел», и не 
получается эффективно и конструктивно реагировать на происходящее, он начинает 
делать это так, как может. Тогда небольшое раздражение легко разгорается и 
превращается в гнев, тревога может быстро перерасти в панику. Человек теряет 
эмоциональную устойчивость и может легко впадать в крайние или пиковые 
состояния. Но чтобы чувствовать что-то большое и сильное — нужен ресурс, а так 
как его нет — долго это продолжаться не может. То есть человек вспыхнул, голос 
повысил, но эти дрова быстро сгорели, других нет, взять их неоткуда, все гаснет. 

Если говорить о появлении хронических или длительных сложностей, то здесь 
большое значение имеет предрасположенность. Свойственное некоторым людям 
катастрофическое мышление может усугубиться до депрессии. Вспыльчивость — до 
агрессии. Тревожность перейти в постоянный страх. И так далее. Похожие процессы 
в результате длительного стресса могут произойти и в организме. Могут быть 
реакции желудочно-кишечного тракта, проблемы сердечно-сосудистой системы, 
гормональный сбой, аллергические реакции, много чего может быть. Помним, что 
психика всегда стремится к исцелению. Если в психологическом плане справиться с 
внутренним напряжением, вызванным стрессом, не получается, то напряжение находит 
свое отражение в организме. Пострадает «самое слабое звено», например, если был 
хронический гастрит, то может открыться язва — то есть проблемной зоной станет 
то, к чему человек предрасположен. 

Четырехуровневый барьер

Вернемся к СМИ. Чего люди боятся больше — заразиться или информации про пандемию 
и ограничения? 

Я думаю, что люди больше всего переживают из-за возможной потери привычного 
образа жизни. А это в свою очередь может быть связано с очень многими вещами — 
со здоровьем и появившимися ограничениями, если я заболел, с рухнувшими планами 
на путешествия в ситуации закрытия границ, с отложенным повышением по должности 
из-за сокращений в компании, с потерей личного благополучия из-за локдауна. Если 
СМИ вещают о чем-то, что может повлиять на мой привычный образ жизни, отменяет 
мои планы, сводит на нет мои ожидания, то мне становится тревожно. 

Допустим, мы можем оградиться от негативных новостей, которые ввергают нас в 
стресс, — не читать их, не смотреть. Но близкие могут их нам приносить. Что 
делать? 

Я думаю, это зависит от готовности человека выставлять свои границы. Я бы 
разделил это на четыре уровня так называемой психологической близости к 
различным источникам не самой позитивной информации. 

Первый уровень, самый дальний, это СМИ — инфополе, в котором распространяются 
какие-то страшные и ужасные истории. На это можно достаточно легко влиять: 
выключать телевизор, не читать новостную ленту в интернете, переключать радио в 
машине. 

Второй — встречные люди, с которыми я сталкиваюсь, коллеги по работе. Если я 
готов проявить некоторую решительность и приложить усилия, чтобы не вовлекаться 
в ненужные разговоры, то могу прямо сказать: «Давайте не будем об этом говорить, 
поговорим о чем-нибудь более интересном, позитивном». Если я готов настоять на 
этом, то я смогу себя оградить от токсичной информации. 

[https://icdn.lenta.ru/images/2020/12/19/19/20201219192831295/pic_9dafb945b254f0
5ec4158348d66cbaf3.jpg]

Фото: Александр Авилов / АГН «Москва»

Третий — самый близкий круг, родственники и друзья. Здесь сложнее всего. 
Особенно если внутри этого круга есть распространитель панических настроений и 
ужасных новостей, а я не могу на него повлиять. Тогда мне будет очень тяжело, но 
это тоже моя ответственность — невозможность сказать: «нет, об этом мы говорить 
не будем, я этого не хочу». Тогда надо менять привычные семейные сценарии. Это 
не просто, но можно сделать. Будет полезно всем членам семьи. 

И вот четвертый уровень — то, что внутри меня, мои собственные установки, 
убеждения, взгляд на жизнь. Надо самому себе дать отчет, почему у меня рука 
тянется к пульту телевизора, почему я участвую в разговорах, в которых не хочу 
участвовать, что со мной происходит, если я продолжаю привносить это в свою 
жизнь. И если я понимаю, что это мне вредит, то зачем я продолжаю это делать? 
Если сложно найти ответ, то лучше обратиться за поддержкой к профессиональному 
психологу. 

Надо задать себе вопрос, почему это происходит и что я могу сделать, чтобы этого 
не было? 

Для меня есть принципиальная разница между вопросами «зачем?» и «почему?». 
Вопрос «почему?» в каком-то смысле бесполезный — он обращает нас взглядом назад, 
и можно придумать сотни вариантов для объяснения причин происходящего, причем 
даже диаметрально противоположных и взаимоисключающих. А если мы задаемся 
вопросом «зачем?», это разворачивает лицом к тому, что будет, — это более 
продвигающий вопрос. 

У вопроса «почему?» есть еще одна ловушка — появляется соблазн передать 
ответственность за происходящее кому-то другому. «Почему это в моей жизни 
произошло? Потому что вот те и вот те чего-то не сделали или как-то не так 
поступили», и так далее. А вопрос «зачем?» предполагает личную ответственность 
за достижение желаемого результата 

Допустим, не получилось оградиться от тяжелых новостей. Как правильно на них 
реагировать? 

Что значит правильно? Мы реагируем так, как мы реагируем. Бесполезно говорить 
себе: «Не бойся!», «Не злись!», «Не расстраивайся!» Это уже с нами происходит. 
Эти реакции — просто следствие. Следствие того, как человек воспринимает свою 
жизнь, как к ней относится. Внешняя реакция, поступок, действие — следствие 
того, что происходит у человека внутри. У меня есть система ценностей, 
верований, отношения к другим. При встрече всего этого с окружающей меня 
реальностью из этой глубины рождается чувство, которое подталкивает меня к 
действию. 

Получается, что сам по себе поступок человека — это результат того, что 
произошло в его внутреннем мире. Например, человек запаниковал при встрече с 
опасностью. Бесполезно говорить человеку: «Не паникуй», потому что паника 
вторична. Почему она вторична? Потому что человек в себя не верит, не верит в 
то, что справится, миру не доверяет, на окружающих не надеется, и это все на 
глубинном уровне. Поэтому бесполезно призывать людей реагировать или не 
реагировать на что-то. Реакция случится автоматически в силу устройства 
внутреннего мира человека. А там изменить что-то одними призывами не получится. 

Вспышка страха

Вы переболели, и довольно серьезно. Как вы относились к вирусу до заражения и 
как относитесь сейчас? 

Отношение менялось. Я предполагаю, что моя реакция не очень широко 
распространена. Во-первых, у меня есть твердое убеждение не слушать 
непроверенную информацию, и я не доверяю в этом СМИ. Поэтому весеннее нагнетание 
тревоги прошло мимо меня. Где-то я останавливал разговоры об этом, где-то просто 
уходил из беседы, не вступал в споры по поводу непроверенной информации. Я 
понимал, что есть какой-то вирус. Я не специалист и не могу составить свое 
экспертное мнение, но я понимаю, что верить непроверенной информации просто 
вредно. Когда говорили об ограничительных мерах, я относился так: «Если это 
необходимо, давайте сделаем». Не могу сказать, что горячо их поддерживал, это 
меняло привычный образ жизни, но готов был доверять, так как такое не на пустом 
месте рождается. Я готов слушать и доверять реальному экспертному мнению, но 
весной его еще не было слышно, а остальное мне не очень интересно. 

Когда я заболел в октябре, то на себе почувствовал, что это тяжелее, чем грипп. 
Помню, у меня была вспышка страха, когда мне сказали, что скорая приедет через 
двое суток, — примерно полчаса мне было не по себе 

Потом я стал отдавать себе отчет, что чувство страха сжигает внутренние ресурсы 
организма. Если скорая приедет не через привычные 30-40 минут, а позже, то мне 
надо помочь себе и поддержать себя, чтобы эти двое суток прожить. При этом у 
меня большой навык приведения себя в устойчивое состояние, это обусловлено и 
профессиональной позицией психолога, и жизненным опытом. Не могу точно сказать, 
как мой случай вписывается в общую статистику. 

[https://icdn.lenta.ru/images/2020/12/19/18/20201219184608176/pic_1e2b85e6d21be0
df26003cc81aad5bd1.jpg]

Фото: Алексей Смагин / «Коммерсантъ»

Когда я заболел — заболела моя физическая часть, а не психологическая. Когда 
человек уходит в страх или панику, то метафорически болезнь тела передается 
психике. Я отдавал себе отчет, что моя задача — поддержать тело. Оно борется с 
вирусом и мобилизует ресурсы, и психика должна помогать. Психологическая и 
физическая стороны очень связаны, существуют психосоматические заболевания, 
например. Если телу плохо, а я еще и начинаю паниковать, то я запускаю болезнь 
дальше. Когда мы переживаем стресс, то вырабатывается гормон кортизол, который 
мешает работе иммунной системы. Если телу плохо, но на уровне психики я устойчив 
и помогаю ему, сохраняю бодрость духа — вырабатываются другие гормоны, которые 
поддерживают иммунную систему, и у меня появляется гораздо больше шансов 
выздороветь. 

Вы говорили про панику. Есть люди, которые этой панике не поддаются, и они 
суперспокойные. Это обязательно должно быть связано с профессиональными 
особенностями или это просто особенности психики? 

Не обязательно связано с профессией. Я думаю, что профессиональная реализация 
лишь развивает личностные качества, а если это есть внутри человека — 
уверенность, доверие к себе и миру, жизнелюбие, — то неважно, кем он работает. 
Он может быть и водителем, и менеджером, это не имеет значения. 

А если человек так называемый ковид-диссидент? Он просто отрицает опасность? Это 
защитная реакция или уверенность, что все врут? 

Я думаю, здесь может быть много причин. Действительно, может быть механизм 
избегания — «раз этого нет, это меня не затронет, и пока я в это не верю, я в 
безопасности». 

Это может быть и скрытой агрессией к миру — я знаю, что это есть, но буду 
отрицать, пусть от этого пострадают другие люди 

Это может быть еще какая-то установка. Но вряд ли там есть что-то конструктивное 
и объективное. 

Очевидно, что люди стали агрессивнее. Постоянно какие-то драки из-за масок, 
ругань. Это проявление общей напряженности или дело в конкретных людях? 

Вы справедливо говорите, что агрессия — это проявление внутреннего напряжения 
человека. Наше переживание внутреннего напряжения напрямую связано с нашими 
представлениями и ожиданиями того, как должен быть устроен мир. Все разнообразие 
чувств рождается при встрече этих ожиданий и реальности. Если реальность 
превосходит ожидания — рождаются положительные чувства. Если не соответствует — 
негативные чувства. Я сейчас специально немного упрощаю, чтобы не погружаться в 
академические дебри. 

Сейчас ожидания многих не оправдались, планы рухнули, расчеты не сложились. 
Отсюда досада, негодование и злость, которые выражаются в виде агрессивного 
поведения. Большинство людей не умеют работать со своим напряжением, поэтому, 
когда оно переполняет, просто выливают его во вне 

Если человек искренне верит — раз он носит, то и все должны носить маски, — у 
него могут возникнуть раздражение и злость при виде человека без маски. Если 
человек допускает, что носит он маску, но это самостоятельный выбор каждого, то, 
скорее всего, такой реакции и не будет. Наши чувства и реакции во многом 
обусловлены ожиданиями от мира и от других людей. Это не про то, чтобы ожиданий 
не было. Это про то, чтобы мы отдавали себе отчет, что наши ожидания — это 
только наш выбор, и навязать его всем остальным не получится. 

[https://icdn.lenta.ru/images/2020/12/19/19/20201219193407570/pic_91b8562884e8c7
b84fb7cf59d41b69fd.jpg]

Фото: Александр Авилов / АГН «Москва»

Лукавый ум

Известно, как многие россияне борются со стрессом. Проблема с алкоголизмом может 
обостриться? 

Есть предположение, что возросло употребление алкоголя, потому что в нашей 
культуре стресс снимается рюмкой или бокалом. Хотя на самом деле не снимается, а 
купируется, это все-таки разные вещи. 

Что значит — алкоголь помогает купировать стресс? То, что реальность никуда не 
девается, но я от нее отстраняюсь, избегаю смотреть на нее. То есть это не 
приносит пользы. Наоборот, сложная ситуация скорее усугубляется. В случае с 
ковидом все еще сложнее. Если я употребляю алкоголь, то иммунитет становится 
слабее. А если я уже переболел, то непонятно, как после коронавируса нервная 
система вообще будет реагировать на алкоголь. 

Многие остались без работы, а кто-то жалуется, что переболел и не может до конца 
восстановиться. Потеря дееспособности воспринимается людьми как крах? 

Что такое крах? Мир не может рухнуть, потому что миру без разницы, как мы к нему 
относимся. Рушится наше представление об этом мире, а оно у нас в голове. 
Уровень стресса, который мы испытываем, зависит от нашей адаптивности, гибкости, 
способности признать, что реальность не соответствует нашим ожиданиям. Мы можем 
пытаться ее изменить, но это ничем не закончится. Наша задача — адаптироваться. 

Вы говорите об очень сложной ситуации — такие вещи на самом деле есть. Таким 
людям нужна поддержка, при этом тут важны две вещи. Первая — способность 
человека, попавшего в непростую ситуацию, говорить, что ему нужна поддержка, и 
искать тех, кто готов откликнуться. Многим сложно признать, что они на самом 
деле нуждаются в помощи, терпят до последнего, когда помочь бывает уже сложно. 
Вторая — позволение себе принять поддержку и не играть в супермена. Люди на 
самом деле откликаются, многие готовы помогать, поддерживать. Я знаю истории, 
когда жители многоквартирных домов кооперировались, чтобы помогать тем, кому 
сложно. Мы же понимаем, что от этого никто не застрахован. Сегодня помогаю я, 
завтра помогают мне. 

А есть ли вообще что-то в нашей истории, что вызвало бы похожее состояние у 
людей, кроме коронавируса, кроме экономической ситуации? Или это явление 
уникальное? 

Я не думаю, что оно уникальное. И точно оно не новое. Если послушать лекции 
профессоров, то коронавирус изучали уже в 70-х годах. Элементы того, что 
происходило в 2020 году, точно были в этом и прошлом десятилетиях — были Эбола, 
свиной грипп, птичий грипп. Ровно так же сначала СМИ поднимали тревожную волну, 
инфополе было насыщено страшными историями, были и заболевшие, и умершие. 
Отличие в том, что это было где-то далеко и с кем-то другим. Те вирусы 
передавались не так легко, как ковид. 

При этом мы давно и повсеместно встречаемся с другими, но похожими проблемами. 
Мы же понимаем, что одновременно есть онкология, СПИД, инфаркты. Есть ДТП, 
которые приводят к инвалидности и потере дееспособности. Есть грипп, от которого 
тоже умирают. Почему мы к ним относимся иначе? Мы признали реальность того, что 
эти вещи есть и они — часть нашей жизни, а коронавирус — это что-то новое, нам 
пока не хочется признавать, что он пришел надолго. Весной казалось, что волна 
пройдет и больше не повторится. Мы сейчас проживем адаптацию к новому 
стрессовому фактору. 

[https://icdn.lenta.ru/images/2020/12/19/18/20201219182933302/pic_72110bf4e87d4c
08ef2ac6876a210702.jpg]

Фото: Кирилл Зыков / АГН «Москва»

Насколько, на ваш взгляд, люди вообще готовы помогать себе адаптироваться к 
новым условиям, не загонять себя, не быть источниками пессимизма и негатива? 

Это вопрос о том, во что я лично искренне верю. Я абсолютно уверен, что в 
глубине своей мы все хотим жить, и жить счастливо. Другое дело, что это 
преломляется через наш лукавый ум. А он легко все переворачивает с ног на 
голову, докажет, что черное — это белое, а белое — это черное. И вот мы выдаем 
какие-то странные, нередко вредные реакции. Но в глубине, там, где мы настоящие, 
мы правда адаптируемся, это неизбежно. Если бы этот механизм не работал, 
человечество вымерло бы уже давно. Будет непросто, но мы пройдем через все 
сложности, справимся. Мы так устроены в базе своей, а все остальное — вторичные 
психологические настройки. 

Тяжелый год

журнал Time
[/tags/organizations/zhurnal-time/]

Недавно написал на обложке, что 2020-й — самый худший год. Но ведь это 
субъективное восприятие? 

Кода я такие вещи слышу, я вспоминаю письмо Николая II жене. Там есть фраза: 
«Скорее бы закончился 1916 год, будь он проклят. 1917-й обязательно будет 
лучше», а там вы помните, что случилось 

Может ли 2020-й повлиять на статистику самоубийств?

прим. «Ленты.ру»

Депрессия есть экзогенная и эндогенная, по классификации МКБ-10 (Международная 
классификация болезней в 10-й редакции — ). Эндогенная обусловлена органическими 
факторами, а экзогенная — психологическими. И сейчас есть предположение, что 
вирус оказывает влияние на появление внутри организма эндогенных факторов 
развития депрессии. Он поражает нервную систему и сердечно-сосудистую. Это 
способствует появлению и развитию депрессии. Один из вариантов максимально 
плохого развития депрессии — суицидальные мысли с последующим суицидом. 

Экзогенная депрессия имеет в основании психологический компонент. Депрессия как 
результат переживания длительного стресса. Если человек предрасположен к 
депрессии, длительное время находится в сильном стрессе, не получает поддержки 
от тех, кто рядом, и не находит сил исправить ситуацию, то это может привести к 
мыслям о суициде с последующей попыткой его совершить. Насколько текущая 
ситуация пандемии с этим связана — не знаю, при этом многим точно не просто. 

А как нам научиться жить с этим всем? Взять ту же удаленку — сидеть в четырех 
стенах тяжело, особенно если живешь с кем-то. Кому-то, наоборот, будет тяжело 
возвращаться на работу. 

Наверное, многие и не захотят возвращаться — они могут быть эффективны в таком 
формате, привыкнут. Кто захочет вернуться — адаптируется. Какие-то вещи будут 
непривычны, но справятся. 

Я очень верю в человека и его способности. Тем, как это проявляется, я восхищен, 
впечатлен и удивлен, насколько мы на самом деле сильны и многогранны. Просто это 
все проявляется в сложные периоды жизни. Сейчас именно такой. У меня нет 
сомнений, что мы справимся. Да, кто-то будет паниковать, кто-то отчаиваться, 
кто-то злиться, но мы справимся 

[https://icdn.lenta.ru/images/2020/12/19/19/20201219193240598/pic_c4e9f3fc711963
97daa05707dcbf0260.jpg]

Фото: Евгения Новоженина / Reuters

Как думаете, сколько времени нам надо на адаптацию?

Чтобы адаптироваться к существенно изменившимся факторам, нужно до года, в 
зависимости от значимости факторов. Если вы переехали в другую квартиру и туалет 
оказался в каком-то непривычном месте, то вам нужно будет около трех недель для 
адаптации, чтобы, проснувшись ночью, найти его в полудреме, не ударяясь об углы. 
Но это не самый существенный фактор. 

Для адаптации к существенным факторам, например, изменению должности или смене 
работы и привыканию на новом месте, нужно полгода. [Пандемия —] это сложнее и 
масштабнее, но в рамках года мы точно уложимся, если, конечно, не произойдет 
чего-то еще. 

Ну за этот год ведь мы не адаптировались?

Ну почему? Мы начинаем адаптироваться с момента признания того, что наступила 
другая реальность. Поэтому я бы не начинал отсчет с весны — мы тогда плохо 
представляли, что происходит. 

Я бы предположил, что для львиной доли россиян это началось с приходом второй 
волны, примерно в начале осени. Когда первая волна пошла на спад, было ощущение, 
что не надо адаптироваться, что все прошло, а потом пошла вторая — и стало 
понятно, что это надолго 

Сейчас уже говорят о третьей волне в марте 2021 года.

Раньше мы жили от Нового года до Нового года — и выдыхали. Теперь мы будем жить 
от локдауна до локдауна? 

С точки зрения психологии тут интересный момент — профессиональные психологи 
призывают человека жить здесь и сейчас. Потому что жизнь — это то, что 
происходит в эту самую секунду. Вчерашнего дня нет — это просто воспоминание, 
будущее — просто гипотеза. Мерилом является качество сегодняшнего мгновения. В 
этом есть колоссальный ресурс, который, кстати, тоже помогает адаптироваться. 
Несмотря на сожаление о прошлом или страх перед будущим, здесь и сейчас нам 
достаточно хорошо, у нас все точно не плохо. Вот прямо сейчас. В эту самую 
секунду. На это и стоит опираться. А жить от сих до сих — это что-то 
неестественное. 

Пандемия нас уже чему-то научила или нам только предстоит учиться и учиться?

Мы только начали учиться. Чтобы выполнить домашнее задание на пятерку, нам еще 
далеко. Для меня основное — идея о том, что кризис с угрозой здоровью 
разворачивает нас к самим себе и к близким людям. В гораздо большей степени, чем 
любой другой экономический кризис. Он разворачивает нас к настоящим приоритетам, 
что для нас важнее: упахиваться на работе или больше времени проводить с детьми, 
купить новый айфон или увидеть счастье в глазах супруга? 

Почему происходит смещение ценностей? Из-за того, что люди осознали близость 
смерти? 

Ну да, вы правы. Мы приложили то, чего мы хотим, к гипотетической шкале 
критериев, важнейший их которых — смерть. Это заставляет переосмыслить 
приоритеты. Экономический кризис такого эффекта не дает — на самом деле человеку 
надо немного, чтобы выжить. Поэтому потерять деньги не так страшно. А вот когда 
вопрос касается жизни или смерти — происходит настоящая внутренняя работа, 
иллюзии пропадают, остается только самое зерно, основание. 

[https://icdn.lenta.ru/images/2020/12/19/18/20201219181609022/pic_820f7cdff49cff
8c1f74b340bc4ef171.jpg]

Фото: Эмин Джафаров / «Коммерсантъ»

А оно всегда одно и то же — не нужны нам ни роскошь, ни излишества, ни даже 
материальное изобилие. Человеку нужен человек 

Мы можем обижаться на родителей, которые не подарили квартиру на свадьбу, но 
когда папа или мама попадают в «красную зону» и стоит вопрос, попадут они оттуда 
на кладбище или домой, — то черт с ней, с этой квартирой. Нам не так уж и много 
надо для того, чтобы жить счастливо. И, похоже, ковид при всей его опасности 
учит нас искать счастье внутри себя, предлагает вновь радоваться каким-то 
простым и повседневным событиям. Разворачивает нас лицом к близким людям. 

Беседовала Майя Гавашели

[/parts/authors/gavasheli/]
```
### URL: https://www.gazeta.ru/social/news/2020/12/24/n_15406796.shtml
```
МИД: российские ученые работают с образцами нового штамма коронавируса - 
Газета.Ru | Новости 

МИД: российские ученые работают с образцами нового штамма коронавируса

Ника Пикекатлет
[/gazeta/authors/nika_pikekatlet.shtml]

24.12.2020 | 16:27

[]

[

//img.gazeta.ru/files3/877/11640877/RIAN_3241930.HR.ru-pic905-895x505-41000.jpg

]

Здание министерства иностранных дел Российской Федерации

РИА «Новости»

МИД
[/tags/organization/mid.shtml]

Мария Захарова
[/tags/person/mariya_zaharova.shtml]

РИА «Новости»

[http://ria.ru]

Официальный представитель России заявила, что российские ученые получили образцы 
нового штамма коронавируса от британских специалистов. Об этом сообщает . 

Она отметила, что Россия проводит интенсивную работу с полученными материалами.

Всемирной организации здравоохранения
[/tags/organization/voz.shtml]

По ее словам, российские ученые в ходе изучения штамма коммуницируют с 
иностранными коллегами и представителями . 

Минздрава
[/tags/organization/minzdrav_rf.shtml]

Мэтт Хэнкок
[/tags/person/mett_henkok.shtml]

Борис Джонсон
[/tags/person/boris_dzhonson.shtml]

14 декабря глава Великобритании сообщил, что британские ученые выявили новый, 
мутировавший, тип коронавируса, который распространяется быстрее известных 
штаммов. Премьер-министр Великобритании заявил, что новая мутация коронавируса 
на 70% заразнее, чем другие виды вируса. 

В связи с напряженной эпидемиологической ситуацией с 20 декабря на юго-востоке 
Великобритании и в Лондоне начал действовать максимальный четвертый уровень 
ограничений. Он предусматривает закрытие всех магазинов, кроме продающих товары 
первой необходимости, а также тренажерных залов, парикмахерских и иных 
заведений. Людям рекомендуется не покидать дома. Ряд стран приостановил 
транспортное сообщение с Великобританией, список этих стран постоянно растет. 

НОВОСТИ ПО ТЕМЕ:

Британский минздрав сообщил о еще одном новом штамме коронавируса

[https://www.gazeta.ru/social/news/2020/12/23/n_15403748.shtml]

—

Moderna проверит свою вакцину против «британского» варианта коронавируса

[https://www.gazeta.ru/social/news/2020/12/24/n_15404096.shtml]

—

Ученый призвал не исключать наличие в России нового варианта коронавируса

[https://www.gazeta.ru/science/news/2020/12/24/n_15404300.shtml]

—

Коронавирус 2019-nCoV

[/news/seealso/13969250.shtml]

Все новости на тему:

[]



```