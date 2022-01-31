<template>
  <v-container style="margin-top: 5em; margin">
    <v-row align-content="center" justify="center" class="secundary-color">
      <v-col align-content="center">
        <h1 style="color: #73e6bf" class="text margin">
          Mapa de Zona de inundacion: {{ this.name}}
        </h1>
        <span >Cantidad de Puntos: {{ this.points }}</span><br>
        <span>Color de línea: {{ this.colour }}</span>
      </v-col>
      <FloodZoneMapId @event="getData" />
    </v-row>
    
  </v-container>
</template>
<script>
import FloodZoneMapId from "@/components/FloodZoneMapId.vue";
export default {
  name: "FloodZoneMap",
  components: {
    FloodZoneMapId,
  },
  data: () => ({
    
    name:null,
    colour:null,
    points:null
    
  }),
  methods: {
    
    getData(name,colour,points) {
      this.name = name;
      this.colour = colour;
      this.points = points;
    },
  }
};
</script>
<style>
</style>