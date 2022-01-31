<template>
  
    <l-map style="height: 500px;" :zoom="zoom" 
      
      :center="[-34.79135898963996, -57.99674526817398]"
      @update:zoom="zoomUpdated"
    >
      <l-tile-layer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      ></l-tile-layer>

      <l-polygon
        :lat-lngs="[this.floodzone_coordinates]"
        :color="this.colour"
        :fill="true"
        :fillOpacity="0.5"
        fillColor="#41b782"
      />

    </l-map>
   
  
</template>
<script>
import { LMap, LTileLayer, LPolygon } from "@vue-leaflet/vue-leaflet";
import "leaflet/dist/leaflet.css";

import axios from "axios";
export default {
  name: "FloodZoneMapId",
  components: {
    LMap,
    LTileLayer,
    LPolygon,
  },
  data: () => ({
    zoom: 10,
    all_floodzone: [],
    floodzone_coordinates: [],
    colour: null,
    name:null,
    
  }),
  methods: {
    

    zoomUpdated(zoom) {
      this.zoom = zoom;
    },
    floodZoneUpdated(flood_zone) {
      this.flood_zone = flood_zone;
    },
    async getFloodZones() {

      let result = await axios.get("https://admin-grupo15.proyecto2021.linti.unlp.edu.ar/api/zonas-inundables/"+this.$route.params.id);

      this.all_floodzone = result.data.atributos;

      var coordinates = [];
      this.all_floodzone.coordenadas.forEach(function (point) {
        coordinates.push([parseFloat(point.lat), parseFloat(point.long)]);
      });
      this.colour = this.all_floodzone.color;
      this.name = this.all_floodzone.nombre;
      
      this.floodzone_coordinates = coordinates;
      this.$emit("event",this.name,this.colour, this.floodzone_coordinates.length);
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