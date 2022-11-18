<template>
    <v-container fluid>
        <v-col style="margin:auto; display:flex; flex-direction: column; justify-content: start; width:70%;">
            <v-row>
                <v-card style="width:100%;" v-if="users.length" :key="componentKey">
                    <v-card-title>Manage users<v-spacer></v-spacer><v-btn @click="createDialog=true">add</v-btn></v-card-title>
                    <v-table>
                        <thead>
                            <tr>
                                <th>Username</th>
                                <th>E-mail</th>
                                <th>Status</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="item in users"
                                :key="item.username"
                                >
                                <td>{{ item.username }}</td>
                                <td>{{ item.email }}</td>
                                <td><v-icon :color="item.active ? 'green' : 'red'">mdi-lan-connect</v-icon></td>
                                <td>
                                    <v-btn color="primary" @click="openModify(item)">modify</v-btn>
                                    <v-btn color="red" v-if="item.username != 'admin'" @click="openDelete(item.id)">delete</v-btn>
                                </td>
                            </tr>
                        </tbody>
                    </v-table>
                </v-card>
            </v-row>
        </v-col>
        <UserModalVue 
        :open="modifyDialog" 
        :onClose="()=>modifyDialog=false" 
        :OK="updateUser" 
        :user="modifyingUser"></UserModalVue>
        <UserModalVue 
        :open="createDialog"
        :onClose="()=>createDialog=false" 
        :OK="addUser"></UserModalVue>
        <v-dialog v-model="deleteConfirm">
            <v-card width="500px" style="margin:auto;">
                <v-card-title>Do you really want to delete this user ?</v-card-title>
                <v-card-text>This action cannot be undone</v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="primary" @click="deleteConfirm=false">Cancel</v-btn>
                    <v-btn color="red" @click="this.deleteUser">Confirm</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </v-container>
</template>

<script>
import { getToken } from '../types/AppConstants';
import { BASE_API_URL } from '../types/AppConstants';
import { ref } from "vue"
import UserModalVue from "./UserModal.vue"

export default {
    components:{
        UserModalVue    
    },
    created()
    {        
        this.updater = setInterval(()=>{
            this.update()
        }, 1000*60)
        this.update();
    },
    data(){
        return {
            updater:null,
            users:[],
            componentKey: ref(0),
            modifyDialog:false,
            createDialog:false,
            deleteConfirm:false,
            modifyingUser:null,
            deleteId:null
        }
    },
    methods:{   
        openDelete(id)
        {
            this.deleteId = id;
            this.deleteConfirm=true
        },
        refresh()
        {
            this.componentKey+=1
        },  
        updateUser(user)
        {
            let headers = new Headers();
            headers.append("Authorization", getToken())
            headers.append("Content-type", "application/json")
            headers.append("Access-Control-Allow-Origin", "*")

            let init = { method: 'POST',
                        headers: headers,
                        mode: 'cors',
                        body:JSON.stringify(user)
                    };

            var request = new Request(BASE_API_URL+'api/user/'+user.id, init);

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
                    this.update()
                }
            })
            this.modifyDialog=false
        },
        addUser(user){
            let headers = new Headers();
            headers.append("Authorization", getToken())
            headers.append("Content-type", "application/json")
            headers.append("Access-Control-Allow-Origin", "*")

            let init = { method: 'POST',
                        headers: headers,
                        mode: 'cors',
                        body:JSON.stringify(user)
                    };

            var request = new Request(BASE_API_URL+'api/user', init);

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
                    this.createDialog=false
                    this.update()
                }
            })
        },
        openModify(user)
        {
            this.modifyingUser=user
            this.modifyDialog=true
        },
        deleteUser()
        {
            let headers = new Headers();
            headers.append("Authorization", getToken())
            headers.append("Access-Control-Allow-Origin", "*")

            let init = { method: 'DELETE',
                        headers: headers,
                        mode: 'cors'};

            var request = new Request(BASE_API_URL+'api/user/'+this.deleteId, init);

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
                    this.deleteConfirm=false
                    this.update()
                }
            })
        },
        update()
        {
            let headers = new Headers();
            headers.append("Authorization", getToken())
            headers.append("Access-Control-Allow-Origin", "*")

            let init = { method: 'GET',
                        headers: headers,
                        mode: 'cors'};

            var request = new Request(BASE_API_URL+'api/users', init);

            fetch(request,init)
            .then((data)=>{
                return data.json()
            })
            .then((json)=>{
                this.users = json.data;
                this.refresh()
            })
        }
    }
}
</script>
