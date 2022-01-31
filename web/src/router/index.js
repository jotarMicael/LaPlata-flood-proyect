import { createWebHistory, createRouter } from "vue-router";
import HomeView from "@/views/HomeView.vue";
import FloodZonesMap from '@/views/FloodZonesMap.vue'
import FloodZoneMap from '@/views/FloodZoneMap.vue'
import AddDenunciation from '@/views/AddDenunciation.vue'

import MeetingSpotsMap from '@/views/MeetingSpotsMap.vue'
import EvacuationRoutesMap from '@/views/EvacuationRoutesMap.vue'
import EvacuationRouteMap from '@/views/EvacuationRouteMap.vue'


const routes = [
  {
    path: "/",
    name: "Home",
    component: HomeView
  
  },

  //---------------------------
  {
    path: "/flood_zones_maps",
    name: "flood_zones_maps",
    component: FloodZonesMap 
  },
  {
    path: "/flood_zone_map/:id",
    name: "flood_zone_map",
    component: FloodZoneMap 
  },

  //---------------------------

  {
    path: "/meeting_spots_maps",
    name: "meeting_spots_maps",
    component: MeetingSpotsMap 
  },
  {
    path: "/add_denunciation",
    name: "add_denunciation",
    component: AddDenunciation 
  },
  {
    path: "/evacuation_routes_maps",
    name: "evacuation_route_maps",
    component: EvacuationRoutesMap 
  },
  {
    path: "/evacuation_route_map/:id",
    name: "evacuation_route_map",
    component: EvacuationRouteMap
  },
  
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;