# Инструкции по установке и запуску проекта

[//]: # (УСТАНОВКА __ГЛАВНОЙ__ ВЕТКИ!)
[//]: # (TODO: Переписать файл Инструкций по Установке при изменнениях в проекте в devel-ветке)

### Эта инструкция подразумевает, что у Вас установлен рабочие `python` и `pip`!

---

## Установка:

1. Необходимо клонировать репозиторий. В командной строке:
```
git clone https://github.com/cleanfuzz/ultimate-translate ultimate-translate 

cd ultimate-translate
```

2. Для наилучшей совместимости требуется активировать виртуальное окружение. В командной строке:
    - На `Windows` в PowerShell:
       ```
       python -m venv venv
       .\venv\Scripts\activate.ps1
       ```
    - На `*nix` (Linux, Mac OS X и т. д.)
       ```
       python -m venv venv
       source venv/bin/activate
       ```

3. Далее нужно установить зависимости. В командной строке:
```
pip install -r requirements.txt
```

---

## Запуск:
1. В той же рабочей директории: 
```
python main.py '(ВАШИ ФАЙЛЫ ЧЕРЕЗ ПРОБЕЛ), например: ~/files/foo_file_0 foo_file_1 ./foo_file_2'
```
- Полный список опций можно посмотреть следующим образом:
```
python main.py --help
```