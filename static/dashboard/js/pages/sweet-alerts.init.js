!(function (t) {
  "use strict";
  function e() {}
  (e.prototype.init = function () {
    t("#sa-basic").on("click", function () {
      Swal.fire({
        title: "همه میتونن با کامپیوتر کار کن",
        confirmButtonColor: "#5438dc",
      });
    }),
      t("#sa-title").click(function () {
        Swal.fire({
          title: "اینترنت؟",
          text: "هنوز وصلی؟",
          icon: "سوال",
          confirmButtonColor: "#5438dc",
        });
      }),
      t("#sa-success").click(function () {
        Swal.fire({
          title: "چه خوب",
          text: "روی دکمه کلیک کردی",
          icon: "success",
          showCancelButton: !0,
          confirmButtonColor: "#5438dc",
          cancelButtonColor: "#ff3d60",
        });
      }),
      t("#sa-warning").click(function () {
        Swal.fire({
          title: "مطمئنی؟",
          text: "نمیتونی دیگه عوضش کنی",
          icon: "warning",
          showCancelButton: !0,
          confirmButtonColor: "#34c38f",
          cancelButtonColor: "#ff3d60",
          confirmButtonText: "آره، پاک کن!",
        }).then(function (t) {
          t.value &&
            Swal.fire("پاک شد!", "فایلت پاک شد", "success");
        });
      }),
      t("#sa-params").click(function () {
        Swal.fire({
          title: "مطمئنی؟",
          text: "نمیتونی دیگه عوضش کنی",
          icon: "warning",
          showCancelButton: !0,
          confirmButtonText: "آره، پاک کن!",
          cancelButtonText: "نه کنسل کن",
          confirmButtonClass: "btn btn-success mt-2",
          cancelButtonClass: "btn btn-danger ml-2 mt-2",
          buttonsStyling: !1,
        }).then(function (t) {
          t.value
            ? Swal.fire({
                title: "پاک شد!",
                text: "فایلت پاک شد",
                icon: "success",
              })
            : t.dismiss === Swal.DismissReason.cancel &&
              Swal.fire({
                title: "کنسل شد",
                text: "فایلت محفوظه",
                icon: "error",
              });
        });
      }),
      t("#sa-image").click(function () {
        Swal.fire({
          title: "جالبه!",
          text: "مودال با تصویر",
          imageUrl: "assets/images/logo-dark.png",
          imageHeight: 20,
          confirmButtonColor: "#5438dc",
          animation: !1,
        });
      }),
      t("#sa-close").click(function () {
        var t;
        Swal.fire({
          title: "بسته شدن خودکار!",
          html: "من بسته میشم تو <strong></strong> ثانیه دیگه.",
          timer: 2e3,
          onBeforeOpen: function () {
            Swal.showLoading(),
              (t = setInterval(function () {
                Swal.getContent().querySelector(
                  "strong"
                ).textContent = Swal.getTimerLeft();
              }, 100));
          },
          onClose: function () {
            clearInterval(t);
          },
        }).then(function (t) {
          t.dismiss === Swal.DismissReason.timer &&
            console.log("با تایمر بسته شدم");
        });
      }),
      t("#custom-html-alert").click(function () {
        Swal.fire({
          title: "<i>HTML</i> <u>نمونه</u>",
          icon: "info",
          html:
            'میتونی با<b>متن بولد</b>, <a href="//themesdesign.in/">لینک</a> و بقیه چیزای اچ تی ام ال کار کنی',
          showCloseButton: !0,
          showCancelButton: !0,
          confirmButtonClass: "btn btn-success",
          cancelButtonClass: "btn btn-danger ml-1",
          confirmButtonColor: "#47bd9a",
          cancelButtonColor: "#ff3d60",
          confirmButtonText: '<i class="fas fa-thumbs-up mr-1"></i> عالی!',
          cancelButtonText: '<i class="fas fa-thumbs-down"></i>',
        });
      }),
      t("#sa-position").click(function () {
        Swal.fire({
          position: "top-end",
          icon: "success",
          title: "کارت ذخیره شد",
          showConfirmButton: !1,
          timer: 1500,
        });
      }),
      t("#custom-padding-width-alert").click(function () {
        Swal.fire({
          title: "عرض و پدینگ و بکگراند سفارشی.",
          width: 600,
          padding: 100,
          confirmButtonColor: "#5438dc",
          background:
            "#fff url(//subtlepatterns2015.subtlepatterns.netdna-cdn.com/patterns/geometry.png)",
        });
      }),
      t("#ajax-alert").click(function () {
        Swal.fire({
          title: "ایمیل خودتون رو برای یک درخواست اجاکس بزنید",
          input: "email",
          showCancelButton: !0,
          cancelButtonText:"ارسال",
          showLoaderOnConfirm: !0,
          confirmButtonColor: "#5438dc",
          cancelButtonColor: "#ff3d60",
          preConfirm: function (n) {
            return new Promise(function (t, e) {
              setTimeout(function () {
                "taken@example.com" === n
                  ? e("این ایمیل وجود دارد")
                  : t();
              }, 2e3);
            });
          },
          allowOutsideClick: !1,
        }).then(function (t) {
          Swal.fire({
            icon: "success",
            title: "درخواست اجاکس تموم شد",
            html: "ایمیل ثبت شده: " + t,
          });
        });
      }),
      t("#chaining-alert").click(function () {
        Swal.mixin({
          input: "text",
          confirmButtonText: "بعدی &rarr;",
          showCancelButton: !0,
          confirmButtonColor: "#5438dc",
          cancelButtonColor: "#74788d",
          progressSteps: ["1", "2", "3"],
        })
          .queue([
            { title: "سوال1", text: "سوییت آسونه" },
            "سوال2",
            "سوال3",
          ])
          .then(function (t) {
            t.value &&
              Swal.fire({
                title: "تموم شد",
                html:
                  "جوابا: <pre><code>" +
                  JSON.stringify(t.value) +
                  "</code></pre>",
                confirmButtonText: "چه خوووب!",
              });
          });
      }),
      t("#dynamic-alert").click(function () {
        swal
          .queue([
            {
              title: "ای پی تو",
              confirmButtonColor: "#5438dc",
              confirmButtonText: "ای پی مو نمایش بده",
              text: "دریافت با اجاکس",
              showLoaderOnConfirm: !0,
              preConfirm: function () {
                return new Promise(function (e) {
                  t.get("https://api.ipify.org?format=json").done(function (t) {
                    swal.insertQueueStep(t.ip), e();
                  });
                });
              },
            },
          ])
          .catch(swal.noop);
      });
  }),
    (t.SweetAlert = new e()),
    (t.SweetAlert.Constructor = e);
})(window.jQuery),
  (function () {
    "use strict";
    window.jQuery.SweetAlert.init();
  })();
