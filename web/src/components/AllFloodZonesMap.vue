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

      <l-polygon
        :lat-lngs="[this.floodzones_coordinates0]"
        :color="this.colour0"
        :fill="true"
        :fillOpacity="0.5"
        fillColor="#41b782"
      />

      <l-polygon
        :lat-lngs="[this.floodzones_coordinates1]"
        :color="this.colour1"
        :fill="true"
        :fillOpacity="0.5"
        fillColor="#41b782"
      />
      <l-polygon
        :lat-lngs="[this.floodzones_coordinates2]"
        :color="this.colour2"
        :fill="true"
        :fillOpacity="0.5"
        fillColor="#41b782"
      />
      <l-polygon
        :lat-lngs="[this.floodzones_coordinates3]"
        :color="this.colour3"
        :fill="true"
        :fillOpacity="0.5"
        fillColor="#41b782"
      />
      <l-polygon
        :lat-lngs="[this.floodzones_coordinates4]"
        :color="this.colour4"
        :fill="true"
        :fillOpacity="0.5"
        fillColor="#41b782"
      />
      <l-polygon
        :lat-lngs="[this.floodzones_coordinates5]"
        :color="this.colour5"
        :fill="true"
        :fillOpacity="0.5"
        fillColor="#41b782"
      />
    </l-map>
    <div>
      <div class="mt-3" >
        <button v-for="item in all_floodzones" :key="item.id"
          class="btn btn-outline-dark color-text"
          @click="fzm_id(item.id)"
        >
          {{ item.nombre }}
        </button>
      </div>
    </div>
  </div>
</template>
<script>
import { LMap, LTileLayer, LPolygon } from "@vue-leaflet/vue-leaflet";
import "leaflet/dist/leaflet.css";

import axios from "axios";
export default {
  name: "AllFloodZonesMap",
  components: {
    LMap,
    LTileLayer,
    LPolygon,
  },
  data: () => ({
    zoom: 10,
    icon: require(`@/assets/logo.png`),
    iconSize: 40,
    modalShow: false,

    all_floodzones: [],
    floodzones_coordinates0: [],
    colour0: null,
    floodzones_coordinates1: [],
    colour1: null,
    floodzones_coordinates2: [],
    colour2: null,
    floodzones_coordinates3: [],
    colour3: null,
    floodzones_coordinates4: [],
    colour4: null,
    floodzones_coordinates5: [],
    colour5: null,
  }),
  methods: {
    fzm_id(id_) {
      this.$router.push({
        name: "flood_zone_map",
        params: {
          id: id_,
        },
      });
    },
    zoomUpdated(zoom) {
      this.zoom = zoom;
    },
    floodZoneUpdated(flood_zone) {
      this.flood_zone = flood_zone;
    },
    async getFloodZones() {

      let result = await axios.get("https://admin-grupo15.proyecto2021.linti.unlp.edu.ar/api/zonas-inundables");

      this.all_floodzones = result.data.zonas;

      var coordinates = [];
      this.all_floodzones[0].coordenadas.forEach(function (point) {
        coordinates.push([parseFloat(point.lat), parseFloat(point.long)]);
      });
      this.colour0 = this.all_floodzones[0].color;

      this.floodzones_coordinates0 = coordinates;
      coordinates = [];
      this.all_floodzones[1].coordenadas.forEach(function (point) {
        coordinates.push([parseFloat(point.lat), parseFloat(point.long)]);
      });
      this.colour1 = this.all_floodzones[1].color;
      this.floodzones_coordinates1 = coordinates;
      coordinates = [];
      this.all_floodzones[2].coordenadas.forEach(function (point) {
        coordinates.push([parseFloat(point.lat), parseFloat(point.long)]);
      });
      this.colour2 = this.all_floodzones[2].color;
      this.floodzones_coordinates2 = coordinates;
      coordinates = [];
      this.all_floodzones[3].coordenadas.forEach(function (point) {
        coordinates.push([parseFloat(point.lat), parseFloat(point.long)]);
      });
      this.colour3 = this.all_floodzones[3].color;
      this.floodzones_coordinates3 = coordinates;
      coordinates = [];
      this.all_floodzones[4].coordenadas.forEach(function (point) {
        coordinates.push([parseFloat(point.lat), parseFloat(point.long)]);
      });
      this.colour4 = this.all_floodzones[4].color;
      this.floodzones_coordinates4 = coordinates;
      coordinates = [];

      this.all_floodzones[5].coordenadas.forEach(function (point) {
        coordinates.push([parseFloat(point.lat), parseFloat(point.long)]);
      });
      this.colour5 = this.all_floodzones[5].color;
      this.floodzones_coordinates5 = coordinates;
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