<template>
    <v-container fluid>
        <v-col style="margin:auto; display:flex; flex-direction: column; justify-content: start; width:70%;">
            <v-row>
                <v-card style="width:100%;">
                    <v-card-title>Manage users</v-card-title>
                    <v-table>
                        <thead>
                            <tr>
                                <th>Username</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="item in users"
                                :key="item.name"
                                >
                                <td>{{ item.username }}</td>
                                <td>
                                    <v-btn color="primary">modify</v-btn>
                                    <v-btn color="red" @click="deleteUser(item.username)">delete</v-btn>
                                </td>
                            </tr>
                        </tbody>
                    </v-table>
                </v-card>
            </v-row>
        </v-col>
    </v-container>
</template>

<script>
import { getToken } from '../types/AppConstants';
import { BASE_API_URL } from '../types/AppConstants';

export default {
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
            users:[]
        }
    },
    methods:{   
        refresh()
        {

        },  
        deleteUser(user)
        {
            let headers = new Headers();
            headers.append("Authorization", getToken())

            let init = { method: 'DELETE',
                        headers: headers,
                        mode: 'cors'};

            var request = new Request(BASE_API_URL+'api/user/'+user, init);

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
                    this.refresh()
                }
            })
        },
        update()
        {
            let headers = new Headers();
            headers.append("Authorization", getToken())

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
