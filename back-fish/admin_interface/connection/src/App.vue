<template>
  <v-app>
    <v-main style="display:flex; flex-direction: column; justify-content: center;">
      <v-card style="width:50%; margin:auto;">
        <v-card-title>Log in</v-card-title>
        <v-card-text>
          <v-form ref="loginform">
            <v-text-field label="Login" v-model="login"></v-text-field>
            <v-text-field type="password" label="Password" v-model="password"></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" @click="logIn">
            Log in
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-main>
    <v-snackbar
      v-model="snackbar"
    >
      {{ event_text }}

      <template v-slot:actions>
        <v-btn
          color="pink"
          variant="text"
          @click="snackbar = false"
        >
          Close
        </v-btn>
      </template>
    </v-snackbar>
  </v-app>
</template>

<script>
import { BASE_URL, setToken } from "./constants"

export default {
  name: 'App',

  data: () => ({
    login:null,
    password:null,
    snackbar:false,
    event_text:""
  }),
  created(){
    const urlSearchParams = new URLSearchParams(window.location.search);
    const params = Object.fromEntries(urlSearchParams.entries());
    if("lostauth" in params)
    {
      this.event_text="Lost authentication, please reconnect."
      this.snackbar=true
    }
  },
  methods:{
    async logIn()
    {      
      const { valid } = await this.$refs.loginform.validate()
      if(valid)
      {        
        let headers = new Headers();
        headers.append("Content-Type", "application/json")
        headers.append("Access-Control-Allow-Origin", "*")

        let details={
          username:this.login,
          password:this.password
        }
        let init = { method: 'POST',
                  headers: headers,
                body:JSON.stringify(details)};
        var request = new Request(BASE_URL+'admin/auth/login', init);
        fetch(request,init)
        .catch((err)=>{       
          console.log(err)
        })
        .then((data)=>{
          return data.json()
        })
        .then((data)=>{   
          if("error" in data){
            switch(data["error"])
            {
              case "ERRAUTH":
                this.event_text="Authentication failed. Please try again."
                this.snackbar=true;
            }
            return
          }
          setToken(data.data)
          window.location.replace(BASE_URL+"admin/dashboard");
        })
      }
    }
  }
}
</script>
