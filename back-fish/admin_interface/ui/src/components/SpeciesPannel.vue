<template>
    <div>
        <div>        
            <v-btn icon
            color="primary"
            @click="dialog=true"
            style="position:fixed; right:10px; bottom:65px; z-index: 1000;"
            >
                <v-icon>mdi-plus-box</v-icon>
            </v-btn>
            <v-container fluid style="width:70%;" v-if="render && speccies.length > 0">
                <v-row dense>
                    <v-col v-for="o in speccies" :key="o.id" 
                    :cols="speccies.length%2 != 0 && speccies.indexOf(o) == speccies.length-1 ? 12 : 6">
                        <SpeccyCardVue 
                            :updateMaker="componentKey" 
                            :name="o.name"
                            :type="o.type"
                            :description="o.description"
                            :family="o.family"
                            :s_name="o.s_name"
                            :s_id="o.id"
                            :image="o.image"
                            :id="'speccy_'+o.id">
                        </SpeccyCardVue>
                    </v-col>
                </v-row>    
            </v-container>
            <div v-else style="color:gray;">
                <div style="display:flex; height:30%; position:absolute; transform: translate(-50%, -50%); left:50%; top:50%;  flex-direction: column; text-align: center; width:60%;">
                    <p style=" vertical-align: center; flex:1 1 auto;">No species registered yet</p>
                    <p style=" vertical-align: center; flex:1 1 auto;">Start adding a speccy to fill this screen up.</p>
                    <v-btn
                    style="vertical-align: center; flex:1 0 0;"
                    color="primary"
                    @click="dialog=true">add your first speccy</v-btn>
                </div>
                <span style="position:absolute; bottom:77px; right:65px;">You can also use this button<v-icon>mdi-arrow-right-thick</v-icon></span>
            </div>
        </div>
        <SpeccyDialogVue :open="dialog" :onClose="()=>dialog=false" :OK="sendNewSpeccy"></SpeccyDialogVue>
    </div>
</template>

<script>
import SpeccyCardVue from './SpeccyCard.vue';
import SpeccyDialogVue from './SpeccyDialog.vue';
import { BASE_API_URL } from '@/types/AppConstants';
import { getToken } from '../types/AppConstants';
import { ref } from 'vue';

export default {
    components:{
        SpeccyCardVue,SpeccyDialogVue
    },
    created()
    {
        this.updater = setInterval(()=>{
            this.update()
        }, 1000*60)
        this.update();
        this.bus.on("speccy_deleted", ()=>{this.update()});
        this.bus.on("speccy_updated", ()=>{this.update()});
    },
    data(){
        return {speccies:[], 
            dialog:false,
            render:true,
            updater:null,
            componentKey: ref(0)
        }
    },
    methods:{
        refresh()
        {
            this.componentKey += 1;
        },
        async sendNewSpeccy(speccy)
        {         
            let headers = new Headers();
            headers.append("Content-type", "application/json")
            headers.append("Access-Control-Allow-Origin", "*")
            headers.append("Authorization",  getToken())

            let init = { method: 'POST',
                        headers: headers,
                        body: JSON.stringify(speccy)};
            console.log(speccy)

            var request = new Request(BASE_API_URL+'api/species_create', init);

            fetch(request,init)
            .catch((err)=>{
                if("error" in err && err.error=="NOTAUTH")
                {                    
                    window.location.replace(BASE_API_URL+"admin/auth/login");
                    return;
                }
            })
            .then((data)=>{
                this.update()
                return data.json()
            }).then((data)=>{                
                if("error" in data && data.error=="NOTAUTH")
                {                    
                    window.location.replace(BASE_API_URL+"admin/auth/login?lostauth");
                    return;
                }
            })
            this.dialog = false;
        },
        update()
        {
            let headers = new Headers();

            let init = { method: 'GET',
                        headers: headers,
                        mode: 'cors',
                        cache: 'default' };

            var request = new Request(BASE_API_URL+'api/species', init);

            fetch(request,init)
            .then((data)=>{
                return data.json()
            })
            .then((json)=>{
                this.speccies = json.data;
                this.refresh()
            })
        }
    }
}
</script>
