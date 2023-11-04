regions = [];
districts = [];

domain = "http://147.182.138.184/api/";

fetch(`${domain}regions`)
  .then((response) => response.json())
  .then((regions) => {
    regionElem = document.getElementById("region");

    for (let region of regions) {
      option = document.createElement("option");
      option.innerText = region.name;
      option.id = "regopt";
      regionElem.appendChild(option);
    }
  });

fetch(`${domain}districts`)
  .then((response) => response.json())
  .then((districts) => {
    districtElem = document.getElementById("district");

    regionElem = document.getElementById("region");

    regionElem.addEventListener("change", (e) => {
      value = e.target.value;
      dists = districts.filter((value) => value.region === e.target.value);

      options = Object.values(districtElem.children);
      for (let opt of options) {
        if (opt.value == "Open this select menu") {
          opt.selected = true;
          continue;
        }
        districtElem.removeChild(opt);
      }

      for (let district of dists) {
        option = document.createElement("option");
        option.innerText = district.name;
        option.className = "dist";

        districtElem.appendChild(option);
      }
    });
  });
