package main

import (
    "fmt"
    "io/ioutil"
    "log"
    "net/http"
)

// Обработчик для корневого маршрута "/"
func index(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "text/html") // Указываем, что ответ в формате HTML

    // Чтение содержимого файла index.html
    content, err := ioutil.ReadFile("templates/index.html")
    if err != nil {
        http.Error(w, "Не удалось загрузить страницу", http.StatusInternalServerError)
        return
    }

    // Отправка содержимого файла в ответ
    w.Write(content)

}

func main() {
    // Назначаем обработчик для маршрута "/"
    http.HandleFunc("/", index)

    // Запускаем сервер на порту 8080
    fmt.Println("Сервер запущен на http://localhost:8080")
    err := http.ListenAndServe(":8080", nil)
    if err != nil {
        log.Fatal("Ошибка при запуске сервера: ", err)
    }
}
