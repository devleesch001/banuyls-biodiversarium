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
            style="margin-left:10px;">Add a new speccy</span></v-toolbar>
            <v-card-text>
                <v-form
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

                    <div style="display:flex; justify-content: center; margin-bottom:30px;">
                        <v-file-input label="Speccy image" @change="loadImage"></v-file-input>
                    </div>
                    <v-img v-if="newSpeccy.image" :src="newSpeccy.image" ></v-img>

                    <v-select
                    label="Type"
                    :items="types"
                    :rules="[rules.required]"
                    v-model="newSpeccy.type"
                    selected
                    >        
                        <template #selection="{item}">
                            <span><v-icon style="margin-right:10px;">mdi-{{allTypes[item.value]}}</v-icon>{{item.value}}</span>
                        </template>         
                    </v-select>

                    <v-tabs
                    v-model="lang"
                    bg-color="primary"
                    >
                        <v-tab v-for="lang in langs" :key="lang" :value="lang">{{lang}}</v-tab>
                    </v-tabs>
                    <v-window v-model="lang">
                        <v-window-item v-for="lang in langs" :key="lang" :value="lang">
                            <v-textarea 
                            counter="1500" 
                            clearable 
                            :rules="[v => (v || '').length <= 1500 ||
                            `A maximum of 1500 characters is allowed`]"
                            label="Description" 
                            v-model="newSpeccy.description[lang]"></v-textarea>
                        </v-window-item>
                    </v-window>
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
import {TYPES_ICON} from "@/types/AppConstants"

export default {
    
    props: {
        open:Boolean,
        OK:Function,
        onClose:Function,
        default:Object
    },

    data(){
        return {      
            dialog:false,      
            rules:{
                required:v => (v || '').length > 0 ||
                    `This field is required`
            },
            newSpeccy:this.default ?? {
                name:null,
                s_name:null,
                family:null,
                description:{
                    fr:null,
                    en:null
                },
                image:null,
                type:Object.keys(TYPES_ICON)[0]
            },
            langs:['fr', 'en'],
            allTypes:TYPES_ICON,
            lang:"fr",
        }
    },
    computed:{
        types()
        {
            return Object.keys(TYPES_ICON)
        }
    },
    watch:{
        open(n, o)
        {
            unused(o);
            this.dialog=n;
        }
    },
    methods:{
        async send()
        {
            const { valid } = await this.$refs.newSpeccyForm.validate()
            if(valid)
            {
                this.OK(this.newSpeccy)
            }
        },
        loadImage(image){
            var reader = new FileReader();
            reader.readAsDataURL(image.target.files[0]);
            let self = this;
            reader.onload = function () {
                self.newSpeccy.image = reader.result
                console.log(self.newSpeccy.image)
            };
            reader.onerror = function (error) {
                console.log('Error: ', error);
            };
        },
        close()
        {
            this.onClose()
        }
    }
}
</script>
