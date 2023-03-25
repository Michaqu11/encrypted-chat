<template>
  <img alt="logo" src="./assets/logo.png">
  <router-view msg="Welcome in S-CHAT Application!"></router-view>
</template>

<script>


export default {
  name: 'App',
  components: {
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
img {
  height: auto;
}
@media (min-width: 40em) {
  img {
    width: 20vw;
  }
}
@media (max-width: 40em) {
  img {
    width: 35vh;
  }
}
</style>
