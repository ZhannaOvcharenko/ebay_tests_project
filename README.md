# Проект по тестированию онлайн-площадки по продаже и покупке товаров "eBay"
> <a target="_blank" href="https://ebay.com/">ebay.com</a>

![main page screenshot](/files/ebay.com.png)

----

### Особенности проекта

* WEB UI и API тесты
* Запуск WEB UI автотестов удаленно в Selenoid либо локально
* Сборка проекта в Jenkins
* Отчеты о запусках тестовых прогонов (интеграция с Allure TestOps)
* Привязка тестовых прогонов и тест-кейсов к задачам (интеграция с Jira)
* Оповещения о тестовых прогонах в Telegram

----

### Проект реализован с использованием:

<img title="Python" src="/files/icons/python-original.svg" height="40" width="40"/> <img title="Pytest" src="/files/icons/pytest-original.svg" height="40" width="40"/> <img title="Selenium" src="/files/icons/selenium-original.svg" height="40" width="40"/> <img title="Selene" src="/files/icons/selene.png" height="40" width="40"/> <img title="Requests" src="/files/icons/requests.png" height="40" width="40"/> <img title="Selenoid" src="/files/icons/selenoid.png" height="40" width="40"/> <img title="GitHub" src="/files/icons/github-original.svg" height="40" width="40"/>  <img title="Jenkins" src="/files/icons/jenkins-original.svg" height="40" width="40"/> <img title="Pycharm" src="/files/icons/pycharm.png" height="40" width="40"/> <img title="Allure Report" src="/files/icons/Allure_Report.png" height="40" width="40"/>  <img title="Allure TestOps" src="/files/icons/allure_testops.png" height="40" width="40"/> <img title="Jira" src="/files/icons/jira.png" height="40" width="40"/> <img title="Telegram" src="/files/icons/tg.png" height="40" width="40"/> 


----

### Локальный запуск автотестов

#### Для запуска Web UI автотестов выполнить в cli:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest tests/web
```

#### Для запуска API автотестов выполнить в cli:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest tests/api
```

#### Получение отчёта:
```bash
allure serve tests/allure-results
```

----

### Проект в Jenkins
> <a target="_blank" href="https://jenkins.autotests.cloud/job/ebay_tests_project_ZhannaOvcharenko/">Ссылка</a>

#### Параметры сборки
> [!NOTE]
> Параметры сборки не обязательны
```python
ENVIRONMENT = ['STAGE', 'PREPROD', 'PROD'] # Окружение
COMMENT = 'some comment' # Комментарий, в котором можно указать аккаунт в tg для уведомления об отчете
```
#### Запуск автотестов в Jenkins
1. Открыть <a target="_blank" href="https://jenkins.autotests.cloud/job/ebay_tests_project_ZhannaOvcharenko/">проект</a>
2. Нажать "Build with Parameters"
3. Из списка "ENVIRONMENT" выбрать любое окружение
4. В поле "COMMENT" ввести комментарий
5. Нажать "Build"

![jenkins project main page](/files/jenkins_project.png)

----

### Отчет в Allure TestOps
#### <a target="_blank" href="https://allure.autotests.cloud/launch/48174">Результаты прогона</a>
![allure_report_overview](/files/Allure%20TestOPS.png)

----

### Оповещения в Telegram
![telegram_allert](/files/telegram_allert.png)

----

### Видео прохождения web/UI автотеста
![autotest_gif](/files/autotest.gif)
