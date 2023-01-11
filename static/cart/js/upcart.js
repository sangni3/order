const app = new Vue({
    el: '#cart',
    data:{
        carts:[],
        user:[],
        user1:'123'
    },
    mounted:function(){
        this.searchMusic()
    },
    methods:{
        searchMusic(){
            var that=this;
            axios.get("http://127.0.0.1:8000/upcart/")
                .then(function (response) {
                    that.carts=JSON.parse(response.data.cartslist)
                    that.user=JSON.parse(response.data.user)
                }, function (err) {})},
    },
})
