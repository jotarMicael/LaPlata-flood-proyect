let map;
let marker;

const mapClickHandlder = (e) => {
    addMarker(e.latlng)
}

const addMarker = ( { lat, lng } ) => {
    if (marker) marker.remove();
    console.log(marker)
    marker = L.marker( [lat,lng] ).addTo(map);
}

const addSearchControl = () => {
    L.control.scale().addTo(map)
    let searchControl = new L.esri.Controls.Geosearch().addTo(map);

    let results = new L.LayerGroup().addTo(map);

    searchControl.on('results', (data) => {
        results.clearLayers();
        if (data.results.length > 0) {
            addMarker(data.results[0].latlng)
        }
    })
}

const submitHandler = (event) => {
    
    if (!marker) {
        event.preventDefault();
        alert('Debes seleccionar una ubicación en el mapa')
        console.log(event.target)
    }
    else {
        latitude_and_longitude = marker.getLatLng();
        document.getElementById('latitude').setAttribute('value',latitude_and_longitude.lat)
        document.getElementById('longitude').setAttribute('value',latitude_and_longitude.lng)
        console.log(event.target)
    }
}

const initializeMap = (selector) => {
    latitude = -34.9187;
    longitude = -57.956;
    if(window.location.pathname.includes("update")){
        latitude = document.getElementById('latitude').getAttribute('value');
        longitude = document.getElementById('longitude').getAttribute('value');
    }
    map = L.map('mapid').setView([latitude, longitude], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
    addSearchControl();
    if(window.location.pathname.includes("update")){
        addMarker({"lat":latitude, "lng": longitude});
    }
    map.on('click', mapClickHandlder);
    
}

window.onload = () => {
    initializeMap('mapid');
    
}