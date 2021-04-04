<template>
    <div class="box" style="width: 60%; margin: auto;">
      <p class="is-size-3" style="padding-bottom: 2rem"> Search a Stock</p>
      <div v-if="searching">
        <div class="container" style="height: 80px;">
          <b-field>
              <b-loading :is-full-page="false" v-model="searching" :can-cancel="true"></b-loading>
          </b-field>
        </div>
        <br />
      </div>
      <div v-else-if="stockResponse">
        <b class="is-size-5">
          <img v-bind:src="stockResponse.logo" style="height:20px;vertical-align:middle"> {{stockResponse.name}}
        </b><br />
        <div class="columns" style="width: 30%; margin: auto; text-align: left;">
          <div class="column is-4">
            <p>
              Ticker:
            </p><br />
            <p>
              Exchange:
            </p>
          </div>
          <div class="column" style="font-weight: bold;float:right;text-align:right">
            <p>
              {{stockResponse.symbol}}
            </p><br />
            <p>
              {{stockResponse.exchange}}
            </p>
          </div>
        </div>
        <br/>
      </div>

      <div>
        <b-field>
            <b-autocomplete
                dropdown-position="bottom"
                rounded
                v-model="value"
                :data="tickerOptions"
                placeholder="e.g. AAPL"
                icon="magnify"
                :loading="isFetching"
                clearable
                @typing="getStockList"
                @select="option => getStockData(option)">
                <template #empty>No results found</template>
            </b-autocomplete>
        </b-field>
      </div>
    </div>
</template>

<script>
export default {
  name: 'StockSearch',
  props: {
  },
  data: function(){
    return {
        greeting: 'Hello, Vue!',
        value: '',
        stockResponse: '',
        tickerOptions: [],
        selectedTicker: '',
        isFetching: false,
        lastSearched: '',
        searching: false

    }
},
methods: {
        async getStockData(stock) {
          this.searching = true
          var url = 'http://127.0.0.1:5000/lookup/stock?stock=' + stock
          const gResponse = await fetch(url);
          const gObject = await gResponse.json();
          this.stockResponse = gObject.data;
          this.searching = false
          console.log(this.stockResponse)
        },
        async getStockList() {
            this.isFetching = true
            this.lastSearched = this.value
            var url = 'http://127.0.0.1:5000/lookup/autocomplete?stock=' + this.value
            const gResponse = await fetch(url);
            const gObject = await gResponse.json();
            console.log(gObject.data)
            this.tickerOptions = gObject.data;
            this.isFetching = false
        }
    },
    mounted () {
      // this.getStockList()
},
watch:{
  value: function(){
      this.getStockList()

  }

},
// created: async function(){
//         const gResponse = await fetch("http://127.0.0.1:5000/lookup?stock=App");
//         const gObject = await gResponse.json();
//         this.stockrespo = gObject.data;
// }
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
</style>
