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
      <l-polyline
        v-for="(item, index) in this.all_evacuationRoutes"
        :key="item[2]"
        :lat-lngs="this.all_coordinates[index]"
        :color="this.color"
      >
      </l-polyline>
    </l-map>
    <div>
      <div class="mt-3" >
        <button v-for="item in this.all_evacuationRoutes" :key="item.id"
          class="btn btn-outline-dark color-text"
          @click="fzm_id(item.id)"
        >
          {{ item.name }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { LMap, LTileLayer, LPolyline } from "@vue-leaflet/vue-leaflet";
import "leaflet/dist/leaflet.css";
import axios from "axios";
export default {
  name: "AllEvacuationRoutes",
  components: {
    LMap,
    LTileLayer,
    LPolyline,
  },
  data: () => ({
    zoom: 10,
    icon: require(`@/assets/logo.png`),
    iconSize: 40,
    modalShow: false,

    all_evacuationRoutes: [],
    all_coordinates:[],
    color: "#FF0000"
  }),
  methods: {
    fzm_id(id_) {
      this.$router.push({
        name: "evacuation_route_map",
        params: {
          id: id_,
        },
      });
    },
    evacuationRoute_zoom(item) {
      this.$swal.fire({
        title: item[3],
        html: " <strong>Descripcion:</strong> " + item[2] + "<br/>",
        imageUrl:
          "https://www.pngkit.com/png/full/267-2678109_map-point-google-map-marker-gif.png",
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
        "https://admin-grupo15.proyecto2021.linti.unlp.edu.ar/api/recorridos-evacuacion/"
      );

      this.all_evacuationRoutes = result.data.recorridos;
      let evacuationRoutes_aux = [];
      let all_coordinates_aux = [];
      this.all_evacuationRoutes.forEach(function (point) {
        evacuationRoutes_aux.push(point);
        let coordenadasAux = [];
        point.coordenadas.forEach(c => {
            let arrAux = [];
            arrAux.push(c.lat);
            arrAux.push(c.long);
            coordenadasAux.push(arrAux);
        })
        all_coordinates_aux.push(coordenadasAux);
      });
      this.all_evacuationRoutes = evacuationRoutes_aux;
      this.all_coordinates = all_coordinates_aux;
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

<style scoped>
</style>