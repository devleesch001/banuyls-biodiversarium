<template>
    <v-card class="mx-auto speccy-card" 
        outlined
        :color="randomColor">
        <v-toolbar
        style="padding-left:2%; background-color: transparent;">
            <v-icon style="margin-right:10px;">mdi-fish</v-icon>
            <v-card-title>{{name}}</v-card-title>
            <v-spacer></v-spacer>
            <v-img 
                aspect-ratio="1"
                src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSbRnBlrAbDhCz9ArlqOGVai4V0vXhIDGOOIQ&usqp=CAU"
                cover>
            </v-img>
        </v-toolbar>
        <div class="speccy-subtitle">
            <div class="text-subtitle-1 speccy-scientific">
                {{s_name}}
            </div>
            <div> | </div>
            <div>
                {{family}}
            </div>
        </div>
        <v-divider class="mx-4"></v-divider>
        <v-card-text>
            {{description}}
        </v-card-text>
        <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn icon style="background-color: white;" elevation="3">
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
    </v-card>
</template>

<script>
export default {
    props:{
        name:String,
        s_name:String,
        description:String,
        family:String,
        s_id:Number
    },
    data: ()=>({
        deleteConfirm:false
    }),
    methods:{
        delete(){
            fetch('http://192.168.170.89:5000/api/species_delete/'+this.s_id, {method:"DELETE"})
            .catch((err)=>{
                console.log(err)
            })
            .then(()=>{
                this.bus.emit("speccy_deleted", this.name)
            })
        }
    },
    computed:{
        randomColor(){
            let colors = [
                "#8fffaa",
                "#ffcc5a",
                "#00ab0f",
                "#bd9dff"
            ]
            return colors[Math.floor(Math.random()*colors.length)]
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
        justify-content: left;
        width:300px;
    }

    .speccy-subtitle > div{
        font-size: 0.9em !important;
        flex:1 1 auto;
        text-align: center;
    }

    .speccy-scientific{
        font-style: italic;
    }
</style>