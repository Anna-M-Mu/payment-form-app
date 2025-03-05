# Приложение с формой для оплаты

## Описание
В данном приложении можно:
  /item/{id} - посмотреть товар с возможностью перейти к оплате с помощью Stripe Sessions
  /createorder - создать заказ
  /order/{id} - посмотреть заказ c возможностью перейти к оплате с помощью Stripe Sessions или Stripe Payment Intent
  /admin - посмотреть все имеющиеся модели, авторизировавшись

## Установка
1. Клонируйте репозиторий:  
   ```sh
   git clone https://github.com/Anna-M-Mu/payment-form-app.git
   ```
2. Перейдите в каталог проекта:  
   ```sh
   cd payment-form-app
   ```
3. Установите зависимости:  
   ```sh
   pip install -r requirements.txt
   ```

## Использование
Для запуска проекта используйте следующую команду:  
```sh
python manage.py runserver
```

## Развертывание
Если используется Docker, соберите и запустите с помощью:  
```sh
docker-compose up --build
```

## Переменные окружения
Настройте файл `.env` с такими переменными:  
```ini
STRIPE_SECRET_KEY=
STRIPE_PUBLIC_KEY=
DJANGO_SECRET_KEY=
DATABASE_URL=
ALLOWED_HOSTS=
CORS_ALLOWED_ORIGINS=
DEBUG=
```
