<template>
    <section>
        <div id="positions-table">
            <b-table :data='data'
                :paginated="true"
                :per-page="25"
                default-sort-direction="desc">

                <b-table-column field="symbol" sortable label="Symbol" width="15" :td-attrs="columnTdAttrs" v-slot="props">
                    {{ props.row.symbol }}
                </b-table-column>

                <b-table-column field="marketValue" numeric sortable label="Market Value" :td-attrs="columnTdAttrs" v-slot="props">
                    {{ "$" + props.row.marketValue.toFixed(2) }}
                </b-table-column>

                <b-table-column field="averagePrice" numeric sortable label="Average Price" :td-attrs="columnTdAttrs" v-slot="props">
                    {{ "$" + props.row.averagePrice.toFixed(2) }}
                </b-table-column>

                <b-table-column field="longQuantity" numeric sortable label="Long Quantity" :td-attrs="columnTdAttrs" v-slot="props">
                    {{ props.row.longQuantity }}
                </b-table-column>

                <b-table-column field="return" sortable numeric label="Return" :td-attrs="columnTdAttrs" v-slot="props">
                    {{ (100 * props.row.return).toFixed(2) + "%" }}
                </b-table-column>

                <b-table-column field="profit" sortable numeric label="Profit" :td-attrs="columnTdAttrs" v-slot="props">
                    {{ "$" + props.row.profit.toFixed(2) }}
                </b-table-column>


            </b-table>
        </div>
    </section>
</template>

<script>
    export default {
        data() {
            return {
                auth: this.$root.$data,
                data: [],
                dollarFormatter: new Intl.NumberFormat('en-US', {style: 'currency', currency: 'USD'})
            }
        },
        methods: {
            async getUsers(){
                const request = new Request(
                "http://127.0.0.1:5000/fund/positions",
                    {
                        method: "POST",
                        mode: "cors",
                        cache: "default",
                        headers: {'Content-Type': 'application/json', 'Authentication': this.auth.authToken},
                        body: JSON.stringify({})
                    }
                );
                const response = await fetch(request);
                const data = await response.json();
                this.data = data.data

                // Calculate profit in $ and %
                for(var i = 0; i < this.data.length; i++){
                    this.data[i].profit = this.data[i].marketValue - this.data[i].longQuantity * this.data[i].averagePrice
                    this.data[i].return = this.data[i].profit / (this.data[i].longQuantity * this.data[i].averagePrice)
                }

                console.log(this.data)
            }
        },
        created() {
            if(this.auth.loggedIn){
                this.getUsers()
            }
            else{
                this.$router.push({ path: '/login'})
            }
        }
    }
</script>

<style scoped>

.b-table{
    text-align:left;
}

#positions-table{
    width: 75%;
    margin: auto;
    margin-bottom: 250px;
}

</style>
