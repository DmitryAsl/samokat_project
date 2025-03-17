<h2 align="center"> Тестовый проект UI автотестов на сайт samokat.ru</h2>  


### Используемый стек
<p>
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original-wordmark.svg" height=50 weight=50 />  
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/pytest/pytest-original-wordmark.svg" height=50 weight=50 />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/jenkins/jenkins-original.svg" height=50 weight=50 />
  <img src="https://github.com/DmitryAsl/samokat_project/blob/master/data/pictures/selenoid.svg" height=50 weight=50 />
  <img src="https://avatars.githubusercontent.com/u/5879127?s=200&v=4" height=50 weight=50 />
  <img src="https://github.com/DmitryAsl/samokat_project/blob/master/data/pictures/Telegram.svg" height=50 weight=50 />
</p>        

### Автоматизированные кейсы
1. Выбор адреса доставки
2. Поиск товара
3. Поиск несуществующего товара
4. Добавление товара в корзину
5. Удаление товара из корзины
6. Корректность расчета стоимости корзины
7. Увеличение количества конкретного товара в корзине

<details>
<summary><h3> Запуск тестов с помощью Jenkins </h3><img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/jenkins/jenkins-original.svg" height=30 weight=30 /></summary> 

  > **Перейти в [сборку](https://jenkins.autotests.cloud/job/dmitry_asl_samokat_web_project/)**  
  > **Перейти на вкладку "Build with Parameters"** 
  <p>
  <img src="https://github.com/DmitryAsl/samokat_project/blob/master/data/pictures/jenkins_build_param.png" />
  </p>  
  
  > **Выбрать параметры из выпадающих списков и нажать "Build"**
  <img src="https://github.com/DmitryAsl/samokat_project/blob/master/data/pictures/build_jenkins.jpg" />
  
  > Результаты запуска находятся в левом углу, последний запуск
  <img src="https://github.com/DmitryAsl/samokat_project/blob/master/data/pictures/check_build.jpg" />
</details>
<details>
<summary><h3> Запуск тестов локально </h3></summary>  
  
  1. Склонировать репозиторий
  2. Открыть проект в PyCharm
  3. Ввести в терминале следующие команды
     - если Poetry ещё **не установлен**, сначала установите его:  
    ```
    pip install poetry  
    ```
  > Основные команды по настройке проекта и запуска тестов  
  ```
  poetry install --no-root
  poetry shell
  pytest tests
  ```
> Для передачи других параметров запуска тестов: в корне проекта нужно создать файл .env и указать в нем нужные параметры (например браузер или расширение экрана)  
> Для запуска тестов удаленно в .env файл нужно добавить login и password от среды запуска qa_guru 

**Если локально установлен Allure можно посмотреть отчет, для этого выполняем**
  ```
  allure serve allure-results
  ```

</details>

### Отчет о результатах в Allure <img src="https://avatars.githubusercontent.com/u/5879127?s=200&v=4" height=30 weight=30 />
> В качестве системы отчетности выбран **Allure Report**  
> Для перехода в отчет, в Jenkins в левом углу нажать на иконку на Вашем запуске  
  <img src="https://github.com/DmitryAsl/samokat_project/blob/master/data/pictures/check_build.jpg" />
  
> В открывшемся окне представлена общая информация по тестам  
>> Для подробной информации переходим на вкладку **Behaviors** и раскрываем все тесты для наглядности  
>>> При нажатии на конкретный тест справа отображается подробная информация по нему  
 <img src="https://github.com/DmitryAsl/samokat_project/blob/master/data/pictures/allure_behaniors_info.png" />

### Отправка оповещения прохождения тестов в Telegram <img src="https://github.com/DmitryAsl/qa_guru_hw_14_Samokat/blob/main/data/icons/Telegram.svg" height=30 weight=30 />

> Автоматически настроена отправка оповещения о результатах прохождения тестов в чат **Telegram** с тегом ответственных людей.  
> В оповещении присутствует общая информация о запуске и ссылка на отчет в **Allure**.  
<img src="https://github.com/DmitryAsl/samokat_project/blob/master/data/pictures/notifications_tg.png" />

### Демонстрация прохождения одного из тестов
> Выбор адреса доставки

![](https://github.com/DmitryAsl/samokat_project/blob/master/data/pictures/address_test.gif)


#### Для вопросов и предложений можно связаться в [telegram](https://t.me/Dmitry_Asl) 

