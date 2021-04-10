<template>
    <section>
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
