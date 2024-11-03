        // const tg = window.Telegram.WebApp;

        // // Инициализация приложения
        // tg.ready();

        // // Настройка главной кнопки
        // tg.MainButton.show();
        // tg.MainButton.setText("Закрыть");

        // // Обработка события нажатия на кнопку
        // tg.MainButton.onClick(() => {
        //     console.log("Кнопка нажата, закрытие приложения...");
        //     tg.close(); // Закрыть приложение
        // });


const { WebApp, Utils } = window.Telegram;
const { MainButton, SecondaryButton, SettingsButton, HapticFeedback, CloudStorage, BiometricManager } = WebApp;

MainButton.text = "Закрыть";
MainButton.show();
MainButton.onClick(() => {
    Telegram.WebApp.close();
});

// Initialize and show Secondary Button
SecondaryButton.text = "Cancel";
SecondaryButton.show();
SecondaryButton.onClick(() => {
    alert("Secondary Button Clicked!");
});

// Show Settings Button and handle click
SettingsButton.show();
SettingsButton.onClick(() => {
    alert("Settings Button Clicked!");
});

// Trigger Haptic Feedback on button click
document.getElementById("hapticFeedback").addEventListener("click", () => {
    HapticFeedback.impactOccurred("medium");
    alert("Haptic Feedback Triggered!");
});

// Example use of Cloud Storage
CloudStorage.setItem("testKey", "testValue", (err) => {
    if (err) console.error("Error saving to CloudStorage", err);
    else alert("Data saved in CloudStorage!");
});

// Initialize and check Biometric Manager
BiometricManager.init(() => {
    if (BiometricManager.isBiometricAvailable) {
        document.getElementById("biometricButton").addEventListener("click", () => {
            BiometricManager.requestAccess({ reason: "Security Check" }, (granted) => {
                alert(granted ? "Access Granted!" : "Access Denied");
            });
        });
    } else {
        alert("Biometric Authentication Not Available");
    }
});

// Theme and color scheme settings
document.body.style.backgroundColor = WebApp.backgroundColor || "#ffffff";
WebApp.onEvent("themeChanged", () => {
    document.body.style.backgroundColor = WebApp.themeParams.bg_color || "#ffffff";
});