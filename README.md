# Проект по тестированию онлайн-площадки по продаже и покупке товаров "eBay"
> <a target="_blank" href="https://ebay.com/">ebay.com</a>

![main page screenshot](/files/ebay.com.png)

----

### Особенности проекта

* Оповещения о тестовых прогонах в Telegram
* Отчеты с видео, скриншотом, логами, исходной моделью разметки страницы
* Сборка проекта в Jenkins
* Отчеты Allure Report
* Запуск web/UI автотестов в Selenoid

### Список проверок, реализованных в web/UI автотестах

- [x] Проверка видимости популярных блоков на главной странице
- [x] Проверка фильтров для Cameras
- [x] Проверка фильтров для Laptops
- [x] Проверка фильтров для Smartphones
- [x] Проверка фильтров для Tablets
- [x] Проверка диалогового для Watches

----

### Используемый стэк

<img title="Python" src="/files/icons/python-original.svg" height="40" width="40"/> <img title="Pytest" src="/files/icons/pytest-original.svg" height="40" width="40"/> <img title="Allure Report" src="/files/icons/Allure_Report.png" height="40" width="40"/> <img title="GitHub" src="/files/icons/github-original.svg" height="40" width="40"/> <img title="Selenoid" src="/files/icons/selenoid.png" height="40" width="40"/> <img title="Selenium" src="/files/icons/selenium-original.svg" height="40" width="40"/> <img title="Selene" src="/files/icons/selene.png" height="40" width="40"/> <img title="Pycharm" src="/files/icons/pycharm.png" height="40" width="40"/> <img title="Telegram" src="/files/icons/tg.png" height="40" width="40"/> <img title="Jenkins" src="/files/icons/jenkins-original.svg" height="40" width="40"/>

----

### Локальный запуск автотестов

#### Для запуска web/UI автотестов выполнить в cli:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest .
```

#### Получение отчёта:
```bash
allure serve tests/allure-results
```

----

### Проект в Jenkins
> <a target="_blank" href="https://jenkins.autotests.cloud/job/ZhannaOvcharenko_qa_guru_python_14/">Ссылка</a>

#### Параметры сборки
> [!NOTE]
> Параметры сборки не обязательны
```python
ENVIRONMENT = ['STAGE', 'PREPROD', 'PROD'] # Окружение
COMMENT = 'some comment' # Комментарий, в котором можно указать аккаунт в tg для уведомления об отчете
```
#### Запуск автотестов в Jenkins
1. Открыть <a target="_blank" href="https://jenkins.autotests.cloud/job/ZhannaOvcharenko_qa_guru_python_14/">проект</a>
2. Нажать "Build with Parameters"
3. Из списка "ENVIRONMENT" выбрать любое окружение
4. В поле "COMMENT" ввести комментарий
5. Нажать "Build"

![jenkins project main page](/files/jenkins_project.png)

----

### Allure отчет
#### <a target="_blank" href="https://jenkins.autotests.cloud/job/ZhannaOvcharenko_qa_guru_python_14/1/allure/">Общие результаты</a>
![allure_report_overview](/files/allure_report_overview.png)

#### <a target="_blank" href="https://jenkins.autotests.cloud/job/qa_guru_python_20_14_kyarygina/16/allure/#suites">Результаты прохождения теста</a>

![allure_reports_suites](/files/allure_report_suites.png)

#### <a target="_blank" href="https://jenkins.autotests.cloud/job/qa_guru_python_20_14_kyarygina/16/allure/#suites">Приложенные к кейсу логи, видео, скриншоты</a>


![allure_reports_attach](/files/allure_report_attach.png)

----

### Оповещения в Telegram
![telegram_allert](/files/telegram_allert.png)

----

### Видео прохождения web/UI автотеста
![autotest_gif](/files/autotest.gif)
