package main

import (
    "database/sql"
    "html/template"
    "log"
    "net/http"
    _ "github.com/mattn/go-sqlite3" // Импортируем драйвер SQLite
)

// Структура для пользователя
type User struct {
    ID       int    `json:"id"`
    Username string `json:"username"`
}

// Функция для получения пользователей из базы данных
func getUsers(db *sql.DB) ([]User, error) {
    // SQL-запрос для получения id и username всех пользователей
    query := "SELECT id, username FROM users"

    // Выполнение запроса
    rows, err := db.Query(query)
    if err != nil {
        return nil, err
    }
    defer rows.Close()

    var users []User
    // Чтение строк из результата запроса
    for rows.Next() {
        var user User
        err := rows.Scan(&user.ID, &user.Username)
        if err != nil {
            return nil, err
        }
        users = append(users, user)
    }

    // Проверка на ошибки при обходе строк
    if err := rows.Err(); err != nil {
        return nil, err
    }

    return users, nil
}

func main() {
    // Подключение к базе данных SQLite
    db, err := sql.Open("sqlite3", "../../db_hub/mood_jar.db")
    if err != nil {
        log.Fatal(err)
    }
    defer db.Close()

    // Обработка маршрута для главной страницы
    http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
        // Получаем пользователей из базы данных
        users, err := getUsers(db)
        if err != nil {
            http.Error(w, err.Error(), http.StatusInternalServerError)
            return
        }

        // Загружаем HTML-шаблон
        tmpl, err := template.ParseFiles("templates/index.html")
        if err != nil {
            http.Error(w, err.Error(), http.StatusInternalServerError)
            return
        }

        // Передаем данные пользователей в шаблон и выводим результат
        tmpl.Execute(w, users)
    })

    // Запуск веб-сервера
    log.Println("Сервер запущен")
    log.Fatal(http.ListenAndServe(":80", nil))
}
