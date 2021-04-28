<template>
  <div id="app">
    <h1>  Test Byne</h1>
    <button v-on:click="getNumbers()">Get Numbers</button>
    <table>
      <thead>
        <tr>
          <th>Id</th>
          <th>Number</th>
          <th>Timestamp</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="line in data" :key="line._id.$oid" >
          <td> {{line._id.$oid}}</td>
          <td> {{line.number}}</td>
          <td> {{line.timestamp.$date}}</td>

        </tr>
      </tbody>
    </table>

  </div>
</template>

<script>

export default {
  name: 'App',
  data() {
    return {
      data : []
    }
  },
  methods: {
    getNumbers: function() {
      console.log(this);
      this.$wamp.call('api.get_numbers', []).then((result) => {
        console.log('api.get_numbers', result)
        this.data = result
      })

    }
  },
  mounted() {
    console.log('mounted')
    this.$on('$wamp.status', ({status}) => {
      console.log('status', status)
    });
    this.$on('$wamp.opened', ({status}) => {
      console.log('opened', status)
    });
  },

}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
