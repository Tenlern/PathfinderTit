const main = document.getElementsByTagName('main')[0];
const xhr = new window.XMLHttpRequest();

function clearView() {
  // Очищаем таблицу
  main.innerHTML = '';
  const names = ['Транспорт', 'Отправление', 'Время в пути', 'Прибытие', 'Цена'];
  for (const name of names) {
    const gridHeadElement = document.createElement('div');
    gridHeadElement.setAttribute('class', 'grid_head');
    gridHeadElement.innerText = name;
    main.appendChild(gridHeadElement);
  }
}

function getSearchData() {
  // Формирование JSON запроса
  let searchData = {
    from: '',
    to: '',
    departure: '',
    type: [],
    priority: '',
  };
  document.querySelectorAll('[name=location]').forEach((elem) => {
    if (elem.id === 'departure') searchData[elem.id] = elem.value;
    else searchData[elem.id] = elem.value;
  });
  document.querySelectorAll('[name=transport]').forEach((elem) => {
    if (elem.checked) searchData.type.push(elem.id);
  });
  searchData.priority = document.querySelectorAll('[name=priority]')[0].value;
  searchData = {
    date: searchData.departure,
    type: "plain",
    from: searchData.from.toLowerCase(),
    to: searchData.to.toLowerCase()
  }

  return searchData;
}

function search() {
  // Заправшиваем данные с сервера
  let data = getSearchData();
  //  для тестирования пересадок
  //	let data = {"from":"Москва","to":"Санкт-Петербург","departure":"2018-10-18","type":["plane","train","bus"],"priority":"departure"};
  xhr.open('POST', '../schedule/lazy/double', true);
  xhr.setRequestHeader('Content-Type', 'application/json');
  data = JSON.stringify(data);
  xhr.send(data);
}

function putFlight(obj, inter) {
  // Разбираем структуру рейса и добавляем рейс в таблицу
  const keyOrder = {
    type: '',
    departure: '',
    duration: '',
    arrival: '',
    price: '',
  };
  for (const key in keyOrder) {
    const val = obj[key];
    const el = document.createElement('div');
    el.setAttribute('class', 'row');
    if (key === 'type') {
      const typeRUS = {
        train: 'Поезд',
        plane: 'Самолёт',
        bus: 'Автобус',
      };
      if (inter) {
        el.className += ' row_inter';
      }
      el.className += ' type';
      el.innerText = typeRUS[val];
    } else if (key === 'departure' || key === 'arrival') {
      const date = new Date(val);
      const options = {
        day: 'numeric',
        month: 'short',
        hour: 'numeric',
        minute: 'numeric',
      };
      el.innerText = date.toLocaleString('ru', options);
    } else if (key === 'duration') {
      let date = new Date();
      const offset = date.getTimezoneOffset() * 60000;
      date = new Date(val * 1000 + offset);
      date = `${date.getHours()} ч ${date.getMinutes()} мин`;
      el.innerText = date;
    } else if (key === 'price') {
      el.setAttribute('class', 'price');
      el.innerText = `${val} ₽`;
    } else el.innerText = val;
    main.appendChild(el);
  }
}

function putInterTitle(arr) {
  // Добавление заголовка для интермодальной перевозки
  const el = document.createElement('div');
  el.setAttribute('class', 'row_inter_title');
  let interStations = '';
  if (arr.length > 2) {
    interStations = 'Пересадки в';
  } else {
    interStations = 'Пересадка в';
  }
  for (let i = 1; i < arr.length; i++) {
    const elem = arr[i];
    interStations = `${interStations} ${elem.from}`;
    if (i < arr.length - 1) {
      interStations += ',';
    }
  }
  interStations += ':';
  el.innerText = interStations;
  main.appendChild(el);
}

function putData(arr) {
  // Добавление данных в таблицу
  clearView();
  if (arr.length !== 0) {
    // Если ответ от сервера не пустой
    arr = JSON.parse(arr);
    console.log(arr);
    for (const val of arr) {
      if (val.length !== undefined) {
        // Если не является массивом, тогда не является интермодальой перевозкой
        putInterTitle(val);
        for (const flight of val) {
          putFlight(flight, true);
        }
      } else putFlight(val);
    }
  } else {
    // Если в ответе от сервера ничего нет
    window.alert('Ничего не найдено');
  }
}

// Ставим обработчик cобытия по нажатию мышью на кнопку "Поиск"
document.getElementById('search_button').addEventListener('click', search, true);

// для тестирования пересадок
// document.addEventListener('load', search, true);

xhr.onreadystatechange = () => {
  // Проверяем состояние запроса и числовой код состояния HTTP ответа
  if (xhr.readyState !== 4) return;
  if (xhr.status !== 200) window.alert(`Ошибка подключения: ${xhr.status}: ${xhr.statusText}`);
  else putData(xhr.responseText);
};
