<template>
    <v-dialog 
    transition="dialog-bottom-transition"
    v-model="dialog"   
    persistent
    max-width="600">
        <v-card>
            <v-toolbar
            color="primary"
            dark
            ><span 
            style="margin-left:10px;">Manage user</span></v-toolbar>
            <v-card-text>
                <v-form
                ref="userForm"
                lazy-validation>
                    <v-text-field 
                    v-if="p_user.username != 'admin'"
                    clearable 
                    label="Username" 
                    variant="outlined" 
                    prepend-icon="mdi-asterisk"
                    :rules="[rules.required]"
                    v-model="p_user.username"></v-text-field>

                    <v-text-field 
                    clearable 
                    :rules="[rules.required, rules.mail]"
                    label="Email" 
                    variant="outlined" 
                    prepend-icon="mdi-asterisk"
                    v-model="p_user.email"></v-text-field>

                    <v-text-field 
                    clearable 
                    :rules="[rules.required]"
                    label="Password" 
                    type="password"
                    variant="outlined" 
                    prepend-icon="mdi-asterisk"
                    v-model="p_user.password"></v-text-field>

                    <v-select
                    v-if="p_user.username != 'admin'"
                    v-model="p_user.grants"
                    label="Grants"
                    :items="roles"
                    item-title="display_name"
                    item-value="name"
                    multiple
                    >
                        <template v-slot:selection="{ item, index }">
                            <span v-if="index >= 0">
                                {{item.display_name}}
                            </span>
                        </template>
                    </v-select>
                </v-form>
            </v-card-text>
            <v-card-actions class="justify-end">
            <v-btn
                text
                color="primary"
                @click="send"
            >Save</v-btn>
            <v-btn
                text
                color="red"
                @click="onClose"
            >Abort</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog> 
</template>

<script>
import { unused } from '@/types/CompilerUtils'
import { getToken, BASE_API_URL } from '@/types/AppConstants';

export default {
    
    props: {
        open:Boolean,
        OK:Function,
        onClose:Function,
        user:Object
    },
    created(){
        let headers = new Headers();
        headers.append("Authorization", getToken())
        headers.append("Content-type", "application/json")
        headers.append("Access-Control-Allow-Origin", "*")

        let init = { method: 'GET',
                    headers: headers,
                    mode: 'cors'
                };

        var request = new Request(BASE_API_URL+'api/roles', init);

        fetch(request,init)
        .then((data)=>{
            return data.json()
        })
        .then((json)=>{
            if("error" in json)
            {
                console.log(json.error)
            }
            else
            {
                this.roles=json.data;
            }
        })
    },
    data(){
        return {      
            dialog:false,      
            rules:{
                required:v => (v || '').length > 0 ||
                    `This field is required`,
                mail:v=>(v||'').match(/^[\w-.]+@([\w-]+.)+[\w-]{2,4}$/) || `This field must be a mail (example@domain.com)`
            },
            p_user:this.user ?? {
                username:null,
                password:null,
                email:null,
                grants:[]
            },
            roles:[]
        }
    },
    watch:{
        open(n, o)
        {
            unused(o);
            this.dialog=n;
        },
        user(n, o)
        {
            unused(o);
            console.log(n)
            this.p_user = n
        }
    },
    methods:{
        async send()
        {
            const { valid } = await this.$refs.userForm.validate()
            if(valid)
            {
                this.OK(this.p_user)
            }
        },
        close()
        {
            this.onClose()
        }
    }
}
</script>
