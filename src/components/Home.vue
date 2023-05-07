<template>
  <div class="content">
    <h1>{{ msg }}</h1>
    <Steppy v-model:step="step" :finalize="connectToChat"  primaryColor1="rgb(137, 168, 245)">

      <template #1>
        <div class="text">Please sign in to continue</div>
        <div class="loginContent">
          <label for="login">Login: </label>
          <input v-model="login" name="login" autocomplete="off">
          <label for="password">Password: </label>
          <input v-model="password" type="password" name="password" autocomplete="off">
          <button class="button" id="signInButton" :disabled="!(login.length && password.length)" :onClick="signIn">Sign In</button>
          <div id="successText" v-if="signedIn">Signed In successfully</div>
        </div>
      </template>

      <template #2>
        <div class="secondContainer">
          <div class="text" v-if="canToSecond()">Generate a key</div>
          <div>
            <input type="radio" id="1024" value="1024" v-model="rsaSize" />
            <label for="1024">RSA-1024</label>
            <input type="radio" id="2048" value="2048" v-model="rsaSize" />
            <label for="2048">RSA-2048</label>
          </div>
          <button class="button" :onClick="generateKey">Generate</button>
          <div id="successText" v-if="isKey">Key generated successfully</div>
        </div>
      </template>

      <template #3>
        <div class="text" v-if="canToThird()">Choose side</div>
        <div class="sideContent">
          <div>
            <input type="radio" id="client" value="client" v-model="chosedSide" />
            <label for="client">Client</label>
            <input type="radio" id="host" value="host" v-model="chosedSide" />
            <label for="host">Host</label>
          </div>
          <div id="ipDiv" v-if="chosedSide == 'client'">
            <label for="ip">Ip: </label>
            <input type="text" id="ip" v-model="ip" autocomplete="off"/>
          </div>
        </div>
      </template>
    </Steppy>
  </div>
</template>

<script>
import { Steppy } from 'vue3-steppy'
import { ref } from "vue";
import axios from 'axios';
import { useRouter } from 'vue-router';

const IS_SIGNED_IN = 'isSignedIn';

export default {
  name: 'HomePage',
  props: {
    msg: String
  },
  components:{
    Steppy
  },
  setup() {
    const step = ref(1);
    const router = useRouter();
    return {
      step,
      router
    }
  },
  data() {
    return {
      login: '',
      password: '',
      chosedSide: '',
      ip: '',
      isKey: false,
      rsaSize: 1024,
      signedIn: false
    }
  },
  methods: {
    signIn() {
      let userDto = {
        "login" : this.login,
        "password" : this.password
      }
      axios.post(process.env.VUE_APP_BACKEND_URL + '/login', userDto)
        .then(response => {
          console.log(response);
          this.signedIn = true;
          sessionStorage.setItem(IS_SIGNED_IN, true);
        })
        .catch(function (error) {
          if (sessionStorage.getItem(IS_SIGNED_IN)) {
            sessionStorage.removeItem(IS_SIGNED_IN);
          }
          alert("Something went wrong")
          console.log(error);
        });
    },
    isSignedIn() {
      return sessionStorage.getItem(IS_SIGNED_IN);
    },
    canToSecond() {
      if (this.isSignedIn()) {
        return true;
      }
      location.reload();
      alert("Please sign in")
      return false;
    },
    async generateKey() {
      await axios.get(process.env.VUE_APP_BACKEND_URL + '/key', { params: { size : this.rsaSize }});
      this.isKey = true;
    },
    isKeyGenerated() {
      return this.isKey;
    },
    canToThird() {
      if (!this.isKeyGenerated()) {
        location.reload();
        alert("Generate key properly please");
        return false;
      }
      return true;
    },
    connectToChat() {
      let connectionOptions = {
        "chosedSide" : this.chosedSide,
        "ip" : this.ip
      }
      sessionStorage.setItem("chosedSide", this.chosedSide);
      axios.post(process.env.VUE_APP_BACKEND_URL + '/side', connectionOptions)
        .then(result => {
          this.ip = result.data;
          console.log(result);
          this.startConnection();
        })
        .catch(function(error) {
          alert("Something went wrong")
          console.log(error);
        })
    },
    startConnection() {
      axios.post(process.env.VUE_APP_BACKEND_URL + '/start_connection')
        .then(result => {
          console.log(result)
          this.router.push({path: 'chat'})
        })
        .catch(function(error) {
          alert("Something went wrong")
          console.log(error);
        })
    }
  }
  
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1 {
  color: rgb(137, 168, 245);
}
.text {
  margin-bottom: 1vh;
  font-weight: bolder;
  font-size: x-large;
}
.loginContent {
  display: grid;
  place-items: center;
}
label, input {
  margin-bottom: 1vh;
}
label {
  font-size: large;
}
.button {
  background-color: rgb(137, 168, 245);
  border-radius: 1vh;
  color: white;
  font-size: large;
  font-weight: bold;
  margin-top: 1vh;
}
#signInButton:disabled {
  background-color: gray;
}
.sideContent {
  display: block;
}
.sideContent label, .sideContent input {
  margin-right: 1vw;
}
.sideContent label {
  font-weight: bold;
  font-size: large;
}
#ipDiv {
  margin-top: 2vh;
}
#successText {
  margin-top: 1vh;
  font-weight: bold;
  font-size: large;
  color: green;
}
.secondContainer {
  display: block;
}
.secondContainer label, .secondContainer input {
  margin-right: 1vh;
  font-size: large;
  font-weight: bold;
}
</style>
