
<template>
      
  <v-container style="margin-top: 5em; margin">
    
    <v-row align-content="center" justify="center" class="secundary-color">
      <v-col lg="12" xl="3">
        
        <h1 style="color: #73e6bf" class="text margin">
          Mapa de Puntos de Encuentro
        </h1>
         <p class="margin">{{ description }}</p>
            
      </v-col>
    </v-row>
    <AllMeetingSpots/>
  </v-container>
   
</template>

<script>
// @ is an alias to /src
import AllMeetingSpots from "@/components/AllMeetingSpots.vue";


export default {
  name: "MeetingSpotsMap",
  components: {
    AllMeetingSpots,

  },
  data() {
    return {
      description: "Seleccione una zona",
    };
  },
};
</script>