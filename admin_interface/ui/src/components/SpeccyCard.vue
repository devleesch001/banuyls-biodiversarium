<template>
    <v-card class="mx-auto speccy-card" 
        outlined
        :color="allColors[type]">
        <v-toolbar
        style="padding-left:2%; background-color: transparent;">
            <v-icon style="margin-right:10px;">mdi-{{allIcons[type]}}</v-icon>
            <v-card-title>{{name}}</v-card-title>
            <v-spacer v-if="image"></v-spacer>
            <v-img v-if="image"
                aspect-ratio="1"
                :src="image"
                cover>
            </v-img>
            <div v-else class="speccy-subtitle">
                <div class="speccy-scientific">
                    {{s_name}}
                </div>
                <v-divider vertical></v-divider>
                <div>
                    {{family}}
                </div>
            </div>
        </v-toolbar>
        <div v-if="image" class="speccy-subtitle">
            <div  style="margin-right:5%;" class="text-subtitle-1 speccy-scientific">
                {{s_name}}
            </div>
            <v-divider vertical></v-divider>
            <div style="margin-left:5%;">
                {{family}}
            </div>
        </div>
        <v-divider class="mx-4"></v-divider>
        <v-card-text>
            <p style="font-size: 1.4em; font-weight: bold; margin-bottom: 20px;">Description</p>
            <v-expansion-panels variant="popout">
                <template v-for="(value, key) of description" :key="key">
                    <v-expansion-panel
                    v-if="value!=null && value.length > 0"
                    :title="key"
                    :text="value">
                    </v-expansion-panel>
                </template>
            </v-expansion-panels>
        </v-card-text>
        <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn icon style="background-color: white;" elevation="3" @click="modifyDialog=true">
                <v-icon color="blue">mdi-lead-pencil</v-icon>
            </v-btn>
            <v-btn icon style="background-color: white;" elevation="3" @click="deleteConfirm=true">
                <v-icon color="red">mdi-delete</v-icon>
            </v-btn>
        </v-card-actions>
        <v-dialog v-model="deleteConfirm">
            <v-card width="500px" style="margin:auto;">
                <v-card-title>Do you really want to delete this speccy ?</v-card-title>
                <v-card-text>This action cannot be undone</v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="primary" @click="deleteConfirm=false">Cancel</v-btn>
                    <v-btn color="red" @click="this.delete">Confirm</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
        <SpeccyDialogVue :open="modifyDialog" :onClose="()=>modifyDialog=false" :OK="update" :default="{            
            name,
            s_name,
            description,
            family,
            type,
            image,
            id:s_id
        }"></SpeccyDialogVue>
    </v-card>
</template>

<script>
import SpeccyDialogVue from './SpeccyDialog.vue'
import { BASE_API_URL, TYPES_COLOR, TYPES_ICON } from '@/types/AppConstants'
import { getToken } from '../types/AppConstants'

export default {
    props:{
        name:String,
        s_name:String,
        description:Object,
        family:String,
        type:String,
        s_id:Number,
        image:String
    },
    components:{
        SpeccyDialogVue
    },
    data(){
        return {
            deleteConfirm:false,
            modifyDialog:false,
            allIcons:TYPES_ICON,
            allColors:TYPES_COLOR
        }
    },
    methods:{
        delete(){
            fetch(BASE_API_URL+'api/species_delete/'+this.s_id, {method:"DELETE", headers:{
                "Authorization": getToken()
            }})
            .catch((err)=>{
                console.log(err)
            })
            .then((data)=>{                
                this.bus.emit("speccy_deleted", this.name)
                return data.json()
            })
            .then((data)=>{
                console.log(data)
                if("error" in data && data.error=="NOTAUTH")
                {                    
                    window.location.replace(BASE_API_URL+"auth/login?lostauth");
                    return;
                }
            })
            this.deleteConfirm=false;
        },
        async update(speccy)
        {                   
            let headers = new Headers();
            headers.append("Content-type", "application/json")
            headers.append("Access-Control-Allow-Origin", "*")
            headers.append("Authorization", getToken())

            let init = { method: 'POST',
                        headers: headers,
                        body: JSON.stringify(speccy)};

            var request = new Request(BASE_API_URL+'api/species_update', init);

            fetch(request,init)
            .catch((err)=>{
                if("error" in err && err.error=="NOTAUTH")
                {                    
                    window.location.replace(BASE_API_URL+"auth/login?lostauth");
                    return;
                }
            })
            .then(()=>{
                this.bus.emit("speccy_updated", this.name)
            })
            this.modifyDialog = false;
        }
    }
}
</script>

<style scoped>
    .speccy-card{
        padding:2%;
    }

    .speccy-subtitle{
        display:flex;
        justify-content: center;
        width:60%;
        position:relative;
        right:0;
    }

    .speccy-subtitle > div{
        font-size: 0.9em !important;
        flex:1 1 auto;
        text-align: center;
        word-wrap: normal;
    }

    .speccy-scientific{
        font-style: italic;
    }
</style>