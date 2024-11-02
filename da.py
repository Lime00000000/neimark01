import asyncio
import logging
import sys
from os import getenv


from aiogram import F, Bot, Dispatcher, html, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import CallbackQuery, Message, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, ReplyKeyboardMarkup, KeyboardButton, FSInputFile
from aiogram.exceptions import TelegramBadRequest


Token = getenv('BOT_TOKEN')


dp = Dispatcher()
dic = {"Москва": 'Курс пх', "Питер": 'молись', "Нижний Новгород": "живи"}
count_sity = {"Москва": 0, "Питер": 0, "Нижний Новгород": 0}
j = 'CAACAgIAAxkBAAO1ZyJbcATNI-BdcnrTQAyLrEOrYnMAAj8vAAJLzZFLN9pSKMYSt9c2BA'
j1 = 'BAACAgIAAxkBAAPjZyMpWN2eEV_HVq1Si1xDrTwGhmgAAr1dAALwgBhJVHq0-kQLQHw2BA'
photo = 'AgACAgIAAxkBAAIBjWcjZlGzImxx02iWQlFW-_L0XKzcAAKY6zEbzHkgSSfqe7Qy6qc3AQADAgADeAADNgQ'
photo1 = 'AgACAgIAAxkBAAIBmGcjbQYikMO9oMrK4f_AupcPvGgRAALF6zEbzHkgSRPXJdzsB8ISAQADAgADeAADNgQ'
stupid = 'AgACAgIAAxkBAAIBxmcjeVRBxMw5z8qHshCKcKHdjmdzAAIp7DEbzHkgSet4MjAIbVVSAQADAgADeAADNgQ'
score = 0
flag = True
flag_restart = False
user_ids = []
check = []
people = {}
teachers_sex_Moscow = [('Фука Явагиси ', 'Олимпиадное программирование','1500 иен\час ', '0', ' Ученица Японской школы Гэккокан. Девушка с отличием закончила учебное заведение. По её словам, параллельно учебе в школе она проходила практику в неком «Тартаре». Скорее всего имеется в виду школа онлайн курсов, в котором Фука смогла отполировать свои знания в сфере IT-технологий. Ученики отмечают скромность девушки, но в месте с тем огромные знания, которыми Явагиси хочет делиться.', 'AgACAgIAAxkBAAIGnGclOQSvAXfmGXsRiVuz4CsCwoiOAAK06TEbzHkoScKsH2e2Z8vAAQADAgADeAADNgQ'),
                       (' Танос ', 'Олимпиадное программирование', '900 руб\час', '1', 'Танос - очень уверенный молодой человек, который ставит себе цель изменить наш мир путём создания команды программистов, которые смогу создавать наисложнейшие продукты. Из преимуществ имеет при себе камень времени, поэтому на обучение у его учеников есть куда больше времени, в сравнении с остальными. Правда иногда за один час обучения придётся платить по двойному тарифу.', 'AgACAgIAAxkBAAIGk2clOQTrfLwR4c72dDLHwhTiCd55AAK16TEbzHkoSbGsbW3l2enSAQADAgADeAADNgQ'),
                       ('Гордон Фримен', 'Олимпиадное программирование', '1500 руб\час ', '2', ' Магистр математики и физики. Его команды являются победителями множества хакатонов и соревнований по программированию. Гордон работает в IT уже больше 30 лет. Он профессионал, про которого ходит множества слухов. Якобы он получил свои знания после опасного эксперимента, побывал в ином измерении. Но узнать правду очень сложно, ведь Фримиен не очень разговорчивый парень.', 'AgACAgIAAxkBAAIGn2clOQTlLYF5WVbWFfmagNaJzHgHAAK36TEbzHkoSdnFZvrZpweeAQADAgADeAADNgQ'),
                       (' Скылл Бокс ', 'Робототехника', '120000руб за курс', '0', ' Скылл Бокс — это ваш личный портал в адско-счастливое, богатое будущее робототехники при поддержке министерства образования России и крупных медиа гигантов, таких как МэйлТочкаСру. Вступай в ряды первопроходцев новейших технологий и помни, наш девиз: «МэйлТочкаСру, всё для людей».', 'AgACAgIAAxkBAAIGkWclOQQY9qrpGaX_VwABsJqluYjlvQACr-kxG8x5KEkEgf67mVTHSAEAAwIAA20AAzYE'),
                       (' СкайКрэнг ', ' Робототехника ', '100000руб за курс ', '1', ' Хотят слухи, что компанией Скай Крэнг управляет неземной разум, который делится высокоразвитыми технологиями и знаниями. Однако никто не знает правду. Ученики же отмечают, что материал подаётся в странной, но вполне понятной и удобной форме. Глава компании часто говорит о захвате мира и постройке космического корабля, но студенты уже привыкли к специфичном шуткам преподавателя.', 'AgACAgIAAxkBAAIGi2clOQRO1F6Hdl3kdg11eryAA1DNAAKr6TEbzHkoSZpUT_W-gaD5AQADAgADeAADNgQ'),
                       (' Леонардо, дай Винчик ', 'Дизайн', '100руб\час ', '0', ' Москвич человек без определенного места жительства, который открыл в себе способность к искусству и взял псевдоним известного художника, после чего мужчина решил открыть свои собственные курсы дизайна. Ученики отмечают резкое амбре, но на удивление крайне сильные и интересные занятия. В целом студенты советуют нового Леонардо, но с определенными оговорками ', 'AgACAgIAAxkBAAIGtmclPKatbyHRGU4_hQdgXWpYyULGAAKn5jEbhDYoSWlX_rUVv6OpAQADAgADbQADNgQ'),
                       (' Марк Уиллер', 'Дизайн', '1000дол\час ', '2', ' Как сказал Конфуций “Чтобы стать лучшим в своем деле, нужно учиться у лучших“ .Поэтому перед вами Арт-директор Microsoft, можно сказать, икона веб-дизайна. Марк переехал в Россию, когда узнал, что в Нижнем Новгороде открывается кампус Неймарк после этого он сказал Америке звезда поэтому он решает открыть свою школу  дизайна и надеется что никто не пройдет мимо ', 'AgACAgIAAxkBAAIGuWclPZL506YWBa7_UHMm5SI6JAqSAAKs5jEbhDYoSTDoL-0-NumEAQADAgADbQADNgQ'),
                       (' Джокер', 'Дизайн', ' Работает ради удовольствия ', '1', ' Джокеру надоело разграблять Готем, поэтому этот харизматичный человек решился забрать все свои эскизы и переехал в Нижний Новгород , где открыл свою школу дизайна. Ученики отмечают его убийственные шутки)', 'AgACAgIAAxkBAAIGu2clPawLt44LL_2088nAlH8n-fg-AAKt5jEbhDYoSZr5w6PlsfLwAQADAgADbQADNgQ'),
                       (' Тони Старк ', 'Робототехника', '15000дол/час ', '2', ' После того, как Тони Старк смог спасти вселенную не один раз, ему стало немного скучно, и он решил разнообразить свою жизнь. Поэтому Страк создал курсы по робототехнике, чтобы передать свои знания следующему поколению гениев. В итоге студенты не только научились создавать умные машины, но и получили незабываемые впечатления от занятий с самим Тони Старком. А он, в свою очередь, понял, что учить других — это такая же захватывающая приключение, как и спасать мир.', 'AgACAgIAAxkBAAIGw2clPdtPxids0HOam9OOpHArHhdLAAKu5jEbhDYoSdcxlpguUbuNAQADAgADbQADNgQ')]


teachers_sex_NN = [('Олег', 'Олимпиадное программирование', '1кг. листьев\час ', '0', ' Несмотря на то, что Олег- олень, он имеет колоссальное количество знаний с сфере программирования. Говорят, что однажды на Олега упал ноутбук Олега Тинькова, и с этого момента молодой оленёнок стал очень быстро обучаться IT-технологиям. После благодаря победам в множестве хакатонов Олег смог переехать в большой город и открыть свою школу олимпиадного программирования. Из плюсов ученики отмечают дешевизну обучения.', 'AgACAgIAAxkBAAIGj2clOQSHWpG6F7z2kuGUJFh0N_yIAAKs6TEbzHkoSaAOe7RRkGi4AQADAgADbQADNgQ'),
                   ('Текна', 'Олимпиадное программирование', '800руб\час ', '1', ' Текна характеризуется своими учениками как аккуратная и рациональная девушка, которая всегда выбирает логический подход для выхода из сложных ситуаций. Хотя она может казаться немного холодной и отчуждённой, она всегда ласковая и щедрая со своими студентами. Так же не представляет жизнь без своих гаджетов.', 'AgACAgIAAxkBAAIGm2clOQTT8rcOOFvvJ_CJmW5u7LvIAAKy6TEbzHkoSS6hheyHuDleAQADAgADbQADNgQ'),
                   (' Пётр Паркин', 'Олимпиадное программирование', '1500руб\час ', '2', ' Дружелюбный сосед всегда рад прийти на помощь своим ученикам Нижегородцам. Пётр самый настоящий вундеркинд, который к своим 17 годам является преподавателем в Высшей Школе Экономике по направлению прикладной математике и информатике. Паркин всегда рад работать со своими учениками несмотря на то, что очень часто они старше его.  Ребята отмечают, что Пётр часто спасает их из самых сложных ситуаций. Так же он им кого-то напоминает, но не могут вспомнить кого.', 'AgACAgIAAxkBAAIGkGclOQTtAnfDO1cuDR2qXTtSe_lZAAKx6TEbzHkoSTl5nrti0oztAQADAgADeAADNgQ'),
                   (' Мехамару ', 'Робототехника', '2000рую\час ', '2', ' Мехамару-студент Киотского магического колледжа. Из-за небесного проклятия он родился без правой руки и нижней части ног. В обмен на неполноценность он получил огромную проклятую энергию, которую использует для управления механическими марионетками. Благодаря своей способности он наглядно демонстрирует то, как устроены роботы. Несмотря на то, что Мехамару лично не присутствует на занятиях это не мешает ему обучать людей в очной форме продолжая при этом быть гугу робототехники.', 'AgACAgIAAxkBAAIGjmclOQQXHNF3r5qBD-lrDc9ajfP9AAKu6TEbzHkoSaB_EmJ7s3ssAQADAgADeAADNgQ'),
                   (' Ксения Шуина ', 'Робототехника', '1000руб\час', '1', ' Ксения профессионал в IT - сфере, ведь о ней знает вся столица мира. К ней сложно пробиться, но если ты сможешь, то не пожалеешь. Ксения программист, дизайнер, разработчик и просто скромная, хорошая девушка. Ученики отмечают особенный подход обучения, построенный на эмпатии и высоком уровне знаний, которые даёт Ксения.', 'AgACAgIAAxkBAAIGjGclOQSAd32fcv_l_s_geg604lrWAAKp6TEbzHkoSWcfDx4-3qW7AQADAgADbQADNgQ'),
                   (' Софья Авдонина ', ' Робототехника ', '750 руб\час ', '0', ' 2)  Ее имя знает каждый, кто хочет добиться успехов в робототехнике. Только она может обеспечить высококлассную базу знаний в этой чудесной сфере. Ученики в восторге от ее техники преподавания. Они занимают призовые места в международных фестивалях и конкурсах.', 'AgACAgIAAxkBAAIGkmclOQQpC9V-QcAg1FaWcG20uQaJAAKw6TEbzHkoSShTze9b9NY0AQADAgADbQADNgQ'),
                   (' Майлз Моралес ', 'Дизайн', '50дол\час', '0', ' Майлз Моралес – после съемки в фильмах обретает славу и богатства, он продолжает рисовать и открывает свои курсы, где выступает в роли наставника, от учеников нет отбоя. Он всегда рад новым ученикам.', 'AgACAgIAAxkBAAIHkWclS0ounsEhDnm6zr9T5LbJd8skAALc5jEbhDYoSSTnNjEJziH_AQADAgADbQADNgQ'),
                   (' Арзамасский гусь ', 'Дизайн', '200дол\час ', '2', ' Арзамасский гусь – после того как Арзамас провозгласили столицей мира он сразу же обрел не бывалую популярность. И ему хотелось сделать мир лучше, он начал преподавать дизайн в АПИ. От студентов не было отбоя каждый был готов сидеть, часами слушая интересные лекции.', 'AgACAgIAAxkBAAIHk2clS2DjuanE3xCpD6mKD_bKErPxAALd5jEbhDYoSQbpjj6s9C7WAQADAgADeAADNgQ'),
                   ('Аид', 'Дизайн', 'Работает для души', '1', ' Однажды Аид, владыка Темного Царства, решил разнообразить свою жизнь и начать преподавать курсы по дизайну. Его уроки были настолько темными и страшными, что даже самые опытные студенты испытывали трудности с пониманием материала. Но когда Аид увидел, что его ученики начали создавать потрясающие произведения искусства, он понял, что его уроки действительно оказывают влияние на мир - и теперь он предпочитает шутить, что он преподает "дизайн ада"!', 'AgACAgIAAxkBAAIHlWclS3zGrzsFqRCBRohiF3ogWwmTAALe5jEbhDYoSQeG3LLEx0ETAQADAgADeAADNgQ')]


teachers_sex_Peterburg = [(' Задиль Али', 'Олимпиадное программирование', '666 руб\час', '0', '«Ааас-саляму алейкум мой дорогой Кади. Благословит нас Аллах на начало твоего обучения в одобренном Шариатом направлении IT-технологий. Олимпиадное программирование — это тебе не харам, поэтому ты без проблем сможешь стартануть с него свой путь в этой сфере. За сим предлагаю начать.»', 'AgACAgIAAxkBAAIGnmclOQTOnQUpIpujhs7hhWaEijamAAK26TEbzHkoSY9Qm5v87kKaAQADAgADeAADNgQ'),
                          ('Футаба Сакура', 'Олимпиадное программирование', '2000 иен\час ', '1', ' Безумно талантливая девушка подросток, которая имеет удивительно большие знания в сфере информационной безопасности и олимпиадного программирования. Ученики Футабы отмечают открытость девушки, желание помогать своим ученикам и продвигать их в сфере IT-технологий. Так же говорят, что Сакура может научить, цитата: «Воровать сердца», но не очень понятно, что она имеет в виду.', 'AgACAgIAAxkBAAIGnWclOQQMm4SFTV0ZR_Pf-MfFUVXKAAKz6TEbzHkoSYO-AYuaIB1LAQADAgADbQADNgQ'),
                          ('Павел Дуров', 'Олимпиадное программирование', '100дол\час ', '2', ' Молодой человек, который быстро завоевал свое место под НАШИМ РУССКИМ солнцем.  Пашу называют НАШИМ СЛОНОМ, который обучает НАШИХ будущих мессий программирования. Дуров пользуется большим авторитетом среди своих учеников. Благодаря его мастерству команда «Goida-Team» известна во всех странах СНГ. К сожалению, за свои услуги Паша требует соответствующий гонорар. Но оно явно того стоит.', 'AgACAgIAAxkBAAIGimclOQSb0yZ3oAxEQB6wJ3W-s0KCAAKq6TEbzHkoScLSavpsLDnJAQADAgADeAADNgQ'),
                          (' Алексей Кутузов ', 'Робототехника', '999руб\час', '0', ' Вы будете героями нашего времени, если Алексей не откажет вам в помощи. Алексей Кутузов — тот человек, который вам нужен! Трушный безумный гений, который иногда любит спускаться на низкий уровень. Научит писать программное обеспечение для роботов на ассемблере.', 'AgACAgIAAxkBAAIGjWclOQT5TbNvZbfcObACXte1VteBAAKt6TEbzHkoSZrVsE3QcTU9AQADAgADbQADNgQ'),
                          ('Хаяо Миядзаки', 'Дизайн', '1000дол\час ', '2', ' Миядзаки с детства интересовался японской анимацией и ее выдающимся стилем. Посте окончания обучения молодой человек решил полностью посветить себя созданию японских шедевров, которые будут известны на весь мир, после выпуска своей работы “Мальчик и птица” пожилой профессионал решает открыть свои онлайн курсы для обучения молодого поколения на них он рассказывает все тонкости нелегкого ремесла дизайнера. После окончания курса молодые его ученики без проблем поступают в приличные вузы дизайна, а позже с легкостью находят работу в данной сфере.', 'AgACAgIAAxkBAAIHn2clTwsC-i1yuj3DJHDvyR_LY5CpAALt5jEbhDYoSRt1pf-eaSUwAQADAgADbQADNgQ'),
                          ('Deadpool', 'Дизайн', '100дол\час ', '0', '«Эй, народ! Дедпул тут, и да, теперь я стал преподавателем курсов по дизайну. Кто бы мог подумать, что самый нелюбимый супергерой всех времен и народов будет делить свои знания о стиле и креативности. Но что поделать, у меня теперь свое шоу "Дедпул Гуру Дизайна" - где каждый ученик получает пул-возможность стать настоящим мастером дизайна под моим пристальным вниманием. И помните, если вы опоздали на мой урок, я буду лично приходить за вами и забирать вовремя, пусть это будет нашим маленьким секретным. До встречи на моих уроках, товарищи!»', 'AgACAgIAAxkBAAIHoWclTx-Awl1dYtCuZQc38ylb7CHbAALu5jEbhDYoSTpDqKEAAT0viwEAAwIAA20AAzYE'),
                          ('Юсукэ Китагава ', 'Дизайн', 'Работает за еду', '1', ' Юсукэ учился у известного японского художника. После окончания обучения молодой человек присоединился к творческой команде "Фантомных Воров", где очень сильно прокачал свои навыки рисования. Его картины, отражающие внутренний мир людей завоевали уважение по всей Японии. Китагава решил не останавливаться на достигнутом и открыл свои курсы, на которых он делится своими навыками и идеями. По некоторой информации знаком с учителем по олимпиадному программированию Футабой Сакурой.', 'AgACAgIAAxkBAAIHo2clTzHLUjPbiObd38C77SZ6Qdf6AALv5jEbhDYoSdyKfgxo9q05AQADAgADeAADNgQ'),
                          ('Альтрон', 'Робототехника', ' Помощь в захвате мира ', '2', ' После неудачной попытки захватить мир, Альтрон решил переквалифицироваться и начать новую карьеру в образовании. Он открыл свои курсы по робототехнике, где учит студентов создавать смертоносные машины и захватывать мир, начиная с их собственных кухонных роботов. Уроки включают в себя практические задания, такие как программирование лазеров и уничтожение моделей городов из кубиков. И хотя студенты иногда жалуются на жесткий подход преподавателя.', 'AgACAgIAAxkBAAIHpWclT0Ri4jwJKwM9_kjhRa_VCEcNAALw5jEbhDYoSb-akUc5ZD9NAQADAgADbQADNgQ'),
                          (' Исигами Сэнку ', 'Робототехника', '2000 иен\час ', '1', ' Исигами Сэнку, гениальный ученый, стал преподавателем курсов по робототехнике, объявив на первом занятии, что студенты соберут робота, который будет делать всё. Однако их конструкции больше походили на неуклюжие горы металла, а его робот-помощник вместо кофе пытался запустить ракету. Каждое занятие превращалось в шоу с взрывами и танцующими роботами, и Сэнку подбадривал студентов: "Каждый великий ученый начинал с провалов!" В итоге они выходили с дипломами и уникальными (и слегка опасными) роботами, а Сэнку стал звездой с девизом: "Робототехника — это весело, если вы готовы к взрывам!"', 'AgACAgIAAxkBAAIHp2clT2DXEncgnwww8j9yDifrW7elAALx5jEbhDYoSVx17vUuLL9nAQADAgADbQADNgQ')]


@dp.callback_query(F.data == 'Дизайн')
@dp.callback_query(F.data == 'Олимпиадное программирование')
@dp.callback_query(F.data == 'Робототехника')
async def level(message: Message) -> None:
    try:
        await message.message.delete()
    except TelegramBadRequest:
        pass
    global people
    members = message.message.chat.id
    people[members].append(message.data)
    level0 = InlineKeyboardButton(text='Я зелёный новичок', callback_data='cum')
    level1 = InlineKeyboardButton(text='Я знаком с направлением, но мне есть куда расти', callback_data='cum_print')
    level2 = InlineKeyboardButton(text='Я без пяти минут профессионал', callback_data='copy')
    level_1 = InlineKeyboardButton(text='Я не знаю', callback_data='typoi')
    f = [[level0], [level1], [level2], [level_1]]
    await message.message.answer('Выберите уровень знаний\nВ зависимости от ответа будут выдоваться нужные курсы', reply_markup=InlineKeyboardMarkup(inline_keyboard=f))


@dp.callback_query(F.data == 'typoi')
async def test(message: Message) -> None:
    try:
        await message.message.delete()
    except TelegramBadRequest:
        pass
    global flag
    people[message.message.chat.id][2] = True
    first = InlineKeyboardButton(text='з', callback_data='yes')
    second = InlineKeyboardButton(text='ко', callback_data='no')
    third = InlineKeyboardButton(text='коз', callback_data='no')
    button = [[first], [second], [third]]
    await message.message.answer_photo(photo=photo, reply_markup=InlineKeyboardMarkup(inline_keyboard=button), caption=
                                       'Что выведет этот код?')


@dp.callback_query(F.data == 'yes')
@dp.callback_query(F.data == 'no')
async def check1(message: Message) -> None:
    try:
        await message.message.delete()
    except TelegramBadRequest:
        pass
    if F.data == 'yes':
        people[message.message.chat.id][0] += 1
    if people[message.message.chat.id][2]:
        first = InlineKeyboardButton(text='ГОЙДА', callback_data='1')
        second = InlineKeyboardButton(text='-', callback_data='2')
        third = InlineKeyboardButton(text='БАН', callback_data='2')
        button = [[first], [second], [third]]
        await message.message.answer_photo(photo=photo1, reply_markup=InlineKeyboardMarkup(inline_keyboard=button), caption=
                                           'Что выведет этот код?')
        people[message.message.chat.id][2] = False


@dp.callback_query(F.data == '1')
@dp.callback_query(F.data == '2')
@dp.callback_query(F.data == 'cum')
@dp.callback_query(F.data == 'cum_print')
@dp.callback_query(F.data == 'copy')
async def result(message: Message):
    try:
        await message.message.delete()
    except TelegramBadRequest:
        pass
    ch = message.message.chat.id
    if F.data == '1':
        people[ch][0] += 1
    if message.data == 'cum':
        people[message.message.chat.id][0] = 0
    elif message.data == 'cum_print':
        people[message.message.chat.id][0] = 1
    else:
        people[message.message.chat.id][0] = 2
    if people[ch][3] == 'Питер':
        for el in teachers_sex_Peterburg:
            if el[1] == people[ch][-1] and str(people[ch][0]) == str(el[3]):
                await message.message.answer_photo(photo=el[-1])
                for el1 in el[:3] + el[4:-1]:
                    await message.message.answer(el1.strip())
    if people[ch][3] == 'Москва':
        for el in teachers_sex_Moscow:
            if el[1] == people[ch][-1] and str(people[ch][0]) == str(el[3]):
                await message.message.answer_photo(photo=el[-1])
                for el1 in el[:3] + el[4:-1]:
                    await message.message.answer(el1.strip())
    if people[ch][3] == 'Нижний Новгород':
        for el in teachers_sex_NN:
            if el[1] == people[ch][-1] and str(people[ch][0]) == str(el[3]):
                await message.message.answer_photo(photo=el[-1])
                for el1 in el[:3] + el[4:-1]:
                    await message.message.answer(el1.strip())
    button = InlineKeyboardButton(text='✨C проблемами можете написать нашему меннеджеру✨', callback_data='money')
    await message.message.answer('🤝Поддержка🤝', reply_markup=InlineKeyboardMarkup(inline_keyboard=[[button]]))
    await message.message.answer('Если нужно начать заново: "/restart"')
    print(people)


@dp.callback_query(F.data == 'money')
async def hamster(message: Message) -> None:
    await message.message.answer('@Limerigo. Спасибо, что готовы нам продаться')


@dp.callback_query(F.data == 'Нижний Новгород')
@dp.callback_query(F.data == 'Москва')
@dp.callback_query(F.data == 'Питер')
async def road(message: Message) -> None:
    try:
        await message.message.delete()
    except TelegramBadRequest:
        pass
    global people
    members = message.message.chat.id
    try:
        print(people)
        people[members].append(message.data)
    except TelegramBadRequest:
        pass
    count_sity[message.data] += 1
    first = InlineKeyboardButton(text='Дизайн', callback_data='Дизайн')
    second = InlineKeyboardButton(text='Олимпиадное программирование', callback_data='Олимпиадное программирование')
    third = InlineKeyboardButton(text='Робототехника', callback_data='Робототехника')
    button = [[first], [second], [third]]
    await message.message.answer('Кто ты войн', reply_markup=InlineKeyboardMarkup(inline_keyboard=button))


@dp.callback_query(F.data == "Да")
async def city(message: Message) -> None:
    button = [[InlineKeyboardButton(text='Москва', callback_data='Москва')],
              [InlineKeyboardButton(text='Санкт-Петербург', callback_data='Питер')],
              [InlineKeyboardButton(text='Нижний Новгород', callback_data='Нижний Новгород')]]

    await message.message.answer('Выберите город', reply_markup=InlineKeyboardMarkup(inline_keyboard=button))


@dp.message(F.text == 'Гойда')
async def goi(message: Message) -> None:
    await message.reply_sticker(j)


@dp.message(F.photo)
async def rehrehr(message: Message) -> None:
    await message.answer(message.photo[-1].file_id)


def main1():
    num = [[InlineKeyboardButton(text='Начнем!!!', callback_data='Да')]]
    return InlineKeyboardMarkup(inline_keyboard=num)


@dp.message(CommandStart())
@dp.message(F.text == 'Рестарт')
async def command_start_handler(message: types.Message, bot: Bot) -> None:
    members = await bot.get_chat_member(message.chat.id, message.from_user.id)
    global user_ids, flag_restart
    if user_ids == [] or not (message.from_user.id in check) or flag_restart:
        people[members.user.id] = [score, flag_restart, flag]
        await message.answer_video_note(j1)
        await message.answer('Знаешь, обычно за предоставление информации из ролика берут достаточно много капусты 💰, но мы же тут не инфоцыГане, чтОбы так делать :)Если же ты готов начать учиться, то потыкаЙ пару кнопочек снизу. Обещаю, после них ты сможешь наконец-то зАняться Делом.\n Чтобы перезапустить бот введите команду /restart', reply_markup=main1())
        user_ids.append(members.user.id)
        check.append(members.user.id)
        flag_restart = False


@dp.message(Command('restart'))
async def restart(message: Message) -> None:
    global user_ids, flag_restart
    try:
        user_ids.remove(message.from_user.id)
    except TelegramBadRequest:
        pass
    button = KeyboardButton(text='Рестарт')
    flag_restart = True
    ch = message.chat.id
    people.pop(ch)
    await message.answer('Нажми', reply_markup=ReplyKeyboardMarkup(keyboard=[[button]], one_time_keyboard=True))


async def main() -> None:
    bot = Bot(token=Token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())


