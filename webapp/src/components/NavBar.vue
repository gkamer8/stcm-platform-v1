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
        <!-- <template #start>
            <b-navbar-item style=" color: white;" href="#">
                <b> Stock Search </b>
            </b-navbar-item>
        </template> -->
    </b-navbar>
</template>

<script>
export default {
  name: 'NavBar',
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
