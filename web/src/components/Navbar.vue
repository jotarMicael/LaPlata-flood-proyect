<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container-fluid">
    <a class="navbar-brand" @click="goToHome" href="#">
      <img src="../assets/logoApp.jpeg"  alt="" width="30" height="24" class="d-inline-block align-text-top">
      InundacionesLP
    </a>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent"
          aria-expanded="false"
          aria-label="Toggle navigation"
        > 
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <a class="nav-link active" aria-current="page" @click="goToHome" href="#">| Inicio |</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" aria-current="page" @click="goToPuntosDeEncuentro" href="#">| Puntos de Encuentro |</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" aria-current="page" @click="goToRecorridos" href="#">| Recorridos de Evacuación |</a>
            </li>
            <li class="nav-item">
              <a @click="fzm" class="nav-link" aria-current="page" href="#">| Zonas Inundables |</a>
            </li>
            
            <li class="nav-item">
              <a @click="den" class="nav-link" aria-current="page" href="#">| Realizar Denuncia |</a>
            </li>            
          </ul>          
        </div>
      </div>
    </nav>
  </div>
</template>

<script>
export default {
  name: "Navbar",
  methods: {
    fzm() {
      this.$router.push({ path: '/flood_zones_maps' });
    },
    goToHome() {
      this.$router.push({ path: '/' });
    },
    den() {
      this.$router.push({ path: '/add_denunciation' });
    },
    goToPuntosDeEncuentro() {
      this.$router.push({ path: '/meeting_spots_maps' })
    },
    goToRecorridos() {
      this.$router.push({ path: '/evacuation_routes_maps' })
    }
  },
};
</script>

<style scoped>
</style>