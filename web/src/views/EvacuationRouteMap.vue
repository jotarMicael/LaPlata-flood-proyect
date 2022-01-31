<template>
  <v-container style="margin-top: 5em; margin">
    <v-row align-content="center" justify="center" class="secundary-color">
      <v-col align-content="center">
        <h1 style="color: #73e6bf" class="text margin">
          Mapa de Recorrido de evacuacion: {{ this.name}}
        </h1>
      </v-col>
      <EvacuationRouteMapId @event="getData" />
    </v-row>
    
  </v-container>
</template>

<script>
import EvacuationRouteMapId from "@/components/EvacuationRouteMapId.vue";

    export default {
        name:"EvacuationRouteMap",
        components: {
            EvacuationRouteMapId
        },
        data: () => ({
            name: null,
            colour: "#FF0000"
        }),
        methods: {
            getData(name) {
                this.name = name;
            },
        }
    }
</script>

<style scoped>

</style>