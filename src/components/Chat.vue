<template>
  <div class="content">
    <button id="leaveButton" :onClick="disconnectFromChat">Connect to another chat</button>
    <div class="statusText">Status: <span id="green" v-if="status">connected</span><span id="red" v-else>disconnected</span></div>
    <div class="text">Choose message type</div>
    <div class="typeContainer">
      <div>
          <input type="radio" id="text" value="text" v-model="messageType" v-on:change="changeMessageType"/>
          <label for="text">Text</label>
      </div>
      <div>
          <input type="radio" id="file" value="file" v-model="messageType" v-on:change="changeMessageType"/>
          <label for="file">File</label>
      </div>
      <div class="text" v-i>Choose encoding type</div>
      <div>
          <input type="radio" id="ecb" value="ECB" v-model="encodingType" />
          <label for="ecb">ECB</label>
      </div>
      <div>
        <input type="radio" id="cbc" value="CBC" v-model="encodingType" />
        <label for="cbc">CBC</label>
      </div>
      <div class="textMsgContainer" v-if="(messageType === 'text' && encodingType !== '')">
          <label for="textMsg">Write your message</label>
          <textarea id="textMsg" v-model="textMsg" rows="5" cols="40" maxlength="500"></textarea>
      </div>
      <div v-if="(messageType === 'file' && encodingType !== '')">
        <input class="fileInput" type="file" @change="onFileChange" ref="file"/>
      </div><button id="sendButton" v-if="textMsg !== ''" :onClick="sendMessage" :disabled="!status || percentage > 0">Send</button></div>
  </div>
  <div id="progress-bar" v-if="percentage > 0">
    <div>
      <div>{{ percentage.toFixed() }}%</div>
      <div class="loading-bar">
        <div class="percentage" :style="{'width' : percentage + '%'}"></div>
      </div>
    </div>
  </div>
  <div class="chatContainer">
    <div class="chatContent">
      <div>Chat with <span v-if="chosedSide=='host'">Client</span><span v-if="chosedSide=='client'">Host</span></div>
      <div  class="allMessages" v-for="message in allMessages" :key="message">
        <div v-if="message.side == 'my'" class="my">{{ message.message }}</div>
        <div v-if="message.side == 'his'" class="his">
          {{ message.message }}<button @click="handleDownload(message)" v-if="message.type === 'file'">download</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

import { useRouter } from 'vue-router';
import { saveAs } from 'file-saver';
import axios from 'axios';

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
      textMsg: '',
      fileName: '',
      files: [],
      fileNames: [],
      encodingType: '',
      messagesFromFriend: [],
      myMessages: [],
      allMessages: [],
      connection: null,
      status: false,
      router: useRouter(),
      chosedSide: sessionStorage.getItem('chosedSide'),
      percentage: 0
    }
  },
  mounted() {
    let vueInstance = this;
    this.connection = new WebSocket(`${process.env.VUE_APP_SOCKET_URL}`);
    vueInstance.status = true;

    this.connection.onmessage = function (event) {
      let data = JSON.parse(event.data);
      if (data.type === 'progressInformation') {
        vueInstance.percentage = data.chunk / data.max * 100
        if (vueInstance.percentage >= 100) {
          vueInstance.percentage = 0;
        }
        return;
      }
      if (data.typeMessage === 'file') {
        vueInstance.percentage = 0;
        vueInstance.fileContent = data.message;
        let fileName = data.fileName;

        vueInstance.messagesFromFriend.push(fileName);
        vueInstance.allMessages.push({
          "message": fileName,
          "side": "his",
          "type" : data.typeMessage
        });
        vueInstance.fileNames.push(fileName);
        vueInstance.files.push(data.message);
        return;
      }
      if (JSON.parse(event.data).message == "disconnected") {
        vueInstance.status = false;
      } else {
        vueInstance.messagesFromFriend.push(data.message);
        vueInstance.allMessages.push({
          "message": data.message,
          "side": "his",
          "type" : data.typeMessage
        });
      }
    }
  },
  beforeUnmount() {
    this.connection.close();
  },
  methods: {
    disconnectFromChat() {
      this.status = false;
      this.connection.send(JSON.stringify({
          message: "disconnected",
          type: "text"
      }));
      this.router.push({path: '/'})
    },
    sendMessage() {
      this.connection.send(JSON.stringify({
        message: this.textMsg,
        type: this.messageType,
        mode: this.encodingType,
        fileName: this.fileName
      }));
      this.addMyMessage();
    },
    addMyMessage() {
      if (this.messageType === 'file') {
        this.myMessages.push(this.fileName);
        this.allMessages.push({
          "message":this.fileName,
          "side":"my"
        });
        this.textMsg = "";
        return;
      }
      this.myMessages.push(this.textMsg);
      this.allMessages.push({
        "message":this.textMsg,
        "side":"my"
      });
      this.textMsg = "";
    },
    onFileChange() {
      const fReader = new FileReader();
      fReader.onload = (event) => {
        this.textMsg = event.target.result;
      }
      this.fileName = this.$refs.file.files[0].name;
      fReader.readAsDataURL(this.$refs.file.files[0]);
    },
    changeMessageType() {
      this.textMsg = '';
    },
    downloadFile(url, name) {
      axios
        .get(url, { responseType: 'blob' })
        .then(response => {
          saveAs(response.data, name);
        })
    },
    handleDownload(message) {
      if (message.type !== "file") {
        return;
      }
      let fileIndex = this.fileNames.indexOf(message.message);
      this.downloadFile(this.files[fileIndex], message.message);
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
  .statusText {
    font-weight: bolder;
    font-size: large;
    margin-top: 1vh;
  }
  #green {
    color: green;
  }
  #red {
    color: red;
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
  #sendButton:disabled {
    background-color: gray;
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
  .his button {
    background-color: black;
    color: white;
    font-size: large;
    border-radius: 10px;
    border: 2px solid white;
    margin-left: 10px;
  }
  .his button:disabled {
    background-color: grey;
  }
  input[type=file] {
    width: 350px;
    max-width: 100%;
    color: #444;
    padding: 5px;
    background: #fff;
    border-radius: 10px;
    border: 1px solid #555;
    font-size: medium;
  }
  #progress-bar {
    font-size:xx-large;
    color: #222;
    width: 100%;
    height: 10vh;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .loading-bar {
    position: relative;
    width: 400px;
    height: 30px;
    border-radius: 15px;
    overflow: hidden;
    border: 1px solid black;
  }
  .percentage {
      position: absolute;
      display: block;
      height: 100%;
      border-radius: 15px;
      background-color: green;
      background-size: 30px 30px;
      animation: animate-stripes 3s linear infinite;
  }
  @keyframes animate-stripes {
    0% { background-position: 0 0; }
    100% { background-position: 60px 0; }
  }
</style>
