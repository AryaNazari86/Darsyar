var options = {
    chart: {
      height: 380,
      type: "line",
      zoom: { enabled: !1 },
      toolbar: { show: !1 },
    },
    colors: ["#5664d2", "#1cbb8c"],
    dataLabels: { enabled: !0 },
    stroke: { width: [3, 3], curve: "straight" },
    series: [
      { name: "بالا - 1398", data: [26, 24, 32, 36, 33, 31, 33] },
      { name: "پایین - 1399", data: [14, 11, 16, 12, 17, 13, 12] },
    ],
    title: { text: "میانگین بالاترین و پایین ترین دما", align: "left" },
    grid: {
      row: { colors: ["transparent", "transparent"], opacity: 0.2 },
      borderColor: "#f1f1f1",
    },
    markers: { style: "inverted", size: 6 },
    xaxis: {
      categories: ["مهر", "آبان", "آذر", "دی", "بهمن", "اسفند", "فروردین"],
      title: { text: "ماه" },
    },
    yaxis: { title: { text: "دما" }, min: 5, max: 40 },
    legend: {
      position: "top",
      horizontalAlign: "right",
      floating: !0,
      offsetY: -25,
      offsetX: -5,
    },
    responsive: [
      {
        breakpoint: 600,
        options: { chart: { toolbar: { show: !1 } }, legend: { show: !1 } },
      },
    ],
  },
  chart = new ApexCharts(
    document.querySelector("#line_chart_datalabel"),
    options
  );
chart.render();
options = {
  chart: {
    height: 380,
    type: "line",
    zoom: { enabled: !1 },
    toolbar: { show: !1 },
  },
  colors: ["#5664d2", "#fcb92c", "#1cbb8c"],
  dataLabels: { enabled: !1 },
  stroke: { width: [3, 4, 3], curve: "straight", dashArray: [0, 8, 5] },
  series: [
    {
      name: "مدت سشن",
      data: [45, 52, 38, 24, 33, 26, 21, 20, 6, 8, 15, 10],
    },
    {
      name: "بازدید صفحه",
      data: [36, 42, 60, 42, 13, 18, 29, 37, 36, 51, 32, 35],
    },
    {
      name: "بازدید کل",
      data: [89, 56, 74, 98, 72, 38, 64, 46, 84, 58, 46, 49],
    },
  ],
  title: { text: "آمار", align: "left" },
  markers: { size: 0, hover: { sizeOffset: 6 } },
  xaxis: {
    categories: [
      "01 مهر",
      "02 مهر",
      "03 مهر",
      "04 مهر",
      "05 مهر",
      "06 مهر",
      "07 مهر",
      "08 مهر",
      "09 مهر",
      "10 مهر",
      "11 مهر",
      "12 مهر",
    ],
  },
  tooltip: {
    y: [
      {
        title: {
          formatter: function (e) {
            return e + " (دقیقه)";
          },
        },
      },
      {
        title: {
          formatter: function (e) {
            return e + " بر سشن";
          },
        },
      },
      {
        title: {
          formatter: function (e) {
            return e;
          },
        },
      },
    ],
  },
  grid: { borderColor: "#f1f1f1", padding: { bottom: 5 } },
  legend: { offsetY: 5 },
};
(chart = new ApexCharts(
  document.querySelector("#line_chart_dashed"),
  options
)).render();
options = {
  chart: { height: 350, type: "area" },
  dataLabels: { enabled: !1 },
  stroke: { curve: "smooth", width: 3 },
  series: [
    { name: "سری1", data: [34, 40, 28, 52, 42, 109, 100] },
    { name: "سری2", data: [32, 60, 34, 46, 34, 52, 41] },
  ],
  colors: ["#5664d2", "#1cbb8c"],
  xaxis: {
    type: "datetime",
    categories: [
      "2018-09-19T00:00:00",
      "2018-09-19T01:30:00",
      "2018-09-19T02:30:00",
      "2018-09-19T03:30:00",
      "2018-09-19T04:30:00",
      "2018-09-19T05:30:00",
      "2018-09-19T06:30:00",
    ],
  },
  grid: { borderColor: "#f1f1f1", padding: { bottom: 15 } },
  tooltip: { x: { format: "dd/MM/yy HH:mm" } },
  legend: { offsetY: 7 },
};
(chart = new ApexCharts(
  document.querySelector("#spline_area"),
  options
)).render();
options = {
  chart: { height: 350, type: "bar", toolbar: { show: !1 } },
  plotOptions: {
    bar: { horizontal: !1, columnWidth: "45%", endingShape: "rounded" },
  },
  dataLabels: { enabled: !1 },
  stroke: { show: !0, width: 2, colors: ["transparent"] },
  series: [
    { name: "بدون سود", data: [46, 57, 59, 54, 62, 58, 64, 60, 66] },
    { name: "برگشت", data: [74, 83, 102, 97, 86, 106, 93, 114, 94] },
    { name: "سود جاری", data: [37, 42, 38, 26, 47, 50, 54, 55, 43] },
  ],
  colors: ["#5664d2", "#1cbb8c", "#fcb92c"],
  xaxis: {
    categories: ["آبان", "آذر", "دی", "بهمن", "اسفند", "فروردین", "اردیبهشت", "خرداد", "تیر"],
  },
  yaxis: { title: { text: " (تومان)" } },
  grid: { borderColor: "#f1f1f1", padding: { bottom: 10 } },
  fill: { opacity: 1 },
  tooltip: {
    y: {
      formatter: function (e) {
        return " " + e + " تومان";
      },
    },
  },
  legend: { offsetY: 7 },
};
(chart = new ApexCharts(
  document.querySelector("#column_chart"),
  options
)).render();
options = {
  chart: { height: 350, type: "bar", toolbar: { show: !1 } },
  plotOptions: { bar: { dataLabels: { position: "top" } } },
  dataLabels: {
    enabled: !0,
    formatter: function (e) {
      return e + "%";
    },
    offsetY: -20,
    style: { fontSize: "12px", colors: ["#304758"] },
  },
  series: [
    {
      name: "تورم",
      data: [2.5, 3.2, 5, 10.1, 4.2, 3.8, 3, 2.4, 4, 1.2, 3.5, 0.8],
    },
  ],
  colors: ["#5664d2"],
  grid: { borderColor: "#f1f1f1", padding: { bottom: 10 } },
  xaxis: {
    categories: [
      "مهر",
      "آبان",
      "آذر",
      "دی",
      "بهمن",
      "اسفند",
      "فروردین",
      "اردیبهشت",
      "خرداد",
      "تیر",
      "مرداد",
      "شهریور",
    ],
    position: "top",
    labels: { offsetY: -18 },
    axisBorder: { show: !1 },
    axisTicks: { show: !1 },
    crosshairs: {
      fill: {
        type: "gradient",
        gradient: {
          colorFrom: "#D8E3F0",
          colorTo: "#BED1E6",
          stops: [0, 100],
          opacityFrom: 0.4,
          opacityTo: 0.5,
        },
      },
    },
    tooltip: { enabled: !0, offsetY: -35 },
  },
  fill: {
    gradient: {
      shade: "light",
      type: "horizontal",
      shadeIntensity: 0.25,
      gradientToColors: void 0,
      inverseColors: !0,
      opacityFrom: 1,
      opacityTo: 1,
      stops: [50, 0, 100, 100],
    },
  },
  yaxis: {
    axisBorder: { show: !1 },
    axisTicks: { show: !1 },
    labels: {
      show: !1,
      formatter: function (e) {
        return e + "%";
      },
    },
  },
  title: {
    text: "تورم در سال 1399",
    floating: !0,
    offsetY: 320,
    align: "center",
    style: { color: "#444" },
  },
  legend: { offsetY: 7 },
};
(chart = new ApexCharts(
  document.querySelector("#column_chart_datalabel"),
  options
)).render();
options = {
  chart: { height: 350, type: "bar", toolbar: { show: !1 } },
  plotOptions: { bar: { horizontal: !0 } },
  dataLabels: { enabled: !1 },
  series: [{ data: [380, 430, 450, 475, 550, 584, 780, 1100, 1220, 1365] }],
  colors: ["#1cbb8c"],
  grid: { borderColor: "#f1f1f1", padding: { bottom: 5 } },
  xaxis: {
    categories: [
      "ایران",
      "ونوزئلا",
      "انگلستان",
      "امریکا",
      "هلند",
      "ایتالیا",
      "فرانسه",
      "ژاپن",
      "چین",
      "آلمان",
    ],
  },
  legend: { offsetY: 5 },
};
(chart = new ApexCharts(
  document.querySelector("#bar_chart"),
  options
)).render();
options = {
  chart: { height: 350, type: "line", stacked: !1, toolbar: { show: !1 } },
  stroke: { width: [0, 2, 4], curve: "smooth" },
  plotOptions: { bar: { columnWidth: "50%" } },
  colors: ["#1cbb8c", "#fcb92c", "#5664d2"],
  series: [
    {
      name: "تیم آ",
      type: "column",
      data: [23, 11, 22, 27, 13, 22, 37, 21, 44, 22, 30],
    },
    {
      name: "تیم ب",
      type: "area",
      data: [44, 55, 41, 67, 22, 43, 21, 41, 56, 27, 43],
    },
    {
      name: "تیم س",
      type: "line",
      data: [30, 25, 36, 30, 45, 35, 64, 52, 59, 36, 39],
    },
  ],
  fill: {
    opacity: [0.85, 0.25, 1],
    gradient: {
      inverseColors: !1,
      shade: "light",
      type: "vertical",
      opacityFrom: 0.85,
      opacityTo: 0.55,
      stops: [0, 100, 100, 100],
    },
  },
  labels: [
    "01/01/1399",
    "02/01/1399",
    "03/01/1399",
    "04/01/1399",
    "05/01/1399",
    "06/01/1399",
    "07/01/1399",
    "08/01/1399",
    "09/01/1399",
    "10/01/1399",
    "11/01/1399",
  ],
  markers: { size: 0 },
  xaxis: { type: "datetime" },
  yaxis: { title: { text: "تعداد" } },
  tooltip: {
    shared: !0,
    intersect: !1,
    y: {
      formatter: function (e) {
        return void 0 !== e ? e.toFixed(0) + " تعداد" : e;
      },
    },
  },
  grid: { borderColor: "#f1f1f1", padding: { bottom: 10 } },
  legend: { offsetY: 7 },
};
(chart = new ApexCharts(
  document.querySelector("#mixed_chart"),
  options
)).render();
options = {
  chart: { height: 350, type: "radialBar" },
  plotOptions: {
    radialBar: {
      dataLabels: {
        name: { fontSize: "22px" },
        value: { fontSize: "16px" },
        total: {
          show: !0,
          label: "کلی",
          formatter: function (e) {
            return 249;
          },
        },
      },
    },
  },
  series: [44, 55, 67, 83],
  labels: ["کامپیوتر", "تبلت", "لپتاپ", "موبایل"],
  colors: ["#5664d2", "#fcb92c", "#1cbb8c", "#ff3d60"],
  legend: { offsetY: 5 },
};
(chart = new ApexCharts(
  document.querySelector("#radial_chart"),
  options
)).render();
options = {
  chart: { height: 320, type: "pie" },
  series: [44, 55, 41, 17, 15],
  labels: ["سری 1", "سری 2", "سری 3", "سری 4", "سری 5"],
  colors: ["#1cbb8c", "#5664d2", "#fcb92c", "#4aa3ff", "#ff3d60"],
  legend: {
    show: !0,
    position: "bottom",
    horizontalAlign: "center",
    verticalAlign: "middle",
    floating: !1,
    fontSize: "14px",
    offsetX: 0,
    offsetY: 5,
  },
  responsive: [
    {
      breakpoint: 600,
      options: { chart: { height: 240 }, legend: { show: !1 } },
    },
  ],
};
(chart = new ApexCharts(
  document.querySelector("#pie_chart"),
  options
)).render();
options = {
  chart: { height: 320, type: "donut" },
  series: [44, 55, 41, 17, 15],
  labels: ["سری 1", "سری 2", "سری 3", "سری 4", "سری 5"],
  colors: ["#1cbb8c", "#5664d2", "#fcb92c", "#4aa3ff", "#ff3d60"],
  legend: {
    show: !0,
    position: "bottom",
    horizontalAlign: "center",
    verticalAlign: "middle",
    floating: !1,
    fontSize: "14px",
    offsetX: 0,
    offsetY: 5,
  },
  responsive: [
    {
      breakpoint: 600,
      options: { chart: { height: 240 }, legend: { show: !1 } },
    },
  ],
};
(chart = new ApexCharts(
  document.querySelector("#donut_chart"),
  options
)).render();
