<template>
  <div>
    <l-map
      style="height: 500px"
      :zoom="zoom"
      :center="[-34.79135898963996, -57.99674526817398]"
      @update:zoom="zoomUpdated"
    >
      <l-tile-layer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      ></l-tile-layer>
      <l-marker
        v-for="item in this.coordinates"
        :key="item"
        :lat-lng="item[0]"
        @click="ms_zoom(item)"
      >
      </l-marker>

      
    </l-map>
  </div>
  
</template>
<script>
import { LMap, LTileLayer, LMarker } from "@vue-leaflet/vue-leaflet";
import "leaflet/dist/leaflet.css";

import axios from "axios";
export default {
  name: "AllMeetingSpots",
  components: {
    LMap,
    LTileLayer,
    LMarker,
  },
  data: () => ({
    zoom: 10,
    icon: require(`@/assets/logo.png`),
    iconSize: 40,
    modalShow: false,

    all_meetingspots: [],
    coordinates: [],
    names: [],
  }),
  methods: {
    ms_zoom(item) {
      this.$swal.fire({
        title: item[1],
        html: ' <strong>Calle:</strong> '+item[2] + '<br>'
        +'<br> <strong>Email:</strong> '+item[3]+ '<br>' + 
        '<br> <strong>Coordenadas:</strong>' +item[0],
        imageUrl: "https://www.pngkit.com/png/full/267-2678109_map-point-google-map-marker-gif.png",
        imageWidth: 150,
        imageHeight: 200,
        imageAlt: "Custom image",
      });
    },
    zoomUpdated(zoom) {
      this.zoom = zoom;
    },
    floodZoneUpdated(flood_zone) {
      this.flood_zone = flood_zone;
    },
    async getFloodZones() {
      let result = await axios.get(
        "https://admin-grupo15.proyecto2021.linti.unlp.edu.ar/api/puntos-encuentro/"
      );

      this.all_meetingspots = result.data.puntos_encuentro;
      var coordinates_aux = [];
      var names_aux = [];
      this.all_meetingspots.forEach(function (point) {

        coordinates_aux.push(
          [[parseFloat(point.latitude), parseFloat(point.longitude)],
          point.name,
         point.address,
          point.email]
        );
        names_aux.push(point.name);
      });
      this.coordinates = coordinates_aux;
      this.names = names_aux;
    },
    log(a) {
      console.log(a);
    },
    changeIcon() {
      this.iconWidth += 2;
      if (this.iconWidth > this.iconHeight) {
        this.iconWidth = Math.floor(this.iconHeight / 2);
      }
    },
  },
  computed: {
    dynamicSize() {
      return [this.iconSize, this.iconSize * 1.15];
    },
    dynamicAnchor() {
      return [this.iconSize / 2, this.iconSize * 1.15];
    },
  },
  created() {
    this.getFloodZones();
  },
};
</script>