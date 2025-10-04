# Приложение для продажи недвижимости

## Статус проекта
🚧 MVP (минимально жизнеспособный продукт), в разработке

## Описание
Мобильное приложение для просмотра и поиска объектов недвижимости.

## Технологии
- **Backend:** Python, FastAPI
- **Frontend:** React Native
- **База данных:** PostgreSQL

## Реализованный функционал
✅ Авторизация и регистрация пользователей  
✅ Главная страница с каталогом объявлений  
✅ Детальная информация об объекте (фото-галерея, цена, площадь, адрес)  
✅ Система избранного (добавление/удаление)  
✅ Профиль пользователя с редактированием данных  
✅ Базовая система сообщений и чатов  
🚧 Поиск и фильтрация (в разработке)  

## Структура проекта
├── app/ # Backend (FastAPI)
├── frontend/ # Frontend (React Native)
└── screenshots/ # Screenshots

## Запуск проекта

### Backend
```bash
cd app
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npx expo start
```
## Скриншоты

<p align="center">
  <img src="https://github.com/user-attachments/assets/72d19f5d-82ba-45dd-961a-160b63d059ba" width="250" alt="Экран входа" />
  <img src="https://github.com/user-attachments/assets/3407552f-ef25-4f70-b325-afea79daadcd" width="250" alt="Главная страница" />
  <img src="https://github.com/user-attachments/assets/41b28a68-0690-4b80-93d6-ac96c22f4fa4" width="250" alt="Детали объявления" />
</p>


