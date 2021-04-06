<template>
    <section style='width: 40%; margin: auto'>

        <b-table :data='data' :columns="columns"
            :opened-detailed="defaultOpenedDetails"
            detailed
            detail-key="id"
            :detail-transition="transitionName"
            :show-detail-icon="showDetailIcon">

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
                columns: [
                    {
                        field: 'id',
                        label: 'ID',
                        width: '40',
                        numeric: true
                    },
                    {
                        field: 'title',
                        label: 'Title',
                        width: '200'
                    },
                    {
                        field: 'date',
                        label: 'Date',
                        width: '40',
                    },
                    {
                        field: 'passed',
                        label: 'Passed?',
                        width: '5',
                        numeric: true
                    },
                ]
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
                for(const el of data.data){
                    const date = new Date(el.date*1000);
                    el.date = date.toLocaleDateString("en-US")

                    el.passed = el.passed == 0 ? "No" : "Yes"
                }

                this.data = data.data
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