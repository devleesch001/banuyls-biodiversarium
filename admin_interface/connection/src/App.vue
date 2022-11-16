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
  </v-app>
</template>

<script>

export default {
  name: 'App',

  data: () => ({
    login:null,
    password:null
  }),
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
        var request = new Request('http://localhost:5000/auth/login', init);
        fetch(request,init)
        .then((data)=>{
          console.log(data)
        })
      }
    }
  }
}
</script>
