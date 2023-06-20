axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

document.addEventListener("DOMContentLoaded", function () {
  var calendarEl = document.getElementById("calendar");

  var calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: "dayGridMonth",

    // 日付をクリック、または範囲を選択したイベント
    selectable: true,
    select: function (info) {
      moment.locale("ja");
      start = moment(info.start).format("YYYY-MM-DD");
      return window.location.replace(start);
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
