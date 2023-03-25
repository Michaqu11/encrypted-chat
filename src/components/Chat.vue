<template>
    <div class="content">
      <button id="leaveButton" :onClick="disconnectFromChat">Connect to another chat</button>
      <div class="text">Choose message type</div>
      <div class="typeContainer">
        <div>
            <input type="radio" id="text" value="text" v-model="messageType" />
            <label for="text">Text</label>
        </div>
        <div>
            <input type="radio" id="file" value="file" v-model="messageType" />
            <label for="file">File</label>
        </div>
        <div class="text">Choose encoding type</div>
        <div v-if="messageType == 'text'">
            <input type="radio" id="ecb" value="ecb" v-model="encodingTextType" />
            <label for="ecb">ECB</label>
        </div>
        <div v-if="messageType == 'text'">
            <input type="radio" id="cbc" value="cbc" v-model="encodingTextType" />
            <label for="cbc">CBC</label>
        </div>
        <div class="textMsgContainer" v-if="(encodingTextType != '' && messageType == 'text')">
            <label for="textMsg">Write your message</label>
            <textarea id="textMsg" v-model="textMsg" rows="5" cols="40" maxlength="500"></textarea>
        </div>
        <button id="sendButton" v-if="textMsg != ''">Send</button>
      </div>
    </div>
</template>
  
  <script>
  
  import { useRouter } from 'vue-router';
  
  export default {
    name: 'ChatPage',
    props: {
      msg: String
    },
    components:{
      
    },
    setup() {
        const router = useRouter();
        return {
        router
        }
    },
    data() {
      return {
        messageType: '',
        encodingTextType: '',
        textMsg: ''
      }
    },
    methods: {
      disconnectFromChat() {
        this.router.push({path: '/'})
      }
    }
    
  }
  </script>
  
  <!-- Add "scoped" attribute to limit CSS to this component only -->
  <style scoped>
    #leaveButton {
        background-color: rgb(97, 0, 136);
        border-radius: 1vh;
        color: white;
        font-size: large;
        font-weight: bold;
        margin-top: 1vh;
    }
    .text {
        margin-bottom: 1vh;
        margin-top: 3vh;
        font-weight: bolder;
        font-size: x-large;
    }
    label {
        font-weight: bold;
        font-size: large;
    }
    .typeContainer {
        display: grid;
        place-items: center;
    }
    .typeContainer div {
        margin-top: 1vh;
    }
    .textMsgContainer {
        display: grid;
        place-items: center;
    }
    .textMsgContainer label {
        margin-top: 2vh;
        margin-bottom: 1vh;
        color: rgb(137, 168, 245);
        font-weight: bold;
        font-size: larger;
    }
    .textMsgContainer textarea {
        background-color: black;
        color: white;
        font-weight: bold;
        font-size: large;
        max-width: 20vw;
        max-height: 10vh;
        resize: none;
    }
    #sendButton {
        margin-top: 2vh;
        margin-bottom: 1vh;
        font-weight: bold;
        font-size: large;
        background-color: rgb(137, 168, 245);
        color: white
    }
  </style>
  