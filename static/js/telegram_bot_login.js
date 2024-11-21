// Дождаться загрузки библиотеки
window.Telegram.WebApp.ready();

    // Получение информации о пользователе
const user = Telegram.WebApp.initDataUnsafe.user;

if (user) {
    console.log(`Имя пользователя: ${user.first_name} ${user.last_name}`);
    console.log(`Юзернейм: ${user.username}`);

        // Отправка данных на сервер
    fetch('/telegram_login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            first_name: user.first_name,
            last_name: user.last_name,
            username: user.username,
        }),
    })
    .then(response => {
        if (response.ok) {
            console.log('Данные успешно отправлены на сервер');
        } else {
            console.error('Ошибка при отправке данных на сервер');
        }
    })
    .catch(error => console.error('Ошибка:', error));
} else {
    console.log("Информация о пользователе недоступна.");
}