package main

import (
    "html/template"
    "log"
    "net/http"
)

func main() {
    // Обработка статических файлов
    http.Handle("/static/", http.StripPrefix("/static/", http.FileServer(http.Dir("./static"))))

    http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
        tmpl, err := template.ParseFiles("templates/index.html")
        if err != nil {
            http.Error(w, err.Error(), http.StatusInternalServerError)
            return
        }
        // Передаем nil, если данные для шаблона не используются
        if err := tmpl.Execute(w, nil); err != nil {
            http.Error(w, err.Error(), http.StatusInternalServerError)
        }
    })

    // Запуск веб-сервера
    log.Println("Сервер запущен")
    log.Fatal(http.ListenAndServe(":80", nil))
}
