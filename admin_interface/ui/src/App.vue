<template>
  <v-app>
    <v-app-bar dense color="primary">
      <v-toolbar-title style="font-weight: bold; font-size:1.5em">
        <v-icon style="margin-right:20px">mdi-diving-helmet</v-icon>
        Seaquarium admin pannel
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn icon @click="logout" style="margin-right:30px"><v-icon>mdi-power</v-icon></v-btn>
    </v-app-bar>
    <v-main>
      <SpeciesPannelVue v-if="menuselection==0" style="margin-bottom:5%"></SpeciesPannelVue>
      <StatsPannelVue v-if="menuselection==1"></StatsPannelVue>
      <ParamsPannelVue v-if="menuselection==2"></ParamsPannelVue>
    </v-main>
    <v-bottom-navigation
      v-model="menuselection"
      :style="'background-color:'+color"
      mode="shift"
      grow
    >
      <v-btn>
        <v-icon>mdi-jellyfish</v-icon>
        <span>Species</span>
      </v-btn>
      <v-btn>
        <v-icon>mdi-chart-bar</v-icon>
        <span>Stats</span>
      </v-btn>
      <v-btn>
        <v-icon>mdi-cog</v-icon>
        <span>Params</span>
      </v-btn>
    </v-bottom-navigation>
  </v-app>
</template>

<script>

import SpeciesPannelVue from './components/SpeciesPannel.vue'
import StatsPannelVue from './components/StatsPannel.vue'
import ParamsPannelVue from './components/ParamsPannel.vue';
import { BASE_API_URL, getToken, removeToken } from './types/AppConstants';

export default {
  name: 'App',

  components: {
    SpeciesPannelVue,StatsPannelVue,ParamsPannelVue
  },

  created()
  {
    if(!localStorage.getItem("token"))
    {           
      window.location.replace(BASE_API_URL+"admin/auth/login");
    }
    else{
      setInterval(()=>{
        let headers = new Headers();
        headers.append("Content-type", "application/json")
        headers.append("Access-Control-Allow-Origin", "*")
        headers.append("Authorization", getToken())

        let init = { method: 'GET',
                    headers: headers};

        var request = new Request(BASE_API_URL+'admin/auth/check', init);

        fetch(request,init)
        .catch((err)=>{
            console.log(err)
        })
        .then((data)=>{
          return data.json()
        })
        .then((data)=>{
          if(!data.data)
          {            
            window.location.replace(BASE_API_URL+"admin/auth/login?lostauth");
          }
        })
      }, 1000*60*20)
    }
  },
  data(){
    return {menuselection: 0}
  },
  methods:{
    logout()
    {
      removeToken();
      window.location.replace(BASE_API_URL+"admin/auth/login");
    }
  },
  computed:{
    color(){   
      switch (this.menuselection) {
          case 0: return '#9CADCC'
          case 1: return 'teal'
          case 2: return 'indigo'
          default: return 'blue-grey'
        }
    }
  },
  watch: {
    menuselection(newMenu, oldMenu) {
      if(newMenu == undefined)
      {
        this.menuselection = oldMenu;
      }
      else
      {
        this.menuselection = newMenu;
      }
    }
  }
}
</script>

<style scoped>
  .v-bottom-navigation{
    transform:none !important;
  }
</style>
