<template>
  <div class="mt-4">
    <div>
      <img src="../assets/logoApp.jpeg" class="tamañoImg" />
      <h2 class="mb-2 mt-3">Bienvenido a InundacionesLP</h2>
      <br />
      <hr style="width: 70%; margin: auto" class="mb-3" />
      <h5 class="mb-5">¿Qué podrás hacer en esta aplicación?</h5>
    </div>
<div class="container">
    <div class="d-flex justify-content-center">
      <div class="card border-dark mb-3 marginHorizontal">
        <div class="card-header bg-dark text-white border-dark">
          Puntos de Encuentro
        </div>
        <div class="card-body text-dark">
          <p class="color-text">
            Podras visualizar los diferentes puntos de encuentro en caso de que
            ocurra una inundación.
          </p>
        </div>
        <div class="card-footer bg-transparent border-dark">
          <button @click="msm" class="btn btn-outline-dark color-text">Ver mas...</button>
        </div>
      </div>
      <div class="card border-dark mb-3 marginHorizontal">
        <div class="card-header border-dark  bg-dark text-white">Recorridos de Evacuación</div>
        <div class="card-body text-dark">
          <p class="color-text">
            Podras ver los distintos recorridos que existen en caso de
            inundación.
          </p>
        </div>

        <div class="card-footer bg-transparent border-dark">
          <button @click="goToRecorridos" class="btn btn-outline-dark color-text">Ver mas...</button>
        </div>
      </div>
      
    </div>

    <div class="d-flex justify-content-center">
      <div class="card border-dark mb-3 marginHorizontal">
        <div class="card-header bg-dark text-white border-dark">
          Zonas Inundables
        </div>
        <div class="card-body text-dark">
          <p class="color-text">
            Podras ver las distinas zonas inundables notificadas que existen en
            la ciudad.
          </p>
        </div>
        <div class="card-footer bg-transparent border-dark">
          <button
            @click="fzm"
            class="btn btn-outline-dark color-text">
            Ver mas...
          </button>
        </div>
      </div>
      <div class="card border-dark mb-3 marginHorizontal">
        <div class="card-header bg-dark text-whitebg-dark text-white border-dark">Realizar Denuncias</div>
        <div class="card-body text-dark">
          <p class="color-text">
            Podras realizar denuncias sobre alcantarillas tapadas, basurales,
            etc.
          </p>
        </div>
        <div class="card-footer bg-transparent border-dark">
          <button 
          @click="den"
          class="btn btn-outline-dark color-text">Ver mas...</button>
        </div>
      </div>
      </div>
    </div>
  </div>
</template>

<script>


export default {
  name: "Home",
  components: {

  },
  methods: {
    fzm() {
      this.$router.push({ path: '/flood_zones_maps' });
    },
    msm() {
      this.$router.push({ path: '/meeting_spots_maps' });
    },
    den() {
      this.$router.push({ path: '/add_denunciation' });
    },
    goToRecorridos() {
      this.$router.push({ path: '/evacuation_routes_maps' });
    },
  },
};
</script>

<style scoped>
.marginHorizontal {
  margin-left: 20px;
  margin-right: 20px;
  width: 60vh;
}

.tamañoImg {
  width: 7rem;
  border-radius: 10%;
}

.color-text {
  color: rgb(70, 70, 70);
}
</style>