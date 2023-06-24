axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function post(path, params, method = "post") {
  // The rest of this code assumes you are not using a library.
  // It can be made less wordy if you use one.
  let form = document.createElement("form");
  form.method = method;
  form.action = path;

  let csrf_element = document.createElement("input");
  csrf_element.type = "text";
  csrf_element.name = "csrfmiddlewaretoken";
  csrf_element.value = [getCookie("csrftoken")];

  form.appendChild(csrf_element);

  for (const key in params) {
    if (params.hasOwnProperty(key)) {
      const hiddenField = document.createElement("input");
      hiddenField.type = "hidden";
      hiddenField.name = key;
      hiddenField.value = params[key];

      form.appendChild(hiddenField);
    }
  }

  document.body.appendChild(form);
  form.submit();
}

document.addEventListener("DOMContentLoaded", function () {
  var calendarEl = document.getElementById("calendar");

  var calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: "dayGridMonth",

    // 日付をクリック、または範囲を選択したイベント
    selectable: true,
    select: function (info) {
      moment.locale("ja");
      path = moment(info.start).format("YYYY-MM-DD/");
      start = moment(info.start).format("YYYY-MM-DD");
      //return window.location.replace(start);
      post(path, { start: start, deadline: start });
    },

    eventClick: function (info, successCallback) {
      post(
        "/application/target_update/",
        {
          start: info.event.start.valueOf(),
          title: info.event.title,
        },
        (method = "get")
      );
    },

    events: function (info, successCallback, failureCallback) {
      axios
        .post("/application/target_get/", {
          start_date: info.start.valueOf(),
          end_date: info.end.valueOf(),
        })
        .then((response) => {
          calendar.removeAllEvents();
          successCallback(response.data);
        })
        .catch(() => {
          // バリデーションエラーなど
          alert("登録に失敗しました");
        });
    },
  });

  calendar.render();
});
