<template>
    <section>
        <b-field label="Name">
            <b-input v-model="regname" value="regname"></b-input>
        </b-field>
        <b-field label="Username">
            <b-input v-model="username" value="username"></b-input>
        </b-field>
        <b-field label="Password">
            <b-input type='password' v-model="password"></b-input>
        </b-field>
        <b-field label="Email">
            <b-input v-model="email" value="email"></b-input>
        </b-field>
        <b-button @click='sendChanges'>Send Changes</b-button>
        <br/><br/>
        <b-message v-if="regFail" type="is-danger" aria-close-label="Close message">
            Change Failed: {{ errorMessage }}
        </b-message>
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
            }
        },
        methods: {
            async getInfo(){
                const request = new Request(
                "http://127.0.0.1:5000/auth/userinfo",
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

                if(!('error' in data)){
                    this.username = data['username']
                    this.regname = data['name']
                    this.email = data['email']
                }

                console.log(this.data)
            },
            async sendChanges(){
                if(this.password == ''){
                    this.errorMessage = "Please enter password"
                    this.regFail = true
                    return
                }
                const request = new Request(
                "http://127.0.0.1:5000/auth/changeinfo",
                    {
                        method: "POST",
                        mode: "cors",
                        cache: "default",
                        headers: {'Content-Type': 'application/json', 'Authentication': this.auth.authToken},
                        body: JSON.stringify({'username':this.username, 'password':this.password, 'email':this.email, 'name':this.regname})
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
                this.getInfo()
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
