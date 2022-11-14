<template>
    <v-container fluid style="width:70%;" v-if="render">
        <v-btn icon
        color="primary"
        style="position:fixed; right:10px; bottom:65px;"
        @click="dialog=true"
        >
            <v-icon>mdi-plus-box</v-icon>
        </v-btn>
        <v-row dense>
            <v-col v-for="o in speccies" :key="o.id" 
            :cols="speccies.length%2 != 0 && speccies.indexOf(o) == speccies.length-1 ? 12 : 6">
                <SpeccyCardVue 
                    :name="o.name"
                    :description="o.description"
                    :family="o.family"
                    :s_name="o.s_name"
                    :s_id="o.id"
                    :id="'speccy_'+o.id">
                </SpeccyCardVue>
            </v-col>
        </v-row>     
        <v-dialog 
        transition="dialog-bottom-transition"
        v-model="dialog"   
        max-width="600">
            <v-card>
                <v-toolbar
                color="primary"
                dark
                ><span 
                style="margin-left:10px;">Add a new speccy</span></v-toolbar>
                <v-card-text>
                    <v-form
                    v-model="newSpeccy.valid"
                    ref="newSpeccyForm"
                    lazy-validation>
                        <v-text-field 
                        clearable 
                        label="Common name" 
                        variant="outlined" 
                        prepend-icon="mdi-asterisk"
                        :rules="[rules.required]"
                        v-model="newSpeccy.name"></v-text-field>

                        <v-text-field 
                        clearable 
                        :rules="[rules.required]"
                        label="Scientific name" 
                        variant="outlined" 
                        prepend-icon="mdi-asterisk"
                        v-model="newSpeccy.s_name"></v-text-field>

                        <v-text-field 
                        clearable 
                        :rules="[rules.required]"
                        label="Family" 
                        variant="outlined" 
                        prepend-icon="mdi-asterisk"
                        v-model="newSpeccy.family"></v-text-field>

                        <v-text-field 
                        clearable 
                        :rules="[rules.required]"
                        label="Type" 
                        variant="outlined" 
                        prepend-icon="mdi-asterisk"
                        v-model="newSpeccy.type"></v-text-field>

                        <v-textarea 
                        counter="500" 
                        clearable 
                        :rules="[v => (v || '').length <= 500 ||
                        `A maximum of 500 characters is allowed`]"
                        label="Description" 
                        variant="outlined" 
                        v-model="newSpeccy.description"></v-textarea>
                    </v-form>
                </v-card-text>
                <v-card-actions class="justify-end">
                <v-btn
                    text
                    color="primary"
                    @click="sendNewSpeccy"
                >Save</v-btn>
                <v-btn
                    text
                    color="red"
                    @click="dialog = false"
                >Abort</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog> 
    </v-container>
</template>

<script>
import SpeccyCardVue from './SpeccyCard.vue';

export default {
    components:{
        SpeccyCardVue
    },
    created()
    {
        this.updater = setInterval(()=>{
            this.update()
        }, 1000*60*5)
        this.update();
        this.bus.on("speccy_deleted", (name)=>{this.update();console.log(name)});
    },
    data(){
        return {speccies:[], 
            render:true,
            dialog:false,
            newSpeccy:{
                name:null,
                s_name:null,
                family:null,
                description:null,
                type:null,
                valid:false
            },
            updater:null,
            rules:{
                required:v => (v || '').length > 0 ||
                    `This field is required`
            }
        }
    },
    methods:{
        refresh()
        {
            this.render = false
            this.$nextTick(()=>{
                this.render=true;
            })
        },
        async sendNewSpeccy()
        {
            const { valid } = await this.$refs.newSpeccyForm.validate()

            if (valid)
            {
                alert("Valid form")
                
                let headers = new Headers();
                headers.append("Content-type", "application/json")
                headers.append("Access-Control-Allow-Origin", "*")

                let init = { method: 'POST',
                            headers: headers,
                            body: JSON.stringify(this.newSpeccy)};

                var request = new Request('http://192.168.170.89:5000/api/species_create', init);

                fetch(request,init)
                .catch((err)=>{
                    console.log(err)
                })
                .then(()=>{
                    this.update()
                })
            }
        },
        update()
        {
            let headers = new Headers();

            let init = { method: 'GET',
                        headers: headers,
                        mode: 'cors',
                        cache: 'default' };

            var request = new Request('http://192.168.170.89:5000/api/species', init);

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
