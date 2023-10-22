# `ultimate-translate` - Мгновенный переводчик файла локали
***(почти мгновенный) перевод YAML-файла в Google, Alibaba, DeepL и т.д.***

___

### Данный проект предназначен специально для перевода файла локалей на русский.

__Но также этот скрипт умеет переводить и с [`lang_list`](https://github.com/UlionTse/translators#supported-languages), и на [`lang_list`](https://github.com/UlionTse/translators#supported-languages).__

_* (Ссылка на поддерживаемые языки - [lang_list](https://github.com/UlionTse/translators#supported-languages))_

В частности, локалей Telegram-бота для создания опросов (их GitHub):
__[ultimate-poll-bot (README)](https://github.com/Nukesor/ultimate-poll-bot/blob/main/README.md)__

---

### Перевод осуществляется с помощью библиотеки [`translators`](https://github.com/UlionTse/translators) 
__[Ссылка на библиотеку translators.](https://github.com/UlionTse/translators)__

Но никто не запрещает Вам адаптировать данный проект для:
- собственного использования на других форматах файлов
- другой библиотеки для перевода
- другого проекта в качестве модуля...

___

_Примечание: функция перевода через API Yandex.Translate_
_`trans.translate_text(query_text='foobar', translator='yandex')`
(расширяется в `translators_fix.server.translate_text()`) может не работать._ 😟

[Подробнее про API Yandex.Translate](https://translate.yandex.net/api/v1/tr.json/translate) - ссылка на страницу устаревшего бесплатного API.

---

## Ссылки:
- __[ARCHITECTURE.md](./ARCHITECTURE.md)__ - архитектура проекта и назначение модулей
- __[INSTALL.md](./INSTALL.md)__ - инструкции по установке и запуску проекта
