<template>
    <section>

        <b-table :data='data'
            :opened-detailed="defaultOpenedDetails"
            detailed
            detail-key="id"
            :detail-transition="transitionName"
            default-sort="date"
            default-sort-direction="desc"
            :show-detail-icon="showDetailIcon">

            <b-table-column field="title" label="Title" width="200" :td-attrs="columnTdAttrs" v-slot="props">
                {{ props.row.title }}
            </b-table-column>

            <b-table-column field="date" sortable label="Date" width="40" :td-attrs="columnTdAttrs" v-slot="props">
                {{ getDate(props.row.date) }}
            </b-table-column>

            <b-table-column field="passed" label="Passed?" width="5" :td-attrs="columnTdAttrs" numeric v-slot="props">
                {{ props.row.passed }}
            </b-table-column>

            <b-table-column field="vote" label="Vote" width="150" :td-attrs="columnTdAttrs" v-slot="props">
                <b-tag v-if='props.row.vote=="Nay"' type="is-danger"> Voted {{ props.row.vote }}</b-tag>
                <b-tag v-if='props.row.vote=="Yea"' type="is-success"> Voted {{ props.row.vote }}</b-tag>
                <b-tag  style='margin-right:10px' v-on:click.native="myVote(1, props.row.id)" v-bind:style="{cursor:'pointer'}" v-if='props.row.vote=="Vote"' type="is-warning"> Yea </b-tag>
                <b-tag v-on:click.native="myVote(0, props.row.id)" v-bind:style="{cursor:'pointer'}" v-if='props.row.vote=="Vote"' type="is-warning"> Nay </b-tag>
            </b-table-column>

            <template #detail="props">
                {{ props.row.description }}
            </template>
        </b-table>

    </section>
</template>

<script>
    export default {
        data() {
            return {
                auth: this.$root.$data,
                myDate: 0,
                showDetailIcon: true,
                data: [],
                votes: {},
            }
        },
        computed: {
            transitionName() {
                return 'fade'
            }
        },
        methods: {
            async getDecisions(myDate){
                const request = new Request(
                "http://127.0.0.1:5000/vote/decisions",
                    {
                        method: "POST",
                        mode: "cors",
                        cache: "default",
                        headers: {'Content-Type': 'application/json', 'Authentication': this.auth.authToken},
                        body: JSON.stringify({'date': myDate})
                    }
                );
                const response = await fetch(request);
                const data = await response.json();

                const request2 = new Request(
                "http://127.0.0.1:5000/vote/votes",
                    {
                        method: "POST",
                        mode: "cors",
                        cache: "default",
                        headers: {'Content-Type': 'application/json', 'Authentication': this.auth.authToken},
                        body: JSON.stringify({})
                    }
                );
                const response2 = await fetch(request2);
                const data2 = await response2.json();

                for(const el of data.data){

                    el.passed = el.passed == 0 ? "No" : "Yes"

                    el.vote = el.id in data2.data ? (data2.data[el.id]['for'] == 0 ? 'Nay' : 'Yea') : 'Vote'
                }

                console.log(data2.data[1])

                this.data = data.data
            },
            async myVote(side, decisionid){
                console.log(decisionid)
                console.log(side)
                const request = new Request(
                "http://127.0.0.1:5000/vote/cast",
                    {
                        method: "POST",
                        mode: "cors",
                        cache: "default",
                        headers: {'Content-Type': 'application/json', 'Authentication': this.auth.authToken},
                        body: JSON.stringify({'for': side, 'decisionid': decisionid})
                    }
                );
                const response = await fetch(request);
                const data = await response.json();
                console.log(data)
                this.getDecisions(0)
            },
            getDate(day){
                const date = new Date(day*1000);
                return(date.toLocaleDateString("en-US"))
            }
        },
        created() {
            if(this.auth.loggedIn){
                this.getDecisions(this.myDate)
            }
            else{
                this.$router.push({ path: '/login'})
            }
        }
    }
</script>