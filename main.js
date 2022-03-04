var app = new Vue({
  el: "#app",
  data: {
    message: "Hello Vue!",
    videoPlaying: true,
  },
});

class Video {
  constructor() {}
}

function loadCsvData(response) {
  console.log(response);
  if (!("data" in response)) {
    console.log("Cannot parse CSV");
  }
  const columnRow = response.data[0];
  let columnNameToIdx = {};
  for (const i in columnRow) {
    columnNameToIdx[columnRow[i]] = i;
  }
  console.log(columnNameToIdx);
  for (let i = 1; i < response.data.length; i++) {}
}

Papa.parse("db.csv", {
  download: true,
  complete: loadCsvData,
});
