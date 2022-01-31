
<template>
      
  <v-container style="margin-top: 5em; margin">
    
    <v-row align-content="center" justify="center" class="secundary-color">
      <v-col lg="12" xl="3">
        
        <h1 style="color: #73e6bf" class="text margin">
          Mapa de Recorrido de Evacuación
        </h1>
         <p class="margin">{{ description }}</p>
            
      </v-col>
    </v-row>
    <AllEvacuationRoutes/>  
  </v-container>
   
</template>

<script>
// @ is an alias to /src
import AllEvacuationRoutes from "@/components/AllEvacuationRoutes.vue";


export default {
  name: "FloodZonesMap",
  components: {
    AllEvacuationRoutes,

  },
  data() {
    return {
      description: "Seleccione un recorrido de evacuacion",
    };
  },
};
</script>