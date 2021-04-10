<template>
  <div class="columns">
    <div class="column is-one-fifth" id='user-menu'>
      <template>
        <b-menu>
          <b-menu-list label="Menu">
            <b-menu-item @click="setMidVoting" icon="vote" label="Vote"></b-menu-item>
            <b-menu-item v-if="admin" icon="cog-outline" expanded>
              <template #label="props">
                Administrator
                <b-icon class="is-pulled-right" :icon="props.expanded ? 'menu-down' : 'menu-up'"></b-icon>
              </template>
              <b-menu-item icon="account" @click="setMidUsers" label="Users"></b-menu-item>
              <b-menu-item icon="arrow-decision" @click="setMidDecisions" label="Decisions"></b-menu-item>
            </b-menu-item>
            <b-menu-item icon="account" label="My Account">
              <b-menu-item label="Change Info" @click="setMidChangeinfo"></b-menu-item>
              <b-menu-item label="Addresses"></b-menu-item>
            </b-menu-item>
          </b-menu-list>
          <b-menu-list>
            <b-menu-item label="Expo" icon="link" tag="router-link" target="_blank" to="/expo"></b-menu-item>
          </b-menu-list>
          <b-menu-list label="Actions">
            <b-menu-item label="Logout" @click="logout"></b-menu-item>
          </b-menu-list>
        </b-menu>
      </template>
    </div>
    <div class="column"></div>
    <div class="column is-half">
      <div v-if="midCol=='changeinfo'">
        Change info
      </div>
      <div v-if="midCol=='decisions'" v-bind:class="{decisionPanel: true}">
        <h1 v-bind:class="{'title is-4': true}" style='float:left'>Administrator - Create Decision</h1>
        <b-input placeholder='Title' maxlength="50" v-model="title"></b-input>
        <b-input type="textarea" placeholder='Description' v-model="description"></b-input>
        <br/>
        <b-button @click='createDecision' type="is-primary">Create</b-button>
      </div>
      <div v-if="midCol=='voting'">
        <h1 class="title">Partner Votes</h1>
        <Voting style=''></Voting>
      </div>
      <div v-if="midCol=='users'">
        <h1 class="title">Partners</h1>
        <AdminUsers></AdminUsers>
      </div>
    </div>
    <div class="column">
    </div>
  </div>
</template>

<script>
import Voting from './Voting.vue'
import AdminUsers from './AdminUsers.vue'

export default {
  components: { Voting, AdminUsers },
    name: 'User',
    data() {
        return {
            auth: this.$root.$data,
            admin: false,
            title: '',
            description: '',
            midCol: 'voting'
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
      },
      logout: function(){
        this.$root.$data.loggedIn = false
        this.$root.$data.authToken = null
        localStorage.clear()
        this.$router.push({ path: '/login' })
      },
      setMidVoting(){
        this.midCol = "voting"
      },
      setMidDecisions(){
        this.midCol = "decisions"
      },
      setMidUsers(){
        this.midCol = "users"
      },
      setMidChangeinfo(){
        this.midCol = "changeinfo"
      }
    },
    props: {
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>


.decisionPanel{
  background-color: #f0f0f0;
  margin: auto;
  margin-bottom: 45px;
  padding: 20px;
  border-radius: 10px;
  width: 75%;
}

#user-menu{
  text-align: left;
  padding: 60px;
  background-color:#f0f0f0;
  height: 100%;
  border-top-right-radius: 20px;
  border-bottom-right-radius: 20px;
}

#user-menu * {
  display: block;
}

</style>
