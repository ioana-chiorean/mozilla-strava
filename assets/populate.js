let ids = {
  '197162': 'cycling',
  '2298': 'running',
};

document.addEventListener("DOMContentLoaded", () => {
  for (let id in ids) {
    let lookup = ids[id];
    fetch(`summaries/summary.${id}.json`)
    .then((response) => {
      return response.json();
    }).then((json) => {
      let latest = false;
      for (let key in json) {
        if (!latest) {
          let distance = document.getElementById(`${lookup}-distance`);
          distance.textContent = Math.round(json[key].distance / 1000);
          let athletes = document.getElementById(`${lookup}-athletes`);
          athletes.textContent = json[key].athletes;
          latest = true;
        }
      }
    });
  }
});
