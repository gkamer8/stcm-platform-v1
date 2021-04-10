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
        <br/>
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
                    this.$router.go();
                }

                console.log(this.data)
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
