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
        <button id="sendButton" v-if="textMsg != ''" :onClick="sendMessage">Send</button>
      </div>
    </div>
    <div class="chatContainer">
      <div class="chatContent">
        <div>Chat with <div v-if="chosedSide=='host'">Client</div><div v-if="chosedSide=='client'">Host</div></div>
        <div  class="allMessages" v-for="message in allMessages" :key="message">
          <div v-if="message.side == 'my'" class="my">{{ message.message }}</div>
          <div v-if="message.side == 'his'" class="his">{{ message.message }}</div>
        </div>
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
    data() {
      return {
        messageType: '',
        encodingTextType: '',
        encodingFileType: '',
        textMsg: '',
        messagesFromFriend: [],
        myMessages: [],
        allMessages: [],
        connection: null,
        router: useRouter(),
        chosedSide: sessionStorage.getItem('chosedSide')
      }
    },
    mounted() {
      let vueInstance = this;
      this.connection = new WebSocket(`${process.env.VUE_APP_SOCKET_URL}`);

      this.connection.onmessage = function(event) {
        vueInstance.messagesFromFriend.push(JSON.parse(event.data).message);
        vueInstance.allMessages.push({
          "message":JSON.parse(event.data).message,
          "side":"his"
        });
      }
    },
    beforeUnmount() {
      this.connection.close();
    },
    methods: {
      disconnectFromChat() {
        this.router.push({path: '/'})
      },
      sendMessage() {
        if (this.messageType == 'text') {
          this.connection.send(JSON.stringify({
            message: this.textMsg
          }));
          this.myMessages.push(this.textMsg);
          this.allMessages.push({
          "message":this.textMsg,
          "side":"my"
        });
        }
        this.textMsg = "";
      },
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
        max-width: 30vw;
        max-height: 10vh;
        resize: none;
    }
    #sendButton {
        margin-top: 2vh;
        margin-bottom: 1vh;
        font-weight: bold;
        font-size: large;
        border-radius: 1vh;
        background-color: rgb(137, 168, 245);
        color: white
    }
    .chatContainer {
      display: grid;
      place-items: center;
      margin-top: 2vh;
    }
    .chatContent {
      background-color: black;
      border-radius: 1vh;
      width: 40vw;
      height: auto;
      color: white;
      font-size: large;
      font-weight: bold;
      padding: 5px;
    }
    .allMessages{
      margin-top: 0.5vh;
      display: block;
    }
    .my {
      background-color: cornflowerblue;
      text-align: center;
      width: 50%;
      margin-left: 50%;
    }
    .his {
      background-color: lightgray;
      text-align: center;
      width: 50%;
    }
  </style>
  