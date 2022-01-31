<template>
  <div class="container" style="margin-top: 5em; margin">
    <h1>Cargar Denuncia</h1>
  <b-container class="container">
    <b-form id="form">
				<b-row>
					<b-col cols="12" md="6" class="pr-5">
						<b-form-input type="text" placeholder="Titulo de la Denuncia"  v-model="title" required > </b-form-input>
						<b-alert v-if="nameErrors != null" show variant="danger" required >
							{{error_name}}
						</b-alert>
            <br>
            <b-form-input type="text" placeholder="Descripcion"  v-model="description" > </b-form-input><br>
						<b-form-input type="text" placeholder="Telefono"  v-model="phone_d" > </b-form-input><br>
						<b-alert v-if="error_phone != null" show variant="danger" >
							{{ error_phone }}
						</b-alert>

						<b-form-input type="text" placeholder="Email"  v-model="email_d" required > </b-form-input><br>
						<b-alert v-if="error_email != null" show variant="danger">
							{{ error_email }}
						</b-alert>

            <b-form-input type="text" placeholder="Nombre del Denunciante" v-model="first_name_d" required> </b-form-input><br>
            <b-form-input type="text" placeholder="Apellido del Denunciante" v-model="last_name_d" required> </b-form-input><br>
          
            <span>Seleccione una categoria</span>
						<b-form-select  v-model="category_id" required>
							<option :value="null"  disabled >Tipo de categoria</option>
							<option v-for="(category,index) in categories" :key="index" :value="category.id" :id="category.name_cat">
							{{category.name_cat}}
							</option>
						</b-form-select><br>
           
					</b-col>
					<b-col cols="12" md="6" class="border-left pl-5">
           
    <l-map style="height: 500px;" 
      :zoom="zoom"   
      :center="[-34.91869346467701, -57.94956597589476]"
      @update:zoom="zoomUpdated"
      @click="addMarker"
    >
      <l-tile-layer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      ></l-tile-layer>
       <l-marker :lat-lng="point"></l-marker>
   
    </l-map>
            
						<div class="d-flex justify-content-center mt-5">
							<b-button v-if="!success" type="submit" @click="onSubmit" variant="danger"> Crear Denuncia</b-button>
							<b-alert v-if="success" show variant="success" class="success">
								¡Se registro la denuncia con éxito!
							</b-alert>
						</div>
					</b-col>
				</b-row>
			</b-form>
  </b-container>
  </div>
</template>
<script>
import axios from "axios";
import { required, maxLength, email } from "vuelidate/lib/validators";
// import { validationMixin } from "vuelidate";
import { LMap, LTileLayer, LMarker } from "@vue-leaflet/vue-leaflet";

export default {
  name: "AddDenunciation",
  components: {
    LMap,
    LTileLayer,
    LMarker
    },
 
  //  mixins: [validationMixin],

  validations: {
    title: { required, maxLength: maxLength(30) },
    description: { required, maxLength: maxLength(50) },
    email_d: { required, email, maxLength: maxLength(30) },
    phone_d: { required, maxLength: maxLength(30) },
    first_name_d: { required, maxLength: maxLength(30) },
    last_name_d: { required, maxLength: maxLength(30) },
    category_id: { required },
  },
 
  data: () => ({
    zoom: 12,
    title: "",
    description: "",
    email_d: "",
    phone_d: "",
    first_name_d: "",
    last_name_d: "",
    category_id: null,
    error_name: null,
		error_phone: null,
		error_email: null,
    categories:null,
		success: false,
    point: [0, 0]
  }),

  methods: {
    async getCategories() {

      let result = await axios.get("https://admin-grupo15.proyecto2021.linti.unlp.edu.ar/api/category-types");
			this.categories= result.data.categories;
    },
    zoomUpdated(zoom) {
      this.zoom = zoom;
    },
    

    async onSubmit() {
      
      let form = {
        title: this.title,
        description: this.description,
        email_d: this.email_d,
        phone_d: this.phone_d,
        first_name_d: this.first_name_d,
        last_name_d: this.last_name_d,
        category_id: this.category_id,
        latitude: this.point[0],
        longitude: this.point[1]
      }

      // para probar local
      //const url="http://localhost:5000/api/denuncias";

      const url = "https://admin-grupo15.proyecto2021.linti.unlp.edu.ar/api/denuncias";
      let result = await axios.post(url,form, {
              headers: {
                "Access-Control-Allow-Origin": "*",
                "Content-Type": "application/json"
              }
      })
      
			.then( 
				response => {
					if(response.data.errores){
						let errores = response.data.errores;
						if(errores.error_name) this.error_name = errores.error_name
						if(errores.error_phone) this.error_phone = errores.error_phone;
						if(errores.error_time) this.error_time = errores.error_time;
						if(errores.error_email) this.error_email = errores.error_email;
						this.success = false;
					}else{
						this.success = true;
            this.$router.push({ name: 'Home' })
					}
        })
      .catch(error => {
              console.log(error.response);
             
            })
      console.log(result)
    },

    reset(){
        this.title= "",
        this.description= "",
        this.email_d= "",
        this.phone_d= "",
        this.first_name_d= "",
        this.last_name_d= "",
        this.category_id= null,
        this.user_id= null
        
    },
    
    async changeAddress() {
      let result = await axios.get(
        `https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=${this.point[0]}&lon=${this.point[1]}`
      );
      console.log(result)
    },
    addMarker(event) {
      if (event.latlng){
        this.point = [event.latlng.lat, event.latlng.lng];
      }
      this.changeAddress();
    },
  },
  created(){
		this.getCategories()
	},
}; 
</script>
<style>
</style>