<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    {{ step }}
    <Steppy v-model:step="step" :finalize="route" :loading="true" primaryColor1="rgb(137, 168, 245)">
      <template #1>Logowanie</template>
      <template #2>Generowanie Klucza</template>
      <template #3>Wybór strony</template>
    </Steppy>
  </div>
</template>

<script>
import { Steppy } from 'vue3-steppy'
import { useRouter } from 'vue-router';
import { ref } from "vue";
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
    const route = () => {
      router.push({ path: 'chat' });
    };
    return {
      step,
      route
    }
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
</style>
