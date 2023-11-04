domain = "http://147.182.138.184/api/";

regionElem = document.getElementById("region");
districtElem = document.getElementById("district");
submittedregion = document.getElementById("submittedregion").value;
submitteddistrict = document.getElementById("submitteddistrict").value;

fetch(`${domain}regions`)
  .then((response) => response.json())
  .then((regions) => {
    for (let region of regions) {
      option = document.createElement("option");
      option.innerText = region.name;
      option.id = "regopt";
      if (region.name === submittedregion) {
        option.selected = true;
      }
      regionElem.appendChild(option);
    }
  })
  .catch((err) => console.log("error in fetching ", err));

fetch(`${domain}districts`)
  .then((response) => response.json())
  .then((districts) => {
    // adding default district..
    wilaya = districts.filter(
      (district) => district.region === submittedregion
    );
    for (let mlaya of wilaya) {
      option = document.createElement("option");
      option.innerText = mlaya.name;
      option.className = "dstopt";
      if (mlaya.name === submitteddistrict) {
        option.selected = true;
      }
      districtElem.appendChild(option);
    }

    // on change logic
    regionElem.addEventListener("change", (e) => {
      value = e.target.value;
      dists = districts.filter((value) => value.region === e.target.value);
      options = Object.values(districtElem.children);
      for (let opt of options) {
        districtElem.removeChild(opt);
      }

      for (let district of dists) {
        option = document.createElement("option");
        if (dists.indexOf(district) === 0) {
          option.selected = true;
        }
        option.innerText = district.name;
        option.className = "odis";
        districtElem.appendChild(option);
      }
    });
  })
  .catch((err) => console.log("error in fetching districts ", err));
