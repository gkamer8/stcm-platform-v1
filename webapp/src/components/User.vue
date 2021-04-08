<template>
  <div>
    <div v-if="admin" v-bind:class="{adminPrivs: admin}">
        <h1 v-bind:class="{'title is-4': true}" style='float:left'>Administrator - Create Decision</h1>
        <b-input placeholder='Title' maxlength="50" v-model="title"></b-input>
        <b-input type="textarea" placeholder='Description' v-model="description"></b-input>
        <br/>
        <b-button @click='createDecision' type="is-primary">Create</b-button>
    </div>
    <h1 class="title">Partner Votes</h1>
    <Voting style='margin:auto;width:50%'></Voting>
  </div>
</template>

<script>
import Voting from './Voting.vue'

export default {
  components: { Voting },
    name: 'User',
    data() {
        return {
            auth: this.$root.$data,
            admin: false,
            title: '',
            description: ''
        }
    },
    mounted() {
      this.getAdminStatus()
    },
    computed: {

    },
    methods: {
      async getAdminStatus(){
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
        console.log(data)
        if('error' in data){
          this.$router.push({ path: '/login' })
        }
        else{
          this.admin = data['admin'] == 1 | data['admin'] == true ? true : false
        }
      },
      async createDecision(){
        const request = new Request(
            "http://127.0.0.1:5000/vote/create",
            {
                method: "POST",
                mode: "cors",
                cache: "default",
                headers: {'Content-Type': 'application/json', 'Authentication': this.auth.authToken},
                body: JSON.stringify({'title': this.title, 'description': this.description})
            }
        );

        const response = await fetch(request);
        const data = await response.json();

        if('error' in data){
          alert("Something went wrong.")
        }
        else if(data['message'] == 'success'){
          this.$router.go();
        }
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

.adminPrivs{
  background-color: #f0f0f0;
  margin: auto;
  margin-bottom: 45px;
  width: 30%;
  padding: 20px;
  border-radius: 10px;

}

</style>
