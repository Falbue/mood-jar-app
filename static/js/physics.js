// Подключение Matter.js
const { Engine, Render, World, Bodies, Composite, Runner, Mouse, MouseConstraint } = Matter;

// Основная настройка
const container = document.getElementById('container');
const containerWidth = container.clientWidth;
const containerHeight = container.clientHeight;

// Создание физического движка
const engine = Engine.create();
const world = engine.world;

// Настройка рендера
const render = Render.create({
  element: container,
  engine: engine,
  options: {
    width: containerWidth,
    height: containerHeight,
    wireframes: false, // Включение полноцветного отображения
    background: 'transparent',
  },
});

// Границы контейнера
const width_wall = 60;
const walls = [
  Bodies.rectangle(containerWidth / 2, 0, containerWidth, width_wall, {
    isStatic: true,
    render: {
      fillStyle: 'rgba(255, 255, 255, 0)', // Полупрозрачный белый цвет
      strokeStyle: 'rgba(255, 255, 255, 0)',  // Убираем обводку
    },
  }), // Верхняя граница
  Bodies.rectangle(containerWidth / 2, containerHeight, containerWidth, width_wall, {
    isStatic: true,
    render: {
      fillStyle: 'rgba(255, 255, 255, 0)',
      strokeStyle: 'rgba(255, 255, 255, 0)',
    },
  }), // Нижняя граница
  Bodies.rectangle(0, containerHeight / 2, width_wall, containerHeight, {
    isStatic: true,
    render: {
      fillStyle: 'rgba(255, 255, 255, 0)',
      strokeStyle: 'rgba(255, 255, 255, 0)',
    },
  }), // Левая граница
  Bodies.rectangle(containerWidth, containerHeight / 2, width_wall, containerHeight, {
    isStatic: true,
    render: {
      fillStyle: 'rgba(255, 255, 255, 0)',
      strokeStyle: 'rgba(255, 255, 255, 0)',
    },
  }), // Правая граница
];
World.add(world, walls);

// Настройка шариков
const ballOptions = {
  restitution: 0.4, // Упругость
  friction: 0.05, // Трение
};

let emojiList = []; // Массив для эмодзи

fetch('http://192.168.0.110:80/get_mood_data')
  .then(response => response.json())
  .then(data => {
    if (data.error) {
        console.log("No data for today");
    } else {
        console.log("Полученные данные:", data); // Здесь проверим структуру
        emojiList = Object.values(data).map(item => item.mood); // Заполняем массив
        console.log("Все эмодзи настроений:", emojiList);

        // После того как массив заполнен, создаем шарики
        let balls = []; // Массив для хранения шариков

        // Используем длину emojiList для создания нужного количества шариков
        emojiList.forEach((emoji, index) => {
          const radius = 20; // Радиус шарика
          const ball = Bodies.circle(
            Math.random() * (containerWidth - 2 * radius) + radius,
            Math.random() * (containerHeight - 2 * radius) + radius,
            radius,
            {
              ...ballOptions,
              render: {
                sprite: {
                  texture: `data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="${radius * 2}" height="${radius * 2}" viewBox="0 0 ${radius*1.16} ${radius}"><text x="50%" y="50%" font-size="${radius}" text-anchor="middle" dominant-baseline="central">${emoji}</text></svg>`,
                },
              },
            }
          );
          World.add(world, ball);
          balls.push(ball);
        });

        // Добавляем взаимодействие с мышью (клики)
        const mouse = Mouse.create(render.canvas);
        const mouseConstraint = MouseConstraint.create(engine, {
          mouse: mouse,
          constraint: {
            stiffness: 0.2,
            render: {
              visible: false,
            },
          },
        });
        World.add(world, mouseConstraint);

        // Слушаем клик по шарикам
        Matter.Events.on(mouseConstraint, 'mousedown', (event) => {
          const mousePosition = event.mouse.position;

          // Проверяем, был ли клик по одному из шариков
          balls.forEach((ball) => {
            if (Matter.Bounds.contains(ball.bounds, mousePosition)) {
              console.log("Нажатие на эмодзи");
            }
          });
        });

        // Запуск рендера и движка
        Render.run(render);
        const runner = Runner.create();
        Runner.run(runner, engine);
    }
  })
  .catch(error => console.error('Error fetching mood data:', error));

// Динамическое обновление размеров контейнера
window.addEventListener('resize', () => {
  const newWidth = container.clientWidth;
  const newHeight = container.clientHeight;

  render.bounds.max.x = newWidth;
  render.bounds.max.y = newHeight;
  render.options.width = newWidth;
  render.options.height = newHeight;

  Render.stop(render);
  Render.run(render);
});
