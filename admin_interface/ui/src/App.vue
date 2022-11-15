<template>
  <v-app>
    <v-app-bar dense color="primary">
      <v-toolbar-title style="font-weight: bold; font-size:1.5em">
        <v-icon style="margin-right:20px">mdi-diving-helmet</v-icon>
        Seaquarium admin pannel
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn icon style="margin-right:30px"><v-icon>mdi-power</v-icon></v-btn>
    </v-app-bar>
    <v-main>
      <SpeciesPannelVue v-if="menuselection==0"></SpeciesPannelVue>
      <StatsPannelVue v-if="menuselection==1"></StatsPannelVue>
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
    </v-bottom-navigation>
  </v-app>
</template>

<script>

import SpeciesPannelVue from './components/SpeciesPannel.vue'
import StatsPannelVue from './components/StatsPannel.vue'

export default {
  name: 'App',

  components: {
    SpeciesPannelVue,StatsPannelVue
  },

  data(){
    return {menuselection: 0}
  },
  computed:{
    color(){   
      switch (this.menuselection) {
          case 0: return '#9CADCC'
          case 1: return 'teal'
          case 2: return 'brown'
          case 3: return 'indigo'
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