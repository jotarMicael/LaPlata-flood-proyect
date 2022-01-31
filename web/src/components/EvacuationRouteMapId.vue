<template>
    <l-map style="height: 500px;" :zoom="zoom" 
      
      :center="[-34.79135898963996, -57.99674526817398]"
      @update:zoom="zoomUpdated"
    >
      <l-tile-layer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      ></l-tile-layer>

      <l-polyline
        :lat-lngs="[this.evacuation_coordinates]"
        :color="this.color"
        :fill="true"
        :fillOpacity="0.5"
        fillColor="#41b782"
      />

    </l-map>
</template>

<script>
import { LMap, LTileLayer, LPolyline } from "@vue-leaflet/vue-leaflet";
import "leaflet/dist/leaflet.css";

import axios from "axios";
    export default {
        name: "EvacuationRouteMapId",
        components: {
            LMap,
            LTileLayer,
            LPolyline
        },
        data: () => ({
            zoom: 10,
            evacuation_route: [],
            evacuation_coordinates: [],
            color: "#FF0000"
        }),
        methods: {
            zoomUpdated(zoom) {
                this.zoom = zoom;
            },
            floodZoneUpdated(flood_zone) {
                this.flood_zone = flood_zone;
            },
            async getEvacuationRoute() {

                //URL local
                // let result = await axios.get("http://localhost:5000/api/recorrido-evacuacion/"+this.$route.params.id);
                //URL produccion
                let result = await axios.get("https://admin-grupo15.proyecto2021.linti.unlp.edu.ar/api/recorrido-evacuacion/"+this.$route.params.id);
                    
                this.evacuation_route = result;

                var coordinates = [];
                this.evacuation_route.data.coordenadas.forEach(function (point) {
                    coordinates.push([parseFloat(point.lat), parseFloat(point.long)]);
                });
                
                this.evacuation_coordinates = coordinates;
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
            this.getEvacuationRoute();
        },
    }
</script>

<style scoped>

</style>