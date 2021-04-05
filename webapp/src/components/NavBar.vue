<template>
    <b-navbar class="shdw" :fixed-top="true" style="background-color: rgb(165, 28, 48);">
        <template #brand>
            <b-navbar-item style="margins: 0;" tag="router-link" :to="{ path: '/' }">
                <img style="height=4.75rem;"
                    src="logo.png"
                    alt="Lightweight UI components for Vue.js based on Bulma"
                >
            </b-navbar-item>
        </template>
        <template #end>
            <b-navbar-item v-if="auth.loggedIn" tag="div">
                <b-tag type="is-light is-large">
                  {{ computedUsername }}
                </b-tag>
                <b-button v-on:click="logout" type="is-danger is-light" style='margin-left: 20px'>
                  Logout
                </b-button>
            </b-navbar-item>
        </template>
    </b-navbar>
</template>

<script>
export default {
    name: 'NavBar',
    data() {
        return {
            auth: this.$root.$data,
            username: ""
        }
    },
    computed: {
        computedUsername: function(){
          this.updateUsername()
          return this.username
        }
    },
    methods: {
        updateUsername: async function(){
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
          this.username = data.username == undefined ? "undef" : data.username
        },
        logout: function(){
          this.$root.$data.loggedIn = false
          this.$root.$data.authToken = null
          localStorage.clear()
        }
    },
    props: {
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}

.navbar-item img {
    max-height: 4.75rem;
}
.shdw {
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.15), 0 6px 20px 0 rgba(0, 0, 0, 0.25);
}
</style>
