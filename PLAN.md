# CVS Contracting — Launch Plan

## Контекст: что Google уже знает о домене

Домен был **CVS Foundations & Excavation, Saco, Maine**.

Google ассоциирует домен с:
- Foundation work
- Excavation
- **Saco, ME** и Southern Maine

Это активы. Начинать нужно там, где у домена уже есть авторитет — усилить, а не воевать с нуля.

---

## Услуги: в каком порядке запускать

| Порядок | Услуга | Почему |
|---------|--------|--------|
| **1** | `foundation-repair` | Буквально в истории домена ("CVS Foundations"). Google уже ассоциирует. |
| **2** | `excavation-contractors` | Тоже в истории ("& Excavation"). Лёгкий старт. |
| **3** | `basement-waterproofing` | Смежно с фундаментом, тот же покупатель, высокий lead value. |
| **4** | `snow-removal` | Другой кластер, но Northeast-специфично. Запускать после первых трёх. |

**Не запускать в Phase 1:**
- `concrete-contractors` — слишком широко, конкуренция огромная без авторитета
- `french-drain-installation` — нишевый, но разбавляет фокус слишком рано
- `septic-system` — другая тематика (waste vs. structural), только Phase 2

**Почему этот порядок органичен для Google:**
Строим "topical cluster" постепенно. Все 4 сразу — Google видит разброс. Foundation → excavation → waterproofing с разницей 2 недели — Google видит нарастающую экспертизу.

---

## Города: geographic cluster, не scatter

320 city pages без трафика и без ссылок = Google помечает как thin programmatic content.

```
НЕ ТАК:                          ТАК:
Portland ME                      Portland ME (anchor)
Manchester NH           -->      South Portland ME
Burlington VT                    Westbrook ME
Concord NH                       Scarborough ME
Augusta ME                       Biddeford ME
Nashua NH                        Saco ME  <-- домашний город домена!
...по 1 странице                 ...15-20 страниц одного кластера
```

Google видит 15 страниц про "foundation repair" в Portland metro → присваивает тематический авторитет на весь регион.

---

## Волна 1 (неделя 1-2): Southern Maine кластер

Запускать для `foundation-repair` + `excavation-contractors`:

| Город | Округ | Population | Почему важен |
|-------|-------|-----------|--------------|
| Portland | Cumberland | 68k | Главный якорь Maine |
| Lewiston | Androscoggin | 38k | Второй по размеру |
| Bangor | Penobscot | 32k | Якорь Central Maine |
| South Portland | Cumberland | 26k | Portland metro |
| Auburn | Androscoggin | 25k | Пара с Lewiston |
| Biddeford | York | 22k | Domain's backyard |
| **Saco** | York | 20k | **Домашний город домена** |
| Westbrook | Cumberland | 19k | Portland metro |
| Windham | Cumberland | 19k | Portland suburb |
| Gorham | Cumberland | 17k | Portland suburb |
| Brunswick | Cumberland | 21k | Mid-coast anchor |
| Scarborough | Cumberland | 22k | Portland metro |
| Augusta | Kennebec | 19k | State capital |
| Sanford | York | 21k | Southern Maine |
| Old Orchard Beach | York | 10k | Tourist/coastal |

15 городов × 2 услуги = **30 страниц**. Все в Cumberland + York County — монолитный кластер.

---

## Волна 2 (неделя 3-4): +basement-waterproofing

Не новые города — новая услуга на уже индексируемые 15 городов.
30 страниц → **45 страниц**.

---

## Волна 3 (неделя 5-6): New Hampshire

Запускать только после первых импрессий в GSC по Maine страницам.

| Город | Population | Почему |
|-------|-----------|--------|
| Manchester | 115k | Самый крупный в NH |
| Nashua | 89k | Второй |
| Concord | 43k | Столица |
| Dover | 32k | Seacoast |
| Portsmouth | 22k | High-income, много старых домов |
| Rochester | 32k | Central NH |
| Laconia | 17k | Lakes Region |
| Keene | 23k | Southwest NH |
| Derry | 34k | Manchester suburb |
| Londonderry | 26k | Manchester suburb |

10 городов × 3 услуги (foundation + excavation + waterproofing) = **30 страниц**.

---

## Волна 4 (неделя 7-8): snow-removal на все города

Snow removal запускать последним — отдельный поисковый кластер. Если запустить раньше, Google будет колебаться между "сайт про фундаменты" и "сайт про уборку снега".

25 городов × 1 услуга = **25 страниц**.

**Итого после 8 недель: ~130 страниц** с реальными данными, вместо 320 пустых.

---

## Почему Saco ME — приоритет #1

Оригинальный бизнес работал из Saco. Это значит:
- Старые ссылки с Yelp, BBB, Yellow Pages указывают именно туда
- Google локально "помнит" этот домен в Saco

Страница `foundation-repair/saco-me` может начать ранжироваться за **2-4 недели**, пока другие города будут ждать месяцами.

---

## Блог: публиковать постепенно

8 постов за один день = сигнал content farm.

| Неделя | Действие |
|--------|----------|
| 1-2 | Запуск city pages (foundation + excavation, Maine) |
| 3 | Пост #1: Foundation Repair Cost |
| 4 | Добавить basement-waterproofing страницы |
| 5 | Пост #2: Excavation Cost in Maine and NH |
| 6 | NH expansion |
| 7 | Пост #3: Signs of Foundation Problems |
| 8 | Snow removal страницы + Пост #4: Snow Removal Cost |
| 9 | Пост #5: How to Choose a Foundation Contractor |
| 10 | Пост #6: Snow Removal Contract vs Per-Visit in New England |
| 11 | Пост #7: Basement Waterproofing Contractors in Maine |
| 12 | Пост #8: Basement Waterproofing Cost Guide |

---

## Outscraper: что парсить в первую очередь

Не весь Northeast сразу. Купить только:
- **Cumberland County ME** (Portland metro)
- **York County ME** (Saco, Biddeford)
- **Androscoggin County ME** (Lewiston, Auburn)
- **Penobscot County ME** (Bangor)

Сервисы: `foundation-repair` + `excavation-contractors` только.

Это будет дешевле ($10-15) и даст чистый датасет для старта. NH и остальные услуги — вторым заказом после того как первая волна запущена.

---

## Checklist: что сделать ДО написания кода

- [ ] Зарегистрироваться в Angi Ads Partner (1-2 недели одобрение — start NOW)
- [ ] Зарегистрироваться в HomeAdvisor affiliate
- [ ] Зарегистрироваться в Thumbtack Pro
- [ ] Купить Outscraper: Cumberland + York + Androscoggin + Penobscot County ME, foundation + excavation
- [ ] Убедиться что Saco ME есть в данных с 3+ компаниями
