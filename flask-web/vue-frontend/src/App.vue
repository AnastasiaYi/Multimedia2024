<template>
  <img alt="Vue logo" src="./assets/image.png" class="logo-image">
  <HelloWorld msg="Welcome to Your Vue.js App"/>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'

export default {
  name: 'App',
  components: {
    HelloWorld
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
  /* margin-top: 45px; */

  background-image: url('./assets/bg5.jpg'); /* Replace with your image name */
  background-size: cover; /* Cover the entire area without stretching */
  background-position: center; /* Center the background image */
  background-repeat: no-repeat; /* Do not repeat the image */
}
.logo-image {
  width: 200px;
  height: auto;
  margin-top: 20px; /* Set your desired margin-top value */
}
</style>
