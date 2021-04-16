<template>
    <section>

        <div id='register'>
            <div class="columns">
                <div class="column">
                    <b-field label="">
                        <b-input v-model="regname" placeholder="Name"></b-input>
                    </b-field>
                    <b-field label="">
                        <b-input v-model="username" placeholder="Username"></b-input>
                    </b-field>
                    <b-field label="">
                        <b-input v-model="email" placeholder="Email"></b-input>
                    </b-field>
                </div>
                <div class="column">
                    <b-field label="">
                        <b-input v-model="stake" placeholder="Stake (decimal)"></b-input>
                    </b-field>
                    <b-field label="">
                        <b-input v-model="password" placeholder="Password" type='password'></b-input>
                    </b-field>
                    <div class='columns'>
                        <div class="column">
                            <b-field label="">
                                <b-input v-model="admin" placeholder="Admin (1 or 0)" type='number'></b-input>
                            </b-field>
                        </div>
                        <div class='column'>
                            <b-button button is-primary @click="addNewUser">Add New user</b-button>
                        </div>
                    </div>
                </div>
            </div>
            <b-message v-if="regFail" type="is-danger" aria-close-label="Close message">
                Registration Failed: {{ errorMessage }}
            </b-message>
        </div>
        <hr/>
        <div id="edit">
            <div class='columns'>
                <div class="column">
                    <b-input type="number" v-model="editid" style="width:65px" placeholder="ID"></b-input>
                </div>
                <div class="column">
                    <b-select v-model="editfield" placeholder="Field">
                        <option value="name">Name</option>
                        <option value="username">Username</option>
                        <option value="password">Password</option>
                        <option value="admin">Admin</option>
                        <option value="email">Email</option>
                        <option value="stake">Stake</option>
                    </b-select>
                </div>
                <div class="column is-half">
                    <b-input v-model="editvalue" placeholder="Value"></b-input>
                </div>
                <div class="column">
                    <b-button @click="sendEdit" is-primary>Edit</b-button>
                </div>
            </div>
        </div>
        <br/>
        <b-message v-if="editFail" type="is-danger" aria-close-label="Close message">
            Editing Failed: {{ errorMessage }}
        </b-message>
        <b-table :data='data'
            default-sort="stake"
            default-sort-direction="desc">

            <b-table-column field="id" sortable label="ID" numeric width="10" :td-attrs="columnTdAttrs" v-slot="props">
                {{ props.row.id }}
            </b-table-column>

            <b-table-column field="username" sortable label="Username" width="40" :td-attrs="columnTdAttrs" v-slot="props">
                {{ props.row.username }}
            </b-table-column>

            <b-table-column field="stake" sortable label="Stake" width="5" :td-attrs="columnTdAttrs" v-slot="props">
                {{ props.row.stake * 100 + "%" }}
            </b-table-column>

            <b-table-column field="name" label="Name" width="150" :td-attrs="columnTdAttrs" v-slot="props">
                {{ props.row.name }}
            </b-table-column>

            <b-table-column field="email" label="Email" width="150" :td-attrs="columnTdAttrs" v-slot="props">
                {{ props.row.email }}
            </b-table-column>

            <b-table-column field="delete" label="" style="text-align:center" width="10" :td-attrs="columnTdAttrs" v-slot="props">
                <b-icon icon="delete" v-on:click.native="delUser(props.row.id)" v-bind:style="{cursor:'pointer'}" type="is-danger"></b-icon>
            </b-table-column>

            <template #detail="props">
                {{ props.row.description }}
            </template>
        </b-table>

    </section>
</template>

<script>
    export default {
        data() {
            return {
                auth: this.$root.$data,
                data: [],
                regFail: false,
                errorMessage: "",
                username: "",
                password: "",
                regname: "",
                email: "",
                stake: "",
                admin: "",
                editfield: "",
                editid: "",
                editvalue: "",
                editFail: false
            }
        },
        methods: {
            async getUsers(){
                const request = new Request(
                "http://127.0.0.1:5000/auth/allusers",
                    {
                        method: "POST",
                        mode: "cors",
                        cache: "default",
                        headers: {'Content-Type': 'application/json', 'Authentication': this.auth.authToken},
                        body: JSON.stringify({})
                    }
                );
                const response = await fetch(request);
                const data = await response.json();

                this.data = data.data
                console.log(this.data)
            },
            async addNewUser(){
                this.stake = parseFloat(this.stake)
                this.admin = parseInt(this.admin)
                const request = new Request(
                "http://127.0.0.1:5000/auth/register",
                    {
                        method: "POST",
                        mode: "cors",
                        cache: "default",
                        headers: {'Content-Type': 'application/json', 'Authentication': this.auth.authToken},
                        body: JSON.stringify({'username':this.username, 'password':this.password, 'email':this.email, 'stake':this.stake, 'name':this.regname, 'admin':this.admin})
                    }
                );
                const response = await fetch(request);
                const data = await response.json();

                if(data.error != undefined){
                    this.errorMessage = data['error']
                    this.regFail = true;
                }
                else{
                    this.regFail = false;
                    this.getUsers()
                }

                console.log(this.data)
            },
            async sendEdit(){
                const request = new Request(
                "http://127.0.0.1:5000/auth/edit",
                    {
                        method: "POST",
                        mode: "cors",
                        cache: "default",
                        headers: {'Content-Type': 'application/json', 'Authentication': this.auth.authToken},
                        body: JSON.stringify({'value':this.editvalue, 'id':this.editid, 'field':this.editfield})
                    }
                );
                const response = await fetch(request);
                const data = await response.json();

                if(data.error != undefined){
                    this.errorMessage = data['error']
                    this.editFail = true;
                    console.log("ERROR")
                }
                else{
                    this.editFail = false
                    this.getUsers()
                }
            },
            async delUser(userid){
                const request = new Request(
                "http://127.0.0.1:5000/auth/delete",
                    {
                        method: "POST",
                        mode: "cors",
                        cache: "default",
                        headers: {'Content-Type': 'application/json', 'Authentication': this.auth.authToken},
                        body: JSON.stringify({'userid':userid})
                    }
                );
                const response = await fetch(request);
                const data = await response.json();

                if(data.error != undefined){
                    this.errorMessage = data['error']
                    this.editFail = true;
                }
                else{
                    this.editFail = false
                    this.getUsers()
                }
            }
        },
        created() {
            if(this.auth.loggedIn){
                this.getUsers()
            }
            else{
                this.$router.push({ path: '/login'})
            }
        }
    }
</script>

<style scoped>

.b-table{
    text-align:left;
}

</style>
