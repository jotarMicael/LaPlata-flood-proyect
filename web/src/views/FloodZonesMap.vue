
<template>
      
  <v-container style="margin-top: 5em; margin">
    
    <v-row align-content="center" justify="center" class="secundary-color">
      <v-col lg="12" xl="3">
        
        <h1 style="color: #73e6bf" class="text margin">
          Mapa de Zonas de inundacion
        </h1>
         <p class="margin">{{ description }}</p>
            
      </v-col>
    </v-row>
    <AllFloodZonesMap/>  
  </v-container>
   
</template>

<script>
// @ is an alias to /src
import AllFloodZonesMap from "@/components/AllFloodZonesMap.vue";


export default {
  name: "FloodZonesMap",
  components: {
    AllFloodZonesMap,

  },
  data() {
    return {
      description: "Seleccione una zona",
    };
  },
};
</script>