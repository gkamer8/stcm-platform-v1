<template>
    <div class='box' style='width:40%;margin:auto'>
        <!-- <p class="is-size-4" style="padding-bottom: 1rem">Login</p> -->
        <img style="padding: 2% 10% 2% 10%" src="logo.jpg"/>
        <b-field style="margin-bottom: 0rem">
            <b-input v-model="username" spellcheck="false" placeholder='Username' maxlength="30"></b-input>
        </b-field>

        <b-field>
            <b-input type="password"
                placeholder='Password'
                password-reveal v-model="password">
            </b-input>
        </b-field>
        <b-message v-if="wrongPassword" type="is-danger" aria-close-label="Close message">
          Invalid Username or Password
        </b-message>
        <div style=" margin-top: 10px;">
          <b-button v-on:click="sendLogin" style='background-color:rgb(165, 28, 48);' class="button is-primary" expanded>Login</b-button>
        </div>

    </div>
</template>

<script>
    export default {
        data() {
            return {
                username: '',
                password: '',
                auth: this.$root.$data,
                wrongPassword: false
            }
        },
        methods: {
            async sendLogin(){
                const request = new Request(
                    "http://127.0.0.1:5000/auth/login",
                    {
                        method: "POST",
                        mode: "cors",
                        cache: "default",
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({'username': this.username, 'password': this.password})
                    }
                );

                const response = await fetch(request);
                const data = await response.json();
                console.log(data)
                if(data.error == undefined){
                    this.auth.loggedIn = true
                    this.auth.authToken = data.auth_token
                    localStorage.setItem('loggedIn', true)
                    localStorage.setItem('authToken', data.auth_token)
                    this.$router.push({ path: '/search' })
                }
                else{
                  this.wrongPassword = true
                }
            }
        },
        created() {

        }
    }
</script>
