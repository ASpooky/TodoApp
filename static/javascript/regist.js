axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

document.addEventListener("DOMContentLoaded", function () {
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
});
